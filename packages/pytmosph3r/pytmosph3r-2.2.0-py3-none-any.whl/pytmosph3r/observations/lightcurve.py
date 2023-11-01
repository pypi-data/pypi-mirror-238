import astropy.units as u
import numpy as np
from exo_k.util.spectral_object import Spectral_object
from scipy.interpolate import CubicSpline
from tqdm.auto import tqdm

from pytmosph3r.log import Logger
from pytmosph3r.util.geometry import CircleIntersection, integrate_circles_intersections, intersection_circles
from pytmosph3r.util.util import get_wls, merge_attrs, to_SI
from .transmission import Transmission
from ..rays import init_rays


class Lightcurve(Transmission, CircleIntersection, Spectral_object):
    """The lightcurve model calculates the transit depth :math:`(R_P/R_S)^2` for all phases of the transit via :func:`compute`.
    It is possible to take into account the tidally-locked rotation of the planet.

    .. note:: :attr:`rotate` will be considerably slower since we have to recompute the transmittance for all phases.
    :func:`partial_transit` calculates the intersection of the transmittance maps (or rays opacities) with the star.
    """
    def __init__(self, rotate=None,  n_transmittances=None, n_phases=None, n_egress=None, phases=None, times=None, start_egress=None, end_egress=None, wns=None, wls=None, atmosphere_only=False, store_transmittances=None, transmittance_surfaces=None, rays=None, **kwargs):
        """The parameters of the lightcurve model are below.


        Args:
            rotate (bool) : Activates the planet rotation (tidally-locked) during transit (requires recomputing of the whole transmittance at each phase, so this option is deactivated by default). If False, we simply use the default transmittance map for all phases (decided by the longitude of the Observer).
            
            n_phases (int) : Total number of phases to calculate (not used if :attr:`phases` is given). Defaults to 30.
            
            n_egress (int) : Number of phases during partial transit (ingress+egress).  'auto' will set it to 2/3 of :attr:`n_phases`.
            
            phases (array, float) : List of phases (in :math:`rad` or astropy units). Overwrites :attr:`n_phases`.

            times (array, float) : List of timesteps (in :math:`s` or astropy units). Needs the orbital period to be set (see :class:`~pytmosh3r.orbit.Orbit`). Overwrites :attr:`phases` and :attr:`n_phases`.
            
            n_transmittances (int) : Number of phases for which to effectively compute the transmittance (the rest will be interpolated). WARNING: a larger number will considerably be slower (same reasons as for :attr:`rotate`).
            
            wns (array, float) : NOT USED FOR NOW. Use `~pytmosph3r.opacity.Opacity.wn_range` instead. List of wavenumbers for which to calculate the lightcurve. Wavenumbers (in :math:`cm^{-1}`) for which to compute lightcurves.  Defaults to the full list of wavenumbers of the input data.
            
            wls (array, float) : NOT USED FOR NOW. Wavelengths (in :math:`\mu m`) for which to compute lightcurves.
            
            atmosphere_only (bool) : Outputs the effect of the atmosphere only (without the planet core radius), useful mainly for debugging and checking the signal of the atmosphere.
        """
        Logger.__init__(self, self.__class__.__name__)
        self.limb_darkening = None
        self.rotate = rotate
        self.n_transmittances = n_transmittances
        self.n_phases = n_phases
        self.n_egress = n_egress
        self.phases = to_SI(phases, u.rad)
        self._times = to_SI(times, u.s)
        if isinstance(start_egress, u.Quantity) and start_egress.si.unit == "rad":
            self.start_egress = to_SI(start_egress, u.rad)
        else:  # we'll handle conversion later, once we know period
            self.start_egress = start_egress
        if isinstance(end_egress, u.Quantity) and end_egress.si.unit == "rad":
            self.end_egress = to_SI(end_egress, u.rad)
        else:  # we'll handle conversion later, once we know period
            self.end_egress = end_egress

        self.wns = wns
        if wns is not None:
            self.wns = np.asarray(wns)
        if wls is not None:
            self.wns = np.sort(10000/np.array(wls))
        self.atmosphere_only = atmosphere_only
        self.store_transmittance = True
        """Store transmittance in Transmission()."""
        self.store_transmittances = store_transmittances
        """Store the list of rays_opacities in (in particular when :attr:`rotate` is used)."""
        if Logger.verbose:
            self.store_transmittances = True
        self.transmittance_surfaces = transmittance_surfaces
        self.transmittance_phases = None 
        
        self.wn_contribution = self.wn_to_integral # TODO: check if we could do sth else here
        self.per_angle = True # TODO: check if we could do sth else here
        for key, value in kwargs.items():
            self.__dict__[key] = value # parameters for Transmission

        # calculated by module
        self._dist = None
        self.model = None
        self._rays = None
        self._orbit = None
        self._sma = None
        self._inclination = None
        self.rays = init_rays(rays)

        self.flux = None
        """Main output of the module. (Rp/Rs)**2 for all :attr:`phases`."""

    @property
    def n_in_star(self):
        """Number of phases during full transit (equal to :attr:`n_phases` - :attr:`n_egress`).
        """
        try:
            return self.n_phases - self.n_egress*2
        except:
            return None

    @property
    def times(self):
        if self.phases is not None and self.orbit is not None and self.orbit.period is not None:
            if isinstance(self.phases, (list,)):  # maybe do this more globally
                self.phases = np.asarray(self.phases)
            self._times = self.orbit.time(self.phases)
        return self._times

    @times.setter
    def times(self, value):
        self._times = to_SI(value, u.s)

    @property
    def end_transit(self):
        """Returns phase corresponding to the end of the transit (simulation is completely out of the star."""
        try:
            Rs = self.model.star.radius
            Ra = (self.model.planet.radius+self.model.atmosphere.max_altitude)
            return np.arcsin((Rs+Ra)/self.sma)
        except Exception as e:
            self.debug("Can't compute end of transit. Full error:\n{e}")
            return None

    def build(self, model):
        self.model = model
        # Get transmission parameters...
        t = model.transmission
        if t is not None: # ... from transmission object if computed
            self = merge_attrs(self, t)
        else: # ... by recomputing them otherwise
            super().build(model)
        
        if self.wns is not None and self.model.opacity is not None and self.model.opacity.wn_range is not None:
            self.wns = np.unique(np.clip(self.wns, *self.model.opacity.wn_range))
        
        self.default_values()

    def default_values(self):
        """Set default values. Called by :func:`~pytmosph3r.transmission.Transmission.compute()`."""
        super().default_values()

        if self.inclination is None:
            self.inclination = 0 # equator by default

        # convert times to phases
        if self.times is not None and self.orbit is not None:
            self.phases = self.orbit.phase(self.times)
        if isinstance(self.start_egress, u.Quantity) and self.star_egress.si.unit == "s":
            self.start_egress = self.orbit.phase(to_SI(self.start_egress))
        if isinstance(self.end_egress, u.Quantity) and self.end_egress.si.unit == "s":
            self.end_egress = self.orbit.phase(to_SI(self.end_egress))

        if self.phases is not None:
            if isinstance(self.phases, (int, float)):
                self.phases=[self.phases] # handle one phase case
            self.phases = to_SI(self.phases, u.rad)
            assert hasattr(self.phases, "__len__"), "Phases should be given as a list or array."
            self.debug("You have set a list of 'phases', so 'n_phases' is ignored.")
            self.n_phases = len(self.phases)
        if self.n_phases is None:
            self.n_phases = 30
            self.n_egress = 10
        if self.n_egress == 'auto' or self.n_egress is None:
            self.n_egress = int(1/3*self.n_phases)
        self.n_phases = int(self.n_phases)
        self.n_egress = int(self.n_egress)
        assert self.n_phases > self.n_egress, "Total number of phases should be larger than phases in partial transit."
        
        if self.phases is None:
            Rp = self.model.planet.radius
            # Radius of planet + atmosphere (with a bit of margin)
            Ra = Rp+self.model.atmosphere.max_altitude * 1.2
            Rs = self.model.star.radius
            # End of partial transit (including all the atmosphere)
            if self.start_egress is None:
                try:
                    self.start_egress = np.arcsin((Rs-Ra)/self.sma)
                except Exception as e:
                    raise AttributeError(f"No orbital semi-major axis. Please provide it in Orbit(). Full error:\n{e}")
            else:
                self.start_egress = to_SI(self.start_egress, u.rad)
            if self.end_egress is None:
                self.end_egress = np.arcsin((Rs+Ra)/self.sma)
            else:
                self.end_egress = to_SI(self.end_egress, u.rad)

            if isinstance(self.n_egress, (int)):
                egress = np.linspace(self.start_egress, self.end_egress, int(self.n_egress))
                mid = np.linspace(-self.start_egress, self.start_egress, self.n_in_star+2)[1:-1]
                self.phases = np.concatenate([-egress[::-1], mid, egress])
            else:
                self.phases = np.linspace(-self.end_egress, self.end_egress, self.n_phases)
                
        elif self.rotate and self.n_transmittances is None:
            # transmittance phases defined by user (equal to phases)
            self.transmittance_phases = self.phases
            
        # if self.n_transmittances == 1: # defined later, once self.model has been set
        #     phase = self.model.orbit.phase_from_observer(self.model.observer.coordinates)
        #     self.transmittance_phases = [phase]

        if self.n_transmittances is None:
            if self.rotate:
                self.n_transmittances = self.n_phases
            else:
                self.n_transmittances = 1 # self.transmittance_phases is defined later
        self.n_transmittances = int(self.n_transmittances)

        if self.rotate is None and self.n_transmittances > 1:
            self.rotate = True

        if self.transmittance_phases is None and self.rotate:
            # transmittance phases defined automatically
            self.transmittance_phases = np.linspace(-self.end_egress, self.end_egress, self.n_transmittances)

        if self.transmittance_surfaces is None:
            try:
                rays = self.rays
            except:
                rays = self.model.rays
            if rays.n_angular < 100:
                # to be more precise
                self.transmittance_surfaces = True

    def star_rays_opacity(self, phase, rays_opacity, Rs=None):
        """Returns the rays opacities to the star flux (using star radius), and the distance of each ray to the edge of the star ( negative values are 'inside' the star).

        Args:
            phase (float): Phase to calculate star opacity for.
            opacity (array): Original rays opacity at this phase.
            Rs (optional): Star radius

        Returns:
            tuple: opacity, distance to star edge (both (N_r x N_a))
        """
        if Rs is None:
            Rs = self.model.star.radius
        res = rays_opacity
        res = rays_opacity.copy() # we will need it again later
        res[np.where(self.dist(phase) > Rs)] = 0 # outside the star
        return res, self.dist()

    # @profile
    def partial_transit(self, phase, rays_opacity):
        """Computes the value of the spectrum when the planet is partially (or completely) in front of the star, using :func:`~pytmosph3r.util.geometry.CircleIntersection.intersections`.

        Args:
            phase (float): phase

        Returns:
            array: rays_opacity (N_r x N_a)
        """
        rays = self.rays
        Rs = self.model.star.radius
        rS, aS = self.orbit.star_coordinates_projected(phase)
        Ra = (self.model.planet.radius+self.model.atmosphere.max_altitude)
        max_phase = np.arcsin((Rs+Ra)/self.sma)
        if (phase > max_phase or phase < -max_phase): # outside star
            return np.zeros((rays_opacity.shape[-1])) # transparent

        ld = 1
        if self.limb_darkening is not None:
            # TODO limb darkening not properly done. Should be integrated for each ray
            ds = self.dist(phase)/Rs
            ld = self.limb_darkening.compute(ds)
            ld_func, ld_coeffs = self.limb_darkening.get_func()
        if self.transmittance_surfaces:
            surfaces = self.intersections(phase, star=self.model.star)
            integral = np.tensordot(rays_opacity, surfaces*ld, axes=([0,1],[0,1]))
            # is opt_einsum faster?
        else:
            star_rays_opacity, ds = self.star_rays_opacity(phase, rays_opacity)
            surfaces = (2.* np.pi* rays.r * rays.dz / rays.n_angular)
            integral = np.sum(np.tensordot(star_rays_opacity, surfaces*ld, axes=([0],[0])), axis=0)
        value = (integral)/(np.pi*Rs**2)
        if self.limb_darkening is not None:
            core_integral = integrate_circles_intersections(rS, Rs, rays.Rp, ld_func, ld_coeffs)/(np.pi*Rs**2)
        else:
            core_integral = intersection_circles(rS, Rs, rays.Rp)/(np.pi*Rs**2)

        value += core_integral
        if self.atmosphere_only:
            value = ((rays.Rp**2.) + integral)/(np.pi*Rs**2) #
        return value

    def get_spectral_chunks(self, wns):
        """Get spectral chunks corresponding to `wns` in opacity database."""
        self.wns = wns
        wn_chunks = None
        Nw = len(self.opacity.wns)
        if len(self.wns) < Nw:
            wn_chunks = []
            wn_search = np.minimum(self.opacity.wnedges.searchsorted(self.wns)-1, Nw-1)
            # restrict selected wns to actual opacity range
            inside = np.where((wn_search>0)&(wn_search < Nw+1))
            self.wns = self.wns[inside]
            indices = np.maximum(wn_search[inside], 0)
            try:
                start = indices[0]
            except IndexError as e:
                raise IndexError(f"Selected wls or wns NOT with wl_range/wn_range. Full error:\n{e}")
            end = start+1
            i = 0
            while i < len(indices):
                start = indices[i]
                end = start+1
                while i+1 < len(indices) and indices[i+1] <= end:
                    i = i+1
                    end = indices[i]+1
                end = min(end, Nw)

                # complicated bit simply to get right chunk... do better?
                try:
                    start_clip = np.clip(start, 0, Nw-1)
                    pad = np.diff(self.opacity.wnedges[start_clip:start_clip+2])[0]/100
                except:
                    pad = self.opacity.wnedges[start]/100
                first = self.opacity.wnedges[start]-pad
                try:
                    end_clip = np.clip(end, 0, Nw-1)
                    pad = np.diff(self.opacity.wnedges[end_clip:end_clip+2])[0]/100
                except:
                    pad = self.opacity.wnedges[end]/100
                last = self.opacity.wnedges[end]+pad

                wn_chunks.append([first, last])
                i = i+1
        return wn_chunks

    def compute_rays_opacities(self):
        """Compute rays opacities (transmittance) at :attr:`n_transmittances` stages of the transit. These will server as a basis for interpolation in :func:`compute`.
        """
        rays_opacities = []

        # find spectral chunks for which to compute lightcurves
        wn_chunks = self.get_spectral_chunks(self.wns)

        if self.rotate:
            for i in tqdm(range(self.n_transmittances)):
                self.model.observer.position_from_phase(self.transmittance_phases[i])
                super().compute(self.model, wn_chunks=wn_chunks)
                rays_opacity = np.subtract(1, self.transmittance) # subtract actually faster
                rays_opacities.append(rays_opacity)
        else:
            phase = self.model.orbit.phase_from_observer(self.model.observer.coordinates)
            self.transmittance_phases = [phase]
            rays_opacity = None
            if self.model.transmission is not None and hasattr(self.model.transmission, "transmittance"):
                if self.wls is not None and len(self.wls) < len(self.model.wls):
                    rays_opacity = np.subtract(1, get_wls(self.model.transmission.transmittance, self.wls, self.model.spectrum.wls))
                else:
                    rays_opacity = np.subtract(1, self.model.transmission.transmittance)
            else:
                for i in tqdm(range(1)): # display the time
                    super().compute(self.model, wn_chunks=wn_chunks)
                rays_opacity = np.subtract(1, self.transmittance)
            rays_opacities.append(rays_opacity)
        rays_opacities = np.asarray(rays_opacities)
        if self.store_transmittances:
            self.rays_opacities = rays_opacities
        return rays_opacities

    def compute(self, model):
        """Compute the lightcurve. Transmittances are calculated by :func:`compute_rays_opacities` on :attr:`n_transmittances` points and interpolated over :attr:`n_phases`. The surface area of the star covered by the transmittance map is calculated by :func:`~pytmosph3r.util.geometry.CircleIntersection.intersections`.
        """
        if self.wns is None:
            self.wns = model.opacity.k_data.wns
        self.model = model
        rays_opacities = self.compute_rays_opacities()
        self.light_curve = []

        if (self.phases != self.transmittance_phases) and (self.rotate or self.n_transmittances > 1):
            try:
                shape = rays_opacities.shape
                mem_total, mem_available = self.available_memory(4*np.prod(shape))
                self.check_memory(4 * np.prod(shape), name="Transmittance interpolation")  # raise MemoryError

                # no memory problem, we can interpolate
                interp_phases = CubicSpline(self.transmittance_phases, rays_opacities)
                # interp1d is slower and consumes more memory
                n_interp = None
            except MemoryError as e:
                self.warning(str(e))
                n_interp = int(mem_total/(mem_available*self.margin))+1
                chunk_size = len(self.transmittance_phases) / n_interp
                splits = [int(i*chunk_size) for i in range(n_interp+1)]
                split_idx = -1 # to create interpolation function at 1st idx
                split_phases = np.searchsorted(self.transmittance_phases[splits[:-1]], self.phases, 'right')-1

        for i, phase in enumerate(tqdm(self.phases)):
            self.model.observer.position_from_phase(phase)
            if (self.phases == self.transmittance_phases):
                rays_opacity = rays_opacities[i]
            elif (self.rotate or self.n_transmittances > 1) and i > 0:
                # ignore first phase as it coincides
                
                rays_opacity = None
                if i == self.n_phases - 1:
                    # ignore last phase as it coincides
                    # interp_phases = lambda x : rays_opacities[0]
                    rays_opacity = rays_opacities[-1]
                elif n_interp is not None:
                    if split_idx != split_phases[i]:
                        # create an interpolation function on this range
                        split_idx = split_phases[i]
                        interp_range = slice(splits[split_idx],splits[split_idx+1]+1)
                        self.debug(f"Interpolating in {interp_range}")
                        interp_phases = CubicSpline(self.transmittance_phases[interp_range], rays_opacities[interp_range])
                if rays_opacity is None:
                    rays_opacity = interp_phases(phase)
            else:
                rays_opacity = rays_opacities[0]

            value = self.partial_transit(phase, rays_opacity)
            self.light_curve.append(value)
        self.flux = np.asarray(self.light_curve)
        return self.flux

    def inputs(self):
        inputs = Logger.inputs(self)
        if self.model:
            if not self.model.transmission:
                inputs += ["rays"]
        return inputs

    def outputs(self):
        outputs = ['wns', 'flux', 'transmittance_phases', 'rays', 'times']
        if self.store_transmittances:
            # TODO kind of tricky, need to doc this
            outputs+= ["rays_opacities"]
        elif self.store_transmittance and not self.rotate:
            if self.model and not self.model.transmission:
                # could be useful if no rotation?
                outputs +=  ["transmittance"]
        return outputs

