from typing import Union

import astropy.units as u
import numpy as np
from astropy.units import Quantity

from pytmosph3r.log import Logger
from pytmosph3r.util import pt
from pytmosph3r.util.geometry import CartesianCoordinateSystem
from pytmosph3r.util.util import to_SI


class Observer(Logger):
    """Defines the position of the observer using a unit vector.
    The starting point of the vector is the center of the planet.
    The ending point is located at the coordinate (:py:attr:`latitude`, :py:attr:`longitude`) on the unit sphere.
    Astropy's units are supported. Floats are considered to be in SI units.
    WARNING: This class has been extracted from :class:`~.rays.Rays` and should probably not be used independently.
    """

    def __init__(self, latitude: Union[float, Quantity[pt.angle]] = None,
                 longitude: Union[float, Quantity[pt.angle]] = None,
                 orbit=None, **kwargs):
        r"""Set the observer's position with:

        Args:
            latitude (float, Unit, optional): Latitude (in :math:`rad` or astropy units). Default to 0.
            longitude (float, Unit, optional): Longitude (in :math:`rad` or astropy units). Default to $\pi$.
        """
        super().__init__(self.__class__.__name__)
        self.unit = 'rad'

        self.latitude = to_SI(latitude, u.rad)
        """Latitude coordinate of the ending point of the unit vector (in radians)."""

        self.longitude = to_SI(longitude, u.rad)
        """Longitude coordinate of the ending point of the unit vector (in radians)."""

        self.orbit = orbit
        self._system = None

        if kwargs:
            raise DeprecationWarning(f"{kwargs=} is not empty.\n"
                                     f"API has been modified, you can now use astropy units.\n"
                                     f"Variables in float or int will be considered in SI.\n"
                                     f"For example the longitude in degrees:\n"
                                     f"longitude = 180 * u.deg\n")

    def build(self, model=None):
        """Link to model, and set default values if not set before."""
        if model is not None:
            self.orbit = model.orbit
        if self.latitude is None:
            self.latitude = 0
        if self.longitude is None:
            self.longitude = np.pi

    @property
    def coordinates(self):
        """Tuple (latitude, longitude)."""
        return self.latitude, self.longitude

    @property
    def orbit(self):
        if self._orbit is None:
            raise AttributeError('You should set the reference to the orbit.')

        return self._orbit

    @orbit.setter
    def orbit(self, orbit):
        self._orbit = orbit
        if orbit is not None and self.longitude is None:
            self.longitude = np.pi + orbit.star_coordinates[1]

    @property
    def cartesian_system(self):
        """Cartesian coordinate system (x,y,z) of which:

        - z is oriented along the rotation axis (pointing towards the North Pole)
        - x points towards a reference point on the equator that corresponds to a longitude equal to zero
        - y is chosen to have a direct basis.

        The coordinates of the unit vector defining the direction of the rays are then computed through
        :class:`~pytmosph3r.util.geometry.CartesianCoordinateSystem` using its spherical coordinates (
        :py:attr:`latitude`, :py:attr:`longitude`).
        """

        self._system = self._system if self._system else CartesianCoordinateSystem(self.latitude, self.longitude)

        return self._system

    def add_ray_origin(self, altitude, angle):
        """Function to add the origin point of a ray, i.e., its intersection with the terminator using its polar
        coordinates (:py:attr:`altitude`, :py:attr:`angle`), to the Cartesian coordinate system
        :py:attr:`cartesian_system`.

        This function is used for each ray in :class:`Rays.compute_sub_rays`.

        Args:
            altitude (float): altitude (`m`) of the origin point
            angle (float): angle (`radians`) of the origin point
        """

        self.cartesian_system.add_ray_origin(altitude, angle)

    def position_from_time(self, time, orbit=None):
        """Update the position of the observer based on the time (in :math:`seconds`) and the orbit.
        """
        if orbit is None:
            orbit = self.orbit

        self.latitude, self.longitude = orbit.observer_from_time(time)
        self._system = None  # reset cartesian system
        return self.latitude, self.longitude

    def position_from_phase(self, phase, orbit=None):
        """Update position of the observer based on the phase (in :math:`rad`) and the orbit.
        """
        if orbit is None:
            orbit = self.orbit

        self.latitude, self.longitude = orbit.observer_from_phase(phase)
        self._system = None  # reset cartesian system
        return self.latitude, self.longitude
