import math as m
import re

import numpy as np


class Simple2DTemperature:
    """Class to build a `2D` temperature, set to :py:attr:`T_day` on the `day` side of the planet,
    :py:attr:`T_night` on the `night` side of the planet,
    and a linear transition between :py:attr:`T_day` and :py:attr:`T_night` within the :py:attr:`beta` angle between day and night, representing the terminator.
    An annulus is defined at pressures above :py:attr:`p_iso`, where the temperature is set to :py:attr:`T_deep`.
    """
    
    def __init__(self, T_day, T_night, T_deep=None, beta=10, p_iso=1e99):
        """Initialize the `2D` temperature using simple parameters:
        
        Args:
            T_day (float) : Temperature on the `day` side of the planet.
            T_night (float) : Temperature on the `night` side.
            T_deep (float) : Temperature set for layers with a pressure above :py:attr:`p_iso` (overriding the other values).
            beta (float) : Angle between day and night defining the region around the terminator with a linear transition between :py:attr:`T_day` and :py:attr:`T_night`.
            p_iso (float) : Pressure above which the temperature is overridden with :py:attr:`T_deep`.
        """
        self.T_day = T_day
        self.T_night = T_night
        self.T_deep = T_deep if T_deep else T_day
        self.beta = beta
        self.p_iso = p_iso

    @property
    def beta_rad(self):
        return m.radians(self.beta)

    def build(self, grid, P, model=None):
        """This function must return the temperature of the atmosphere, and therefore have a shape compatible with `grid`.

        Args:
            grid (Grid3D): Grid (from Pytmosph3R).
            P (float, array): Pressure points corresponding to the grid.
            model (Model, optional): Entire Pytmosph3R model in case you need something else (chemistry, ...).
        """        
        self.temperature = np.zeros(grid.shape)

        sol_lon, sol_lat = 0., 0.

        if model and model.orbit is not None:
            sol_lat, sol_lon = model.orbit.star_coordinates

        for lat, lon in grid.horizontal_walk():
            alpha = np.arcsin(np.sin(grid.mid_latitudes[lat])*np.sin(sol_lat)
                    + np.cos(grid.mid_latitudes[lat])*np.cos(grid.mid_longitudes[lon] - sol_lon) * np.cos(sol_lat))

            if 2*alpha > self.beta_rad:
                T = self.T_day
            elif 2*alpha < -self.beta_rad:
                T = self.T_night
            else:
                T = self.T_night + (self.T_day-self.T_night) * (alpha/self.beta_rad + 1/2)
            self.temperature[:, lat, lon] = T
            assert not np.isnan(T).any(), "Nan in temperature"

        self.temperature[np.where(P > self.p_iso)] = self.T_deep

        return self.temperature

def simple_2D(grid, day_value, night_value):
    """Returns an array with the shape of :py:attr:`grid`,
    of which the values on the day side are equal to :py:attr:`day_value`,
    and the values on the night side are equal to :py:attr:`night_value`.
    See :class:`~pytmosph3r.grid.Grid3D.day_longitudes` for a definition of the day side
    and :class:`~pytmosph3r.grid.Grid3D.night_longitudes` for a definition of the night side.

    Args:
        grid (:class:`~pytmosph3r.grid.Grid3D`): 3D grid giving the dimensions for the array.
        day_value (float): Value for the day side.
        night_value (float): Value for the night side.
    """
    array = np.zeros(grid.shape)
    array[:, :, grid.day_longitudes] = day_value
    array[:, :, grid.night_longitudes] = night_value
    return array

def simple_2D_vmr(grid, input_vmr):
    new_dict = {}
    for gas_name, vmr in input_vmr.items():
        if gas_name.endswith("_day"):
            vmr_day = vmr
            gas_day = gas_name
            gas_night = re.sub('_day$', '_night', gas_name)
            gas = re.sub('_day$', '', gas_name)
            try:
                vmr_night = input_vmr[gas_night]
            except:
                raise KeyError("If you have a day vmr, you should have a night vmr too! The corresponding key is %s" % gas_night)
            new_dict[gas] = simple_2D(grid, vmr_day, vmr_night)
        elif gas_name.endswith("_night"):
            continue
        else:
            new_dict[gas_name] = input_vmr[gas_name]
    return new_dict