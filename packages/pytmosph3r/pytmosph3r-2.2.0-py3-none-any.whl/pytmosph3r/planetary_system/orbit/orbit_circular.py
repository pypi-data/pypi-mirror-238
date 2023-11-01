from typing import Optional, Tuple, Union

import astropy.units as u
import numpy as np
from astropy.units import Quantity

from pytmosph3r.util import pt
from pytmosph3r.util.util import to_SI

from .base import Orbit


@np.vectorize
def neg_pi(x):
    """Simply get negative values for 2*Pi > x > Pi."""
    if x > np.pi:
        return x - 2 * np.pi
    return x


class CircularOrbit(Orbit):
    """
    This class implement the default behaviour for the trajectory of a planet, ie a circular orbit with tidal lock.
    """

    def __init__(self,
                 a: Union[None, float, Quantity[pt.length]] = None,
                 period: Union[None, float, Quantity[pt.time]] = None,
                 star_coordinates: Tuple[float, float] = None,
                 inclination: Union[float, Quantity[pt.angle]] = None):
        """

        Args:
            a (Optional[float]): Distance between the star and the planet in meter (m), if none provided default to 1 AU
            period (Optional[float]): Orbital period in seconds.
            star_coordinates (tuple): Defines the coordinates of the star (latitude, longitude) in the planetary
                coordinate system if needed. Used for emission (top flux) for example. By default, the position is (
                0, 0).
            inclination (float): Inclination of the orbit in radians (rad).
        """
        super().__init__()

        self._a: float = to_SI(a, u.m)
        """Radius of the circular orbit in `m`."""

        self._period: float = to_SI(period, u.s)
        """Period of the circular orbit in `seconds`."""

        self._star_coordinates: Tuple[float, float] = to_SI(star_coordinates, u.rad)
        """Coordinates (in `radians`) of the star (latitude, longitude) in the planetary spherical coordinate system.
         Used to specify the top flux (emission)."""

        self._inclination: float = to_SI(inclination, u.rad)
        """Inclination of the circular orbit in `radians`, at mid-transit.
         (highest point is at mid-transit, other points are not supported yet)."""

    def build(self, model=None):
        pass

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = to_SI(value, u.m)

    @property
    def inclination(self):
        if self._inclination is None:
            return 0
        return self._inclination

    @inclination.setter
    def inclination(self, value):
        self._inclination = to_SI(value, u.rad)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period: float = to_SI(value, u.s)

    @property
    def star_coordinates(self):
        if self._star_coordinates is None:
            return (0, 0)
        return self._star_coordinates

    @star_coordinates.setter
    def star_coordinates(self, value):
        self._star_coordinates = value

    @property
    def is_tidal_locked(self) -> bool:
        return True

    def r(self, true_anomaly: float = 0) -> float:
        return self.a

    def time(self, phase):
        """Converts phase (in radians) to time (in seconds), using :attr:`period`."""
        return phase / (2 * np.pi) * self.period

    def phase(self, time):
        """Converts time (in seconds) to phase (in radians), using :attr:`period`."""
        try:
            return time / self.period * (2 * np.pi)
        except:
            raise AttributeError(
                    "Period has not been defined. Please provide it in the Orbit() module to use time variables.")

    def star_coordinates_projected(self, phase):
        """Taken from `pytmosph3r.util.geometry.CircleIntersection.star_coordinates`"""

        b = self.a * np.sin(self.inclination) * np.cos(phase)
        d = self.a * np.sin(phase)

        # Projected over the sky plan
        rS = np.sqrt(b ** 2 + d ** 2)
        aS = np.arctan2(d, b)

        return rS, aS

    def obs_long_to_phase(self, longitude):
        """Converts the `longitude` of an observer (in :math:`rad`) to the `phase` of the transit. The phase is
        defined as equal to 0 during mid-transit and increasing during transit. The longitude of the observer is
        equal to :math:`pi` + :attr:`substellar_longitude` at mid transit (and also increasing).
        """
        return np.pi + self.star_coordinates[1] - longitude

    def phase_to_obs_long(self, phase):
        """Converts a phase (in :math:`rad`) to the longitude of the observer. See definition of phase and observer
        in :func:`obs_long_to_phase` below.
        """
        return np.pi + self.star_coordinates[1] - phase

    def phase_from_observer(self, obs_loc=(0, np.pi)):
        """Calculates the phase of the transit using the coordinates of the observer and the star (in :math:`rad`).
        The phase is defined as equal to 0 at mid-transit and increasing during transit.
        """
        phase = self.obs_long_to_phase(obs_loc[1])
        # TODO fix formula
        return neg_pi(phase)

    def observer_from_phase(self, phase=0):
        """Calculates the phase of the transit using the coordinates of the observer and the star (in :math:`rad`).
        The phase is defined as equal to 0 at mid-transit and increasing during transit.
        This function only supports stars at the equator (0) or at the pole (+/-Pi/2).
        Args:
            phase (float): phase in `rad`
        """
        star_lat, star_lon = self.star_coordinates
        obs_lat = (-self.inclination - star_lat) * np.cos(phase)

        if star_lat in (np.pi / 2, -np.pi / 2):
            if self.inclination:
                self.debug("Inclination not supported for this star latitude.")
            obs_lat = (-star_lat) * np.cos(phase)
            sign = np.sign(phase / np.arccos(np.cos(phase)))
            obs_lon = sign * (star_lon + np.pi / 2)
        elif star_lat < -np.pi / 8 or star_lat > np.pi / 8:
            raise NotImplementedError("Orbit not supported for this star latitude.")
        else:
            obs_lon = self.phase_to_obs_long(phase)

        return obs_lat, obs_lon

    def observer_from_time(self, time=0):
        """Function to convert time to observer position."""
        return self.observer_from_phase(self.phase(time))

    def time_from_observer(self, observer):
        """Function to get time from observer position."""
        return self.phase_from_observer(observer) / (2 * np.pi) * self.period
