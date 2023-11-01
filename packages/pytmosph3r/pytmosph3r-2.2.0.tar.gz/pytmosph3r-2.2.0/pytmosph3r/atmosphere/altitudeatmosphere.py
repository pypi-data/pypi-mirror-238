from copy import copy

import numpy as np

from pytmosph3r.util.constants import RGP
from pytmosph3r.util.math import interp1d
from pytmosph3r.util.util import arrays_to_zeros, aerosols_array_iterator
from .atmosphere import Atmosphere
from ..grid import Grid3D

class AltitudeAtmosphere(Atmosphere):
    """
    Atmospheric model with a (altitude, latitude, longitude) coordinate system. The attributes of this
    class are the same as :class:`~pytmosph3r.atmosphere.input_atmosphere.InputAtmosphere`, except that
    they have been interpolated in a spherical grid.
    """

    def __init__(self, model=None, n_vertical=100, n_latitudes=49, n_longitudes=64):
        super().__init__(self.__class__.__name__)
        if model:
            self.model = model
            self.planet = model.planet
            self.input_atm = model.input_atmosphere
            self.recompute_molar_mass = self.input_atm.recompute_molar_mass
            n_vertical = model.n_vertical
            n_latitudes = self.input_atm.n_latitudes
            n_longitudes = self.input_atm.n_longitudes
            self.grid = copy(model.input_atmosphere.grid)
            self.grid.n_vertical = n_vertical
        else:
            self.debug("Not using model. You will have to deal with the rest yourself!")
            self.grid = Grid3D(n_vertical=n_vertical, n_latitudes=n_latitudes, n_longitudes=n_longitudes)


        self.max_altitude = None
        """Max altitude in the model, calculated based on :py:attr:`~pytmosph3r.model.Model.min_pressure`."""
        self.altitude_levels = None
        """Altitudes of each level (separating each layer). :obj:`Array` of length :py:attr:`n_levels`."""
        self.altitude = None
        """Altitudes in the middle of each layer.  :obj:`Array` of length :py:attr:`n_layers`."""
        self.aerosols = {}
        """Aerosols for each point of the altitude grid, interpolated from
        :attr:`pytmosph3r.atmosphere.InputAtmosphere.aerosols` (each aerosol is a dictionary with keys {'mmr', 'reff',
        'condensate_density'}). """

    def build(self):
        self.generate_altitude_grid()
        self.interpolate_from_input()

    @property
    def n_layers(self) -> int:
        """Number of layers in the model."""
        return self.grid.n_vertical

    @property
    def n_levels(self) -> int:
        """Number of levels in the model (equal to :py:attr:`n_layers` `+1`)."""
        return self.grid.n_vertical+1

    def index_altitude(self, altitude):
        """Gives the index of the layer containing an `altitude` (given in `m`)."""
        if altitude > self.max_altitude or altitude < 0:
            return np.nan
        return int(altitude / self.max_altitude * self.n_layers)

    def generate_altitude_grid(self):
        """Build an atmospheric grid based on the highest altitude of the level-based atmospheric grid,
        discretized into :py:attr:`n_vertical` points.
        """
        try:
            # find altitude just above or exactly at min_pressure
            p_i = np.where(self.input_atm.pressure >= self.input_atm.min_pressure)
            r_i = p_i[0]+1
            i = np.where(r_i < self.input_atm.n_vertical)
            indices = (r_i[i], p_i[1][i], p_i[2][i])

            self.max_altitude = self.input_atm.altitude[indices].max()
        except:
            self.warning("No min_pressure provided in .cfg file under [Atmosphere].")
            self.max_altitude = self.input_atm.altitude[np.where(self.input_atm.altitude != np.inf)].max()
        if self.max_altitude <= 0:
            raise RuntimeError(f"Max altitude is {self.max_altitude}. Is there an atmosphere and something in it?")
        self.altitude_levels = np.linspace(0, self.max_altitude, self.n_levels)
        self.altitude = self.altitude_levels[:-1] + np.diff(self.altitude_levels) / 2.  # middle of the layers
        assert not np.isnan(self.altitude).any(), "NaN value in altitude"

    def interpolate_from_input(self):
        """Interpolate pressure, temperature and gas mix ratios from levels to the new coordinate system.
        """
        self.info('Interpolating PTX profiles...')
        self.interp = 'linear'
        if self.model.interp:
            self.interp = self.model.interp

        self.pressure = np.zeros(self.shape)
        self.temperature = np.zeros(self.shape)
        self.winds = np.zeros(self.shape+(3,))
        self.gas_mix_ratio = {}
        for gas in self.input_atm.gas_mix_ratio:
            self.gas_mix_ratio[gas] = np.zeros(self.shape)
        self.aerosols = arrays_to_zeros(self.input_atm.aerosols, self.shape)

        # Interpolate temperature
        self.horizontal_run(self.altitude_interp, self.temperature,
                            self.input_atm.temperature, interp='linear')

        # Interpolate winds
        if self.model.opacity.doppler:
            for i in range(3): # u, v, w
                self.horizontal_run(self.altitude_interp, self.winds[...,i], self.input_atm.winds[...,i], interp='linear')

        # Interpolate VMRs
        for gas in self.gas_mix_ratio:
            if isinstance(self.input_atm.gas_mix_ratio[gas], (float, str)):
                self.gas_mix_ratio[gas] = self.input_atm.gas_mix_ratio[gas]
            else:
                self.horizontal_run(self.altitude_interp,
                                    self.gas_mix_ratio[gas],
                                    self.input_atm.gas_mix_ratio[gas],
                                    interp='linear')  # linear mode ensures total VMRs = 1

        if self.recompute_molar_mass:
            self.compute_molar_mass()
        else:
            self.molar_mass = np.zeros(self.shape)
            self.horizontal_run(self.altitude_interp, self.molar_mass,
                                self.input_atm.molar_mass, interp='linear')

        # Interpolate aerosols
        for aerosol, key in aerosols_array_iterator(self.aerosols):
            self.horizontal_run(self.altitude_interp,
                                self.aerosols[aerosol][key],
                                self.input_atm.aerosols[aerosol][key], interp='linear')

        # Interpolate pressure
        if self.model.interp:
            self.horizontal_run(self.altitude_interp, self.pressure, self.input_atm.pressure)
        self.compute_pressure()

        assert not np.isnan(self.pressure).any(), "NaN values in pressure"

    def altitude_interp(self, lat, lon, dest, origin, interp='log'):
        """Interpolation of the values of :py:attr:`dest` based on the information of :py:attr:`origin`,
        associated with the altitude of the :class:`~pytmosph3r.atmosphere.InputAtmosphere`.
        This function operates on the (vertical) column at the location given by (:py:attr:`lat`,
        :py:attr:`lon`) in the atmosphere.
        The interpolation uses the altitude of the altitude grid as the input variables.

        Args:
            lat (int): Latitude index
            lon (int): Longitude index
            dest (:obj:`array`): Destination array to interpolate into
            origin (:obj:`array`): Origin array to interpolate from
            interp (str): 'linear', 'log', ...
        """
        alt_max = self.altitude.searchsorted(self.input_atm.altitude[:, lat, lon].max(), side='left')
        dest[alt_max:, lat, lon] = origin[-1, lat, lon]  # outside of origin boundaries, just copy last value

        dest[:alt_max, lat, lon] = interp1d(self.input_atm.altitude[:, lat, lon],
                                            origin[:, lat, lon], ykind=interp)(self.altitude[:alt_max])

    def compute_pressure(self):
        """Re-compute the pressure lower than min_pressure, using the hydrostatic equilibrium equation.
        """

        if isinstance(self.temperature, (float, int)):
            self.temperature = np.full(self.shape, self.temperature)
        if isinstance(self.molar_mass, (float, int)):
            self.molar_mass = np.full(self.shape, self.molar_mass)
        p_min = self.input_atm.min_pressure\
            if self.input_atm.min_pressure and self.input_atm.min_pressure > self.input_atm.pressure.min()\
            else self.input_atm.pressure.min()

        g = np.zeros(self.shape)
        H = np.zeros(self.shape)

        ps = self.input_atm.ps  # surface pressure
        g[0] = self.planet.surface_gravity  # surface gravity (0th layer)
        H[0] = (RGP * self.temperature[0]) / (
                    self.molar_mass[0] * g[0])  # scaleheight at the surface (0th layer)
        dz = np.diff(self.altitude)

        columns = np.where(self.pressure[0] < 10 * p_min)
        self.pressure[0][columns] = ps[columns] * np.exp(-self.altitude[0] / H[0][columns])

        for i in range(1, self.n_vertical):
            columns = np.where(self.pressure[i] < 10 * p_min)
            self.pressure[i][columns] = self.pressure[i - 1][columns] * np.exp(-dz[i - 1] / H[i - 1][columns])

            with np.errstate(over='ignore'):
                g[i] = self.planet.gravity(self.altitude[i])  # gravity at the i-th layer
            with np.errstate(divide='ignore'):
                H[i] = (RGP * self.temperature[i]) / (self.molar_mass[i] * g[i])

    def outputs(self):
        return ["grid", "altitude", "altitude_levels", "pressure", "temperature", "gas_mix_ratio", "aerosols"]
