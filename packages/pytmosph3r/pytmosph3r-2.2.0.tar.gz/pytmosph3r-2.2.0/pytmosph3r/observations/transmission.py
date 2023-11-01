import exo_k as xk
import numba
import numpy as np
from tqdm.auto import tqdm

from pytmosph3r.log import Logger
from pytmosph3r.util.constants import KBOLTZ
from pytmosph3r.util.memory import memory_usage, MemoryUtils
from pytmosph3r.util.util import make_array, spectral_chunks, timer
from ..aerosols import PrepareAerosols
from ..atmosphere import AltitudeAtmosphere
from ..rays import init_rays, Rays


@numba.njit
def compute_optical_depth_mie(P, T, rays_lengths, cross_section, mie_abs_coeff, opacity_indices, rays_list, n_rays,
                              n_intersection, tau):
    """Computes tau, the optical depth."""
    for r in range(n_rays):
        ray = rays_list[r]
        ray_coords = ray
        for i in range(n_intersection):
            data = rays_lengths[ray_coords][i]
            if data[0] == -1:
                break
            coord = (int(data[0]), int(data[1]), int(data[2]))
            ray_length = data[3]
            mie = mie_abs_coeff[opacity_indices[coord]]
            tau[ray] += ray_length * (
                (P[coord] / (KBOLTZ*T[coord]) * cross_section[opacity_indices[coord]])
                + mie )


@numba.njit
def compute_optical_depth(P, T, rays_lengths, cross_section,  opacity_indices, rays_list, n_rays, n_intersection, tau):
    """Computes tau, the optical depth."""
    for r in range(n_rays):
        ray = rays_list[r]
        ray_coords = ray
        for i in range(n_intersection):
            data = rays_lengths[ray_coords][i]
            if data[0] == -1:
                break
            coord = (int(data[0]), int(data[1]), int(data[2]))
            ray_length = data[3]
            tau[ray] += ray_length * (P[coord] / (KBOLTZ*T[coord])
                         * cross_section[opacity_indices[coord]])


