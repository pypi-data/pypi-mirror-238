from typing import Optional, Union

import numpy as np

from pytmosph3r.config.factory import create_obj
from .atmosphere import Atmosphere


class InputAtmosphere(Atmosphere):
    """Class to build an atmosphere of your own, which will override the datafile."""

    def __init__(self,
                 grid=None,
                 pressure=None,
                 max_pressure=None,
                 min_pressure=None,
                 temperature=None,
                 gas_mix_ratio=None,
                 transparent_gases=None,
                 aerosols=None,
                 winds=None,
                 chemistry=None,
                 molar_mass=None,
                 albedo_surf=None,
                 wn_albedo_cutoff=None
                 ):
        """Create the atmosphere you want (or you deserve).

        Args:
            grid (:class:`~pytmosph3r.grid.Grid3D`): Grid representing the coordinate system (level+layer, latitude,
            longitude).
            pressure (float, :obj:`array`, optional): Pressure for each point in :py:attr:`grid`. Incompatible with
            :py:attr:`max_pressure`.
            max_pressure (float) : Maximum pressure (at the surface). Incompatible with :py:attr:`pressure`.
            min_pressure (float) : Minimum pressure to use in the highest column of the model.
            temperature (float, :obj:`array`, dict): Temperature for each point in :py:attr:`grid`. If it is an array
            or a float, it will simply define the temperature over the whole grid. If used as a dictionary,
            it can configure :class:`~pytmosph3r.atmosphere.simple2d.Simple2DTemperature`.
            gas_mix_ratio (float, :obj:`array`): Volume Mixing Ratio of gases (dictionary :code:`{'H2O': array, ...}`.
            transparent_gases (list, optional): Gases considered transparent (not taken into account for the
            contributions).
            aerosols (float, :obj:`array`): Aerosols: number density of particles (in number per unit volume).
            chemistry (:class:`pytmosph3r.chemistry.Chemistry`): Chemistry module. Either a class of
            :class:`pytmosph3r.chemistry.Chemistry` or your personal module (which should probably inherit from
            :class:`pytmosph3r.chemistry.Chemistry`, or at least change the gas mix ratio of the atmosphere).
            albedo_surf (ndarray, optional): 2d array with the albedo value to use on each column.
            wn_albedo_cutoff (ndarray, optional): 2d array with the cutoff value of the low pass filter on each column.
        """

        super().__init__(self.__class__.__name__)

        if aerosols is None:
            aerosols = {}
        if gas_mix_ratio is None:
            gas_mix_ratio = {}
        self.grid = grid
        self.pressure = pressure
        self.max_pressure = max_pressure
        self.min_pressure = min_pressure
        if max_pressure and min_pressure and max_pressure < min_pressure:
            self.critical(
                    f"max_pressure = {max_pressure} < min_pressure = {min_pressure}. I am reversing them but check if "
                    f"it "
                    f"is not a mistake.")
            self.max_pressure = min_pressure
            self.min_pressure = max_pressure
        self.temperature = temperature
        self.winds = winds
        self.gas_mix_ratio = gas_mix_ratio
        self.transparent_gases = transparent_gases
        self.aerosols = aerosols
        self.altitude = None  # Altitude for each point in :py:attr:`grid`.

        # Treat the albedo of the planet surface
        # 2d array of float.
        self.albedo_surf: Optional[Union[float, np.ndarray]] = albedo_surf
        self.wn_albedo_cutoff: Optional[Union[float, np.ndarray]] = wn_albedo_cutoff

        if chemistry is None or (isinstance(chemistry, dict) and not len(chemistry)):
            self.chemistry = None
        elif isinstance(chemistry, dict):
            self.chemistry = create_obj({"Chemistry": chemistry}, "Chemistry")
        else:
            self.chemistry = chemistry

        self.molar_mass = molar_mass
        if self.molar_mass is not None:
            self.recompute_molar_mass = False

    def outputs(self):
        return ["altitude"]
