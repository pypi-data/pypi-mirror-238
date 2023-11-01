from typing import Optional, Union

import exo_k as xk
import numpy as np

from pytmosph3r.config.factory import get_class
from pytmosph3r.log import Logger
from pytmosph3r.util.constants import RGP
from .simple2d import Simple2DTemperature, simple_2D_vmr
from ..grid import Grid3D


class Atmosphere(Grid3D):
    """Base class for building atmospheric models."""

    def __init__(self, name):
        Logger.__init__(self, name)

        self.molar_mass = None
        """ Molar mass (in `kg/mol`)."""

        self.model = None

        self.pressure = None
        """Pressure (in `Pa`)."""

        self.max_pressure = None
        """Max (bottom) pressure in the model (in `Pa`). Optional if using an input file."""

        self.min_pressure = None
        """Min (top) pressure in the model (in `Pa`). Optional if using an input file."""

        self.temperature = None
        """Temperature (in `K`)."""

        self.gas_mix_ratio = {}
        """Volume mixing ratios of each gas."""

        self.aerosols = {}
        """Dictionary for aerosols. Each aerosol is itself a dictionary of which each element indicates the
        MMR, the effective radius and the condensate density of the aerosol. """

        self.p_min_aerosols = None
        """For pressures under `p_min_aerosols`, all aerosols MMRs are set to 0."""

        self.recompute_molar_mass = True
        """Recompute molar mass from the gas mix ratios (activated by default) using the method :func:`exo_k.Gas_mix.molar_mass`. If you give Atmosphere() a molar mass, this will be set to False. If you change your mind later, simply set this parameter again to True to recompute it automatically."""

        self.rcp: float = .28
        """Default rcp value to be used in emission mode"""

        self.albedo_surf: Optional[Union[float, np.ndarray]] = None
        self.wn_albedo_cutoff: Optional[Union[float, np.ndarray]] = None

        # Attributes defined by the methods
        self.grid = None
        self.planet = None
        self.chemistry = None
        self.model = None
        self.input_vmr = None
        self.min_input_pressure = None
        self.ps = None
        self.altitude = None
        self.scaleheight = None
        self.gravity = None

    @property
    def n_latitudes(self):
        return self.grid.n_latitudes

    @property
    def n_longitudes(self):
        return self.grid.n_longitudes

    @property
    def n_vertical(self):
        return self.grid.n_vertical

    @n_vertical.setter
    def n_vertical(self, value):
        self.grid.n_vertical = value

    def compute_molar_mass(self):
        """Compute :py:attr:`molar_mass` (`kg/mol`)."""
        self.info("Computing molar mass (Exo_k)...")
        try:
            if not self.recompute_molar_mass and self.molar_mass is not None:
                self.warning("Molar mass will not be recomputed, as it has been given by the user. If you *need* to recompute it from the gas mix, please set recompute_molar_mass to False.")
            else:
                self.molar_mass = xk.Gas_mix(self.gas_mix_ratio).molar_mass()
            if isinstance(self.molar_mass, (float, int)):
                self.molar_mass = np.full(self.shape, self.molar_mass)
        except Exception as e:
            self.critical(e)
            return

    def build(self, model=None):
        """Ensure that all data has been computed and formatted in arrays of the same shape.
        Handle different configurations of pressure, temperature and chemistry.
        """
        if model:
            self.model = model
            self.planet = model.planet

        if self.grid is None:
            raise NameError("Grid is not defined. Please set one in your input.")

        if self.grid.n_vertical is None:
            self.debug(f"Setting input grid n_vertical to {self.model.n_vertical + 1} (nb of levels)")
            self.grid.n_vertical = self.model.n_vertical + 1

        assert self.max_pressure is not None \
               or self.pressure is not None, "You should set an input pressure in the model (either set 'max_pressure' or 'pressure')"

        if self.max_pressure:
            # Define pressure levels using top and bottom bounds
            assert self.min_pressure is not None, "A max pressure has been defined so a min pressure " \
                                                  "should be defined too in order to discretize a linear" \
                                                  " space in-between."
            self.pressure = np.ones(self.shape)
            self.pressure *= np.exp(np.linspace(np.log(self.min_pressure),
                                                np.log(self.max_pressure),
                                                self.n_vertical))[::-1, None, None]
        elif (self.pressure[-1] == 0).all():
            self.min_input_pressure = self.min_pressure
            if (self.min_pressure is None) or (self.min_pressure > self.pressure[-2].any()):
                self.min_input_pressure = .9 * self.pressure[-2].min()
                self.warning(f'min_pressure is larger than the 2nd "top" pressure so it will be set to 90% '
                             f'of the min of that level, i.e., {self.min_input_pressure:g} ('
                             f'old value is {self.min_pressure})')
            # "lower" the top pressure from 0 (infinite altitude) to min_pressure
            self.pressure[-1] = self.min_input_pressure

        assert self.pressure is not None, "Pressure has not been defined"
        self.ps = np.ones((self.n_latitudes, self.n_longitudes))  # ensure dimension
        self.ps *= self.pressure[0]

        if isinstance(self.temperature, dict) and "T_day" in self.temperature.keys():
            # Define temperature using day and night temperatures
            self.temperature = Simple2DTemperature(**self.temperature).build(self.grid, self.pressure,
                                                                             self.model)
        elif isinstance(self.temperature, (float, int)):
            self.temperature = np.full(self.shape, self.temperature)
        elif isinstance(self.temperature, str):
            # Define temperature using a custom class
            temp_class = get_class(self.temperature)
            self.temperature = temp_class().build(self)
        elif hasattr(self.temperature, "build"):
            # we assume temperature is a class then, with a build function.
            self.temperature = self.temperature.build(self.grid, self.pressure, self.model)

        self.temperature = self.make_3D(self.temperature)

        if self.gas_mix_ratio is None:
            self.gas_mix_ratio = {}
        self.input_vmr = self.gas_mix_ratio
        # Define VMRs using day and night values
        self.gas_mix_ratio = simple_2D_vmr(self.grid, self.gas_mix_ratio)
        
        self.gas_mix_ratio = self.make_3D(self.gas_mix_ratio)
        
        if self.chemistry is not None:
            self.chemistry.build(self)

        # For pressure under p_min_aerosols, set aerosols MMRs to 0
        for aerosol, aer_dict in self.aerosols.items():
            if "mmr" in aer_dict.keys() and "p_min" in aer_dict.keys():
                aer_dict["mmr"] = np.full(self.shape,
                                          aer_dict["mmr"])  # make mmr the same size as everything else
                aer_dict["mmr"][np.where(self.pressure < aer_dict["p_min"])] = 0

        self.compute_molar_mass()
        try:
            self.compute_altitude()
        except Exception as e:
            self.error(f"Could not compute altitude. {e}")

        # Ensure that the surface albedo parameters are correct.
        if self.albedo_surf is None:
            self.wn_albedo_cutoff = None

        if self.albedo_surf is not None and type(self.albedo_surf) is not np.ndarray:
            self.albedo_surf = self.albedo_surf * np.ones((self.n_latitudes, self.n_longitudes))

        if self.wn_albedo_cutoff is not None and type(self.wn_albedo_cutoff) is not np.ndarray:
            self.wn_albedo_cutoff = self.wn_albedo_cutoff * np.ones((self.n_latitudes, self.n_longitudes))

    def compute_altitude(self):
        """
        Compute altitude `z`, scaleheight `H` and gravity `g` at coordinates on `grid`.
        """
        self.info("Computing altitude using the hydrostatic equilibrium equation...")

        assert self.temperature.shape == self.shape, "Temperature does not have the right shape. Report " \
                                                     "this as a bug. "
        assert len(self.gas_mix_ratio) > 0, "No gas has been defined"
        assert self.molar_mass is not None, "Molar mass not computed. Call compute_molar_mass() first."

        # shape specific to atmospheric vertical shape:
        # level atmosphere is "doubled" by merging layers and levels
        z = np.zeros(self.shape)
        H = np.zeros(self.shape)
        g = np.zeros(self.shape)
        try:
            g[0] = self.planet.surface_gravity  # surface gravity (0th layer)
        except:
            self.error("Provide a planet to the atmosphere.")

        H[0] = (RGP * self.temperature[0]) / (
                self.molar_mass[0] * g[0])  # scaleheight at the surface (0th layer)

        for i in range(1, self.n_vertical):
            deltaz = (-1.) * H[i - 1] * np.log(self.pressure[i] / self.pressure[i - 1])
            z[i] = z[i - 1] + deltaz  # altitude at the i-th layer

            if i == self.n_vertical:
                break
            with np.errstate(over='ignore'):
                g[i] = self.planet.gravity(z[i])  # gravity at the i-th layer
            with np.errstate(divide='ignore'):
                H[i] = (RGP * self.temperature[i]) / (self.molar_mass[i] * g[i])

        self.altitude = z
        self.scaleheight = H
        self.gravity = g
        try:
            assert not np.isinf(self.altitude[:-1]).any()
            assert self.altitude.max() > 0
        except:
            if self.altitude.max() <= 0:
                msg = f"Max altitude is {self.altitude.max()}\n"
                bottom_loc = [[0, -1], 0, 0]
            else:
                loc = [min(i) for i in np.where(np.isinf(self.altitude))]
                bottom_loc = [[0, loc[0] - 1], loc[1], loc[2]]
                msg = "Altitude goes to infinity and beyond!\n"
                msg += "Infinite values begin at position %s (vertical, latitude, longitude).\n" % loc
            i = tuple(bottom_loc)
            msg += "Here are the values at positions %s:\n" % bottom_loc
            msg += "Altitude = %s\n" % z[i]
            msg += "Scaleheight = %s\n" % H[i]
            msg += "Gravity = %s\n" % g[i]
            msg += "Pressure = %s\n" % self.pressure[i]
            msg += "Temperature = %s\n" % self.temperature[i]
            msg += "Molar mass = %s\n" % self.molar_mass[i]
            raise ValueError(msg)
        return self.altitude
