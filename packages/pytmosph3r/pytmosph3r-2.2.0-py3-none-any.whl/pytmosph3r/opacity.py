from typing import Optional, List, Tuple

import astropy.units as u
import exo_k as xk
from exo_k.util.cst import C_LUM
import numpy as np
import scipy as sp
from exo_k.util.spectral_object import Spectral_object

from pytmosph3r.log import Logger

# DopplerParam = TypedDict('DopplerParam', {'Kp': float, 'phi': float, 'wind': bool, 'omega': float})


class Opacity(Logger, Spectral_object):
    """This module is the (main) link between pytmosph3r and exo_k. It will load the gas databases (:func:`load_gas_database`), and compute the opacities (:func:`compute`) of a list of cells of the atmosphere (using their physical properties: P, T, etc).
    """
    _remove_zeros = True # for exo_k

    def __init__(self, rayleigh: bool = False, cia: Optional[List[str]] = None,
                 wn_range: Optional[Tuple[float, float]] = None, k_data=None,
                 doppler=None):
        """The parameters of the Opacity module are:

        Args:
            rayleigh (bool, optional): Activates Rayleigh. Defaults to None.
            cia (list, optional): List of molecules for which to compute Collision Induced Absorption. Defaults to None. Example: :code:`['H2','He']`.
            wn_range (tuple, optional): Range (wn_min, wn_max) of wave numbers to select for the computations. Defaults to None.
            k_data (exo_k.Kdatabase, optional): Exo_k object containing the gas database (especially useful if you will run multiple models, with the same data). Defaults to None.
            cia_data (exo_k.Kdatabase, optional): Exo_k object containing the CIA database (especially useful if you will run multiple models, with the same data). Defaults to None.
        """
        super().__init__(self.__class__.__name__)

        self.rayleigh = rayleigh
        """Activate Rayleigh (by default, it is deactivated)."""
        self.doppler = doppler
        """Activate Doppler (by default, it is deactivated). Dictionary containing 'Kp' and 'phi' values. TODO
        """
        self.wn_range: Optional[Tuple[float, float]] = wn_range
        if hasattr(wn_range, "__len__") and not len(wn_range) and len(wn_range) != 2:
            self.wn_range = None  # empty range
        """Range (wn_min, wn_max) of wave numbers to select for the computations."""

        self.cia = cia
        """List of molecules to look for when computing CIA pairs."""

        self.k_data: Optional[xk.Kdatabase] = k_data

    @classmethod
    @u.quantity_input(w_range='wavenumber', equivalencies=u.spectral())
    def fromQuantity(cls, rayleigh: bool = False, cia: Optional[List] = None,
                     w_range: Optional[List] = None):
        """
        Create an `Opacity` object using astropy quantity for wn_range.

        Args:
            rayleigh (bool):
            cia (List[str]):
            w_range (List[Quantity]): Range of quantity to determine (wn_min, wn_max) ie wn_range

        Returns:
            Opacity
        """
        wn_range: Optional[List] = None

        if w_range is not None:
            wn_range = np.sort(w_range.to_value(u.Unit('cm-1'), equivalencies=u.spectral())).tolist()  # noqa

        return cls(rayleigh=rayleigh, cia=cia, wn_range=wn_range)

    def load_gas_database(self, model):
        """Loading :class:`exo_k` gas/CIA/aerosols databases,
        and potentially clip the spectral range.
        """
        self.model = model
        atm = self.model.input_atmosphere
        if not (model.transmission or model.lightcurve):
            atm = self.model.emission_atmosphere
        self.aerosols = atm.aerosols

        # check if there is a background gas
        background = False
        for gas, value in atm.gas_mix_ratio.items():
            if isinstance(value, str) and value == 'background':
                background = True
        if not background:
            self.warning("No background gas given.")

        # Remove gases treated as transparent from the ones treated as visible.
        self.visible_gases = list(atm.gas_mix_ratio.keys())
        transparent_gases = atm.transparent_gases
        if isinstance(transparent_gases, str):
            self.visible_gases.remove(transparent_gases) # only one gas
        else:
            if atm.transparent_gases is not None:
                for gas in atm.transparent_gases:
                    try:
                        self.visible_gases.remove(gas)
                    except:
                        pass

        # Load k_data for the visible gases
        if self.k_data is not None and 'total' in self.k_data.molecules:
            self.warning(f"Database already loaded. Using a single molecule named `total` in place of "
                         f"`self.visible_gases`")
        elif self.k_data is not None and self.k_data.molecules is not None and self.visible_gases is not None and set(self.visible_gases).issubset(set(self.k_data.molecules)):
            self.warning("Database already loaded. If you want to load another, set opacity.k_data to None.")
        else:
            self.info("Exo_k: Loading gas database for %s... (%s considered transparent)"%(self.visible_gases, transparent_gases))
            self.k_data = xk.Kdatabase(self.visible_gases, remove_zeros=self._remove_zeros)

        # Load CIA data
        self.cia_data = None
        if len(self.visible_gases):
            self.k_data.clip_spectral_range(self.wn_range)
            if self.cia is not None and not False and hasattr(self.cia, "__len__") and len(self.cia):
                self.info("Exo_k: Loading CIA database for %s..."%(self.cia))
                self.cia_data = xk.CIAdatabase(molecules=self.cia)
                self.cia_data.sample(wngrid=self.k_data.wns)

        # Load aerosols data
        self.aerosol_data: Optional[xk.Adatabase] = None

        if self.aerosols is None or self.aerosols == []:
            self.info(f"Exo_k: No aerosols to load.")
        else:

            self.info(f"Exo_k: Loading aerosols database for {list(self.aerosols.keys())}...")

            aerosol_files: List[str] = []
            for aerosol_name,aerosol_val in self.aerosols.items():
                if isinstance(aerosol_val, dict) and 'optical_properties' in aerosol_val:
                    aerosol_files.append(aerosol_val['optical_properties'])
                else:
                    try:
                        aerosol_files.append(model.aerosol(aerosol_name))
                    except:
                        raise KeyError(
                            f"Please provide 'optical_properties' for aerosol '{aerosol_name}', i.e., the name of the "
                            f"file in 'aerosol_path' ({xk.Settings().search_path['aerosol']}) which contains the data "
                            f"associated with '{aerosol_name}'.")

            if len(aerosol_files) != 0:
                self.debug(f'Aerosols files to send to Adatabase: {aerosol_files}')
                self.aerosol_data = xk.Adatabase(filenames=aerosol_files)

                self.aerosol_data.sample(wngrid=self.k_data.wns)

        self.gas_mix = xk.Gas_mix(k_database=self.k_data, cia_database=self.cia_data)

        self.info("Exo_k: loading databases - DONE")

    def compute(self, log_p, temperature, gas_vmr, aer_reff_densities, winds, coords, wn_range):
        """Compute the opacities for a list of cells of the atmosphere.

        Args:
            log_p (ndarray): Log10(pressure) of each cell
            temperature (ndarray): Temperature of each cell
            gas_vmr (ndarray): gas dictionary (:code:`{gas_name: VMR}`) of each cell
            aer_reff_densities (ndarray): Aerosol data of each cell (see :class:`~pytmosph3r.aerosols.PrepareAerosols`)
            winds (ndarray): Winds (u,v,w) of each cell
            coords (ndarray): Coordinates (z,lat,lon) of each cell
            wn_range (ndarray): Wavenumber range to consider
        """
        self.cross_section = self.gas_mix.cross_section(composition=gas_vmr, logp_array=log_p, t_array=temperature, rayleigh=self.rayleigh, wn_range=wn_range)

        if self.aerosols:
            self.mie_abs_coeff = self.aerosol_data.absorption_coefficient(aer_reff_densities)
            if self.k_data.Ng:
                # homogenize the shapes of mie coeff and cross sections
                self.mie_abs_coeff = self.mie_abs_coeff[..., None] * np.ones(self.k_data.Ng)
        else:
            self.mie_abs_coeff = None

        if self.doppler:
            #theta_v = self.model.observer.latitude+np.pi/2.  # if Wardenier2021
            # warning: phi_v depends on the GCM longitude definition.
            # could be read from model.observer
            phi_v = 0. #np.pi #self.model.observer.longitude
            R0 = self.model.planet.radius
            c = np.asarray(list(coords.keys()))
            altitudes = self.model.atmosphere.altitude[c[:,0]]
            latitudes = self.model.atmosphere.latitudes[c[:,1]]  #-np.pi/2  # if Wardenier2021
            longitudes = self.model.atmosphere.longitudes[c[:,2]]

            if self.doppler['wind'] == True:

                for i, (u,v,w) in enumerate(winds):

                    theta = latitudes[i]
                    phi = longitudes[i]
                    z = altitudes[i]

                    # Wardenier2021
                    #v_los = u*np.sin(theta_v)*np.sin(phi-phi_v)\
                    #        + (v*np.cos(theta)-w*np.sin(theta))*np.sin(theta_v)*np.cos(phi-phi_v)\
                    #        - (v*np.sin(theta)+w*np.cos(theta))*np.cos(theta_v)\
                    #        + self.doppler['omega']*(R0+z)*np.sin(theta)*np.sin(theta_v)*np.sin(phi-phi_v)
                    
                    # Harada2021        
                    v_los = - u*np.sin(phi+phi_v)\
                            - v*np.cos(phi+phi_v)*np.sin(theta)\
                            + w*np.cos(phi+phi_v)*np.cos(theta)\
                            - self.doppler['omega']*(R0+z)*np.sin(phi+phi_v)*np.cos(theta)

                    shifted_wns = self.gas_mix.wns.copy()/(1 - v_los / C_LUM ) # To do doppler shift

                    if self.cross_section[i].ndim>1:
                        doppler_cross_section = sp.interpolate.interp2d(self.k_data.ggrid, self.gas_mix.wns, self.cross_section[i][...])(self.k_data.ggrid, shifted_wns) # TODO: could this be faster?
                    else:
                        doppler_cross_section = np.interp(shifted_wns, self.gas_mix.wns, fp=self.cross_section[i])
                    self.cross_section[i] = doppler_cross_section

            else:

                for i in range(len(altitudes)):

                    theta = latitudes[i]
                    phi = longitudes[i]
                    z = altitudes[i]

                    v_los = -self.doppler['omega']*(R0+z)*np.sin(phi+phi_v)*np.cos(theta)

                    shifted_wns = self.gas_mix.wns.copy()/(1 - v_los / C_LUM ) # To do doppler shift

                    doppler_cross_section = np.interp(shifted_wns, self.gas_mix.wns, fp=self.cross_section[i])
                    self.cross_section[i] = doppler_cross_section

        return self.cross_section, self.mie_abs_coeff

    @property
    def wns(self):
        return self.k_data.wns
    @property
    def wnedges(self):
        return self.k_data.wnedges

    def outputs(self):
        return ['wns', 'wnedges'] # Opacity is usually called multiple times so an output would be useless here