class Transmission(Logger):
    """The transmission module computes the transit depth :math:`(R_P/R_S)^2` given a set of :attr:`rays` crossing the atmosphere.
    """
    def __init__(self, rays=None, store_transmittance=None, identical=None, memory_aware=None, per_angle=True):
        """The transmission module has several parameters:

        Args:
            rays (:class:`~pytmosph3r.rays.Rays` or dict) : Defining the grid (`n_radial`, `n_angular`) of light rays that cross the atmosphere.
            store_transmittance (bool): Stores transmittance in output.
            identical (bool) : Activates the search for identical cells for which to compute the opacities only once. (Should be used when there is a lot of homogeneous data in the model).
            memory_aware (bool) : Try to stay under a memory fixed threshold (experimental).
            per_angle (bool) : Compute the transit depth per angle in the grid of rays, to be able to free the memory of the optical depths of the rays of that angle once they're done. Defaults to True.
        """
        super().__init__(self.__class__.__name__)

        self.store_transmittance = store_transmittance
        """Stores transmittance in output."""
        if Logger.verbose:
            self.store_transmittance = True
        self.identical = identical
        """Computes only once the opacity for cells with identical physical properties (True by default). You can use this to your advantage when an atmosphere has multiple cells with the same properties. If your atmosphere is completely heterogeneous however, consider removing this option (searching for identical cells is a waste of time)."""
        self.memory_aware = memory_aware
        """Divide the computation of opacities to fit into memory."""
        self.per_angle = per_angle
        """Divide the computation along azimuthal angles of the rays grid."""
        self.wn_contribution = self.wn_to_integral
        """Pointer to function to use for contribution by wns (by default computes integral, but can be set to compute transmittance by setting it to wn_to_transmittance)."""
        self.dim = None
        """For internal use only. Determines on which dimension the optical depth is computed (radial/angular dimension(s)). (0,1) will iterate over both.
        """
        self.shape = None
        """For internal use only. Shape of the transmittance (without the spectral dimension)."""
        self.size = None
        """For internal use only. Length of cross-sections)."""
        self.rays = init_rays(rays)
        """Light rays characteristics. See :class:`~pytmosph3r.rays.Rays`."""
        self.model = None

    def default_values(self):
        if self.model.parallel and self.model.parallel.dimension == "rays":
            self.per_angle = False
        if not getattr(self, "per_angle", None):
            self.per_angle = None
        if not hasattr(self, "memory_aware"):
            self.memory_aware = None
        if not hasattr(self, "identical"):
            self.identical = None
        if self.memory_aware is None:
            if not self.per_angle:
                self.memory_aware = True
        if not hasattr(self, "identical") or self.identical is None:
            self.identical = True
            if self.model.filename is not None:
                self.identical = False
        if self.model.opacity.doppler:
            if self.identical:
                self.warning("Disabling 'identical' optimization with doppler (we need to compute the Doppler shift for all atmospheric cells.")
            self.identical = False
        self.debug("memory_aware = %s ; identical = %s ; per_angle = %s" % (self.memory_aware, self.identical, self.per_angle))

    def build(self, model):
        """Builds an atmospheric grid based on altitude coordinates. See :class:`~pytmosph3r.atmosphere.AltitudeAtmosphere`.
        """
        self.model = model
        model.input_atmosphere.build(model)
        model.input_atmosphere.compute_altitude()
        model.atmosphere = AltitudeAtmosphere(model)
        model.atmosphere.build()

        if self.rays is None:
            self.rays = Rays() # default values
        elif not isinstance(self.rays, Rays):
            self.rays = Rays(grid=self.rays)
        self.rays.build(model)

    @property
    def opacity(self):
        return self.model.opacity

    @property
    def atmosphere(self):
        return self.model.atmosphere

    @timer
    def prepare_opacities(self, *args, **kwargs):
        """Prepares opacities list that need to be computed by exo_k.
        Cells with the same physical properties are grouped together to compute their opacity only once.
        Timed function. Use :func:`_prepare_opacities` if time is not needed.
        """
        return self._prepare_opacities(*args, **kwargs)

    def _prepare_opacities(self, opacity_coords):
        """Prepares opacities list that need to be computed by exo_k.
        Cells with the same physical properties are grouped together to compute their opacity only once.
        """
        self.opacity_indices = np.full(self.atmosphere.shape, -1, dtype='i')
        """To get opacity index fast"""

        # Initialization of data
        self.size = len(opacity_coords)
        cell_log_p = np.full((self.size), np.nan)
        cell_temperature = np.full((self.size), np.nan)
        cell_winds = np.full((self.size, 3), np.nan)
        cell_gas_vmr = {}
        aer_reff_densities = None
        for gas in self.atmosphere.gas_mix_ratio.keys():
            if not isinstance(self.atmosphere.gas_mix_ratio[gas], (float, str)):
                cell_gas_vmr[gas] = np.full((self.size), np.nan)
        prepare_aerosols = PrepareAerosols(self.model, self.atmosphere, self.size)

        indices = {}
        for i, coordinates in enumerate(opacity_coords.keys()):
            self.opacity_indices[coordinates] = i

            cell_log_p[i] = np.log10(self.atmosphere.pressure[coordinates])
            cell_temperature[i] = self.atmosphere.temperature[coordinates]
            for gas in self.atmosphere.gas_mix_ratio.keys():
                if isinstance(self.atmosphere.gas_mix_ratio[gas], (float, str)):
                    cell_gas_vmr[gas] = self.atmosphere.gas_mix_ratio[gas]
                else:
                    cell_gas_vmr[gas][i] = self.atmosphere.gas_mix_ratio[gas][coordinates]

            if self.identical:
                gas_values = np.asarray([gas for gas in list(cell_gas_vmr.values()) if isinstance(gas, np.ndarray)])
                if len(gas_values):
                    key = (cell_log_p[i],cell_temperature[i], *gas_values[:, i])
                else:
                    key = (cell_log_p[i],cell_temperature[i])
                if key not in indices:
                    indices[key] = []
                indices[key] += [i]

            aer_reff_densities = prepare_aerosols.compute(i, coordinates)
            cell_winds[i] = self.atmosphere.winds[coordinates]

        if self.identical:
            self.debug("Computing %s out of %s"% (len(indices), len(opacity_coords)))
            if len(indices) == len(opacity_coords):
                self.warning("`identical` option useless. Maybe remove it next time? Your atmosphere is completely heterogeneous so we can't find identical cells.")
        else:
            indices = cell_log_p, cell_temperature, cell_gas_vmr

        self.n_opacities += len(indices)
        return indices, aer_reff_densities, cell_gas_vmr, cell_winds, opacity_coords

    @timer
    def compute_integral(self, *args, **kwargs):
        """Computes integral by iterating over opacities given by :func:`prepate_opacities` and if :attr:`memory_aware`, use :func:`wn_chunks` to subdivide the work along the spectral axis.
         Timed function. Use :func:`compute_contribution` if time is not needed.
        """
        return self.compute_contribution(*args, **kwargs)

    def compute_contribution(self, opacities, wn_chunks=None):
        """Computes integral by iterating over :attr:`opacities` given by :func:`prepate_opacities` for :attr:`wn_chunks` spectral ranges if specified, else if :attr:`memory_aware`, subdivide the spectral axis using :func:`wn_chunks`.

        Args:
            opacities (tuple) : Tuple containing a list of data points for which we compute the absorption, formed like this: ((P,T,X), A, X, C), where P is the pressure, T the temperature, X the VMR, A the aerosols reff densities (see :class:`~pytmosph3r.aerosols.PrepareAerosols`), and C the coordinates (z,lat,lon) of the point. The first tuple (P,T,X) should be unique, and is stored slightly differently in the :attr:`identical` case (hence the separation/redundancy), but that could be changed in future developments.
        """
        cells = opacities[0]
        aer_reff_densities = opacities[1]
        cell_gas_vmr = opacities[2]
        winds = opacities[3]
        coords = opacities[-1]

        # unpack data from prepare_opacities()
        if self.identical:
            data = np.asarray(list(cells.keys())).T
            log_p = data[0]
            temperature = data[1]
            gas_vmr = cell_gas_vmr.copy()
            for i, gas in enumerate([gas for gas, vmr in list(cell_gas_vmr.items()) if isinstance(vmr, np.ndarray)]):
                gas_vmr[gas] = data[i+2]
        else:
            log_p = cells[0]
            temperature = cells[1]
            gas_vmr = cells[2]

        if self.model.parallel and self.model.parallel.dimension == "spectral":
            integrals = self.model.parallel.compute_integral(self, cells, log_p, temperature, gas_vmr, aer_reff_densities, winds, coords)
        else:
            integrals = []
            if wn_chunks is None:
                wn_chunks = self.wn_chunks(len(log_p))

            # iterate over chunks of wavelengths that fit into memory
            for wn_chunk in wn_chunks:
                chunk_integral = self.wn_contribution(cells, log_p, temperature, gas_vmr, aer_reff_densities, winds, coords, wn_range=wn_chunk)
                integrals.append(chunk_integral)

        try:
            # concatenate all wavelengths back together
            integral = np.concatenate(integrals)
            return integral
        except:
            return integrals


    def wn_chunks(self, nb_xsec):
        """Subdivides the work along the spectral axis.
        Useful when cross sections + transmittance are too large to fit into memory.

        Args:
            nb_xsec (int): Size of the cross-sections array (opacities) to compute.
        """
        transmittance_shape = self.shape + (self.opacity.k_data.Nw, )
        xsec_shape = (nb_xsec, self.opacity.k_data.Nw)
        if self.opacity.k_data.Ng:
            xsec_shape += (self.opacity.k_data.Ng, )

        wn_chunks = [None] # all spectral range by default
        if self.memory_aware:
            mem_total, mem_available = self.available_memory(np.prod(xsec_shape) + np.prod(transmittance_shape), name="Cross section + Transmittance")
            try:
                self.check_memory(np.prod(xsec_shape) + np.prod(transmittance_shape), name="Cross section + Transmittance")
            except MemoryError as e:
                self.warning(str(e))
                nchunks = int(mem_total/(mem_available*MemoryUtils.margin))+1
                wn_chunks = spectral_chunks(self.opacity.k_data, nchunks)

                self.info("Subdividing the work into %s wavelength chunks..."%nchunks)
                new_xsec_shape = (nb_xsec, int(np.ceil(self.opacity.k_data.Nw/nchunks)))
                if self.opacity.k_data.Ng:
                    new_xsec_shape += (self.opacity.k_data.Ng, )
                new_transmittance_shape = self.shape + (self.opacity.k_data.Nw/nchunks, )
                mem_total, mem_available = self.available_memory(np.prod(new_xsec_shape) + np.prod(new_transmittance_shape), name="Cross section + Transmittance")
            self.debug("Transmittance + cross-sections should consume %s GB"%(mem_total/1e9))
        return wn_chunks

    def wn_to_integral(self, *args, **kwargs):
        transmittance = self.wn_to_transmittance(*args, **kwargs)
        return self.transmittance_to_integral(transmittance)

    def wn_to_transmittance(self, indices, *args, **kwargs):
        self.opacity.compute(*args, **kwargs)

        self.cross_section = self.opacity.cross_section
        self.mie_abs_coeff = self.opacity.mie_abs_coeff
        if self.identical:
            self.cross_section = np.empty((self.size,)+self.opacity.cross_section.shape[1:])
            for i, coords in enumerate(indices.values()):
                self.cross_section[coords] = self.opacity.cross_section[i]

        tau = self.compute_optical_depth()

        if self.opacity.k_data.Ng: # correlated-k
            transmittance = np.sum(np.exp(-tau) * self.opacity.k_data.weights, axis=-1)
        else: # cross-section
            transmittance = np.exp(-tau)

        if self.store_transmittance:
            self.transmittance.append(transmittance)
        return transmittance

    def transmittance_to_integral(self, transmittance):
        # r = self.rays.r - self.rays.dz/2
        # self.S = 2.* r * self.rays.dz / self.rays.n_angular
        self.S = 2.* self.rays.r * self.rays.dz / self.rays.n_angular
        S = self.S.reshape((-1,) + (1,)*(transmittance.ndim-1))
        return np.sum((1. - transmittance) * S, axis=tuple(range(transmittance.ndim - 1)))

    def compute_optical_depth(self):
        """Computes tau, the optical depth."""
        # self.info("Optical depth...")
        tau = np.zeros(self.shape+self.cross_section.shape[1:])
        rays_it = self.rays.walk(self.dim)
        rays_list = []
        for ray in rays_it:
            rays_list.append(ray) # convert to list for numba
        if self.dim == (-1, ):
            rays_list = range(len(self.rays.rays_lengths))
        rays_list = np.array(rays_list).flatten()
        if isinstance(self.rays.rays_lengths, list):
            rays_lengths = make_array(self.rays.rays_lengths)
            n_intersection = rays_lengths.shape[1]
        else:
            angle_idx = self.rays.angle_idx if self.per_angle and "angle_idx" in self.  rays.__dict__ else -1
            n_intersection = self.rays.rays_lengths.shape[2]
            rays_lengths = self.rays.rays_lengths
            if angle_idx > -1:
                rays_lengths = self.rays.rays_lengths[:, angle_idx]
        if not self.per_angle:
            rays_list = [r for r in range(self.rays.n_radial)]
            for i in range(self.rays.n_angular):
                if self.mie_abs_coeff is not None:
                    compute_optical_depth_mie(self.atmosphere.pressure, self.atmosphere.temperature, rays_lengths[:, i], self.cross_section, self.mie_abs_coeff, self.opacity_indices, rays_list, len(rays_list), n_intersection, tau[:, i])
                else:
                    compute_optical_depth(self.atmosphere.pressure, self.atmosphere.temperature, rays_lengths[:, i], self.cross_section, self.opacity_indices, rays_list, len(rays_list), n_intersection, tau[:, i])
        else:
            if self.mie_abs_coeff is not None:
                compute_optical_depth_mie(self.atmosphere.pressure, self.atmosphere.temperature, rays_lengths, self.cross_section, self.mie_abs_coeff, self.opacity_indices, rays_list, len(rays_list), n_intersection, tau)
            else:
                compute_optical_depth(self.atmosphere.pressure, self.atmosphere.temperature, rays_lengths, self.cross_section, self.opacity_indices, rays_list, len(rays_list), n_intersection, tau)
        return tau

    def angle_to_integral(self, **kwargs):
        self.n_opacities = 0
        self.rays.opacity_coords = {} # dictionary by coordinates for computing opacity
        if self.store_transmittance:
            self.transmittance = []
        self.rays.compute_sub_rays_angle()
        opacities = self._prepare_opacities(self.rays.opacity_coords)
        integral_angle = self.compute_contribution(opacities, **kwargs)

        # free some memory just in case
        del self.rays.opacity_coords

        return integral_angle

    def grid_to_transmittance(self, bounds=None):
        """Computes transmittance for rays between bounds.

        Args:
            bounds (tuple): Must be ((r_s,r_e), (a_s,a_e)), where r_s and r_e are the radial start and end points, and a_s and a_e the angular ones.
        """
        self.per_angle = False
        self.dim = (-1, )
        self.rays.rays_indices = []
        self.rays.rays_lengths = []
        self.rays.compute_sub_rays(bounds)
        self.shape = (len(self.rays.rays_indices), )
        opacities = self._prepare_opacities(self.rays.opacity_coords)
        self.wn_contribution = self.wn_to_transmittance # compute only transmittance in this mode
        transmittance = self.compute_contribution(opacities)
        return transmittance

    def compute(self, model, **kwargs):
        """Sums all optical depths and computes the transit depth (ratio of visible radius of the planet on the radius of the star to the square :math:`(R_P/R_S)^2`).

        Returns:
            Spectrum (exo_k object): Spectrum :math:`(R_P/R_S)^2`
        """
        self.debug("Real Memory before transit depth = %s"% memory_usage())
        self.debug("Virt Memory before transit depth = %s"% memory_usage("VmH"))
        if model.parallel:
            model = model.parallel.synchronize(model) # get model from P0
        self.model = model
        if self.__class__.__name__ in ("Lightcurve",):
            self.rays = model.lightcurve.rays # sync for parallel
        else:
            self.rays = model.transmission.rays # sync for parallel

        self.n_opacities = 0
        self.dim = (0,)
        self.shape = (self.rays.shape[0],)

        self.default_values()

        self.rays.init_subrays()
        if self.store_transmittance:
            self.transmittance = []

        if self.model.parallel and not self.model.parallel.dimension == "spectral":
            integral = self.model.parallel.compute_integral(self)
            if self.per_angle:
                integral = np.sum(integral, axis=0)
        elif self.per_angle:
            integrals = []
            transmittance = []
            for self.rays.angle_idx, ray_angle in enumerate(tqdm(self.rays.angles, leave=False)):
                integrals.append(self.angle_to_integral(**kwargs))
                if self.store_transmittance:
                    try:
                        transmittance.append(np.concatenate(self.transmittance, axis=-1)) # get transmittance wavelengths chunks
                    except:
                        pass # parallel version doesn't support transmittance yet
            integral = np.sum(integrals, axis=0)
            if self.store_transmittance:
                try:
                    self.transmittance = np.transpose(np.array(transmittance), [1,0,2])
                except:
                    pass # parallel version doesn't support transmittance yet
        else:
            self.dim = (0,1)
            self.shape = self.rays.shape
            self.rays.compute_sub_rays()
            self.info("Preparing opacities of %s cells..."%len(self.rays.opacity_coords))
            opacities = self.prepare_opacities(self.rays.opacity_coords)
            self.info("Computing opacities...")
            integral = self.compute_integral(opacities, **kwargs)
            if self.store_transmittance:
                try:
                    self.transmittance = np.concatenate(self.transmittance, axis=-1)
                except:
                    pass # parallel version doesn't support transmittance yet

        if self.model.parallel and self.model.parallel.rk:
            return # Only proc 0 needs to compute the rest

        self.debug("Real Memory after transit depth = %s"% memory_usage())
        self.debug("Virt Memory after transit depth = %s"% memory_usage("VmH"))
        self.debug("Number of opacities computed: %s"%self.n_opacities)

        value = ((self.rays.Rp**2.) + integral)/(self.rays.Rs**2)
        self.spectrum = xk.Spectrum(value, wns=self.opacity.k_data.wns, wnedges=self.opacity.k_data.wnedges)
        return self.spectrum

    def outputs(self):
        outputs= ["n_opacities", "spectrum"]
        if self.store_transmittance:
            outputs +=  ["transmittance"]
        try:
            assert self.model.parallel is not None
            return outputs
        except:
            return outputs + ["rays"]
