from typing import Union

import astropy.units as u
from astropy.units import Quantity, quantity_input

from pytmosph3r.log import Logger
from pytmosph3r.util import pt
from pytmosph3r.util.constants import G
from pytmosph3r.util.util import to_SI


@quantity_input
def mass_to_surface_gravity(mass: Quantity[pt.mass], radius: Quantity[pt.length]):  # -> Quantity[pt.acceleration]
    """
    Compute the gravity at the surface of a sphere of radius `radius` and mass `mass`.

    Args:
        mass (Quantity[mass]): Mass of the planet.
        radius (Quantity[length]): Radius of the planet.
    Return:
        (Quantity[acceleration]): Return the gravity at the surface of the planet.

    """

    surface_gravity: Quantity[pt.acceleration] = G * mass / (radius ** 2) * u.Unit('N*m2*kg-2')

    return surface_gravity.to('m.s-2')


class Planet(Logger):
    """Represent a planet, while allowing to get the position of the star in the planet frame."""

    def __init__(self, surface_gravity: Union[float, Quantity[pt.acceleration]],
                 radius: Union[float, Quantity[pt.length]], **kwargs):
        """
        Args:
            surface_gravity (float): Surface gravity of the planet (m.s-2)
            radius (float): Radius of the planet (m)
        """
        Logger.__init__(self, name='Planet')

        self.radius = to_SI(radius, u.m)
        """ Planet radius (in `m`)."""

        # Basic check to ensure
        if self.radius < 10:
            raise ValueError(
                    f"Planet radius ({radius}) is too small. "
                    f"For a radius in Jupiter radii, you can use astropy: radius * u.Rjup")

        if kwargs:
            raise DeprecationWarning(f"{kwargs=} is not empty.\n"
                                     f"API has been modified, you can now use astropy units.\n"
                                     f"Variables in float or int will be considered in SI.\n"
                                     f"For example the radius in Jupiter radii:\n"
                                     f"radius = 1.5 * u.Rjup\n")

        self.surface_gravity = to_SI(surface_gravity, u.Unit('m*s-2'))
        r"""Surface gravity (:math:`m\cdot s^{-2}`)."""

    def build(self, model=None):
        pass

    @classmethod
    def fromJupiter(cls, surface_gravity: float, radius: float):
        """Create a `Planet` object using Jupiter values.

        Args:
            surface_gravity (float): Surface gravity in `m s-2`
            radius (float): Planet radius in Jupiter radius.
        """

        radius = (radius * u.Rjup).to_value('m')

        return cls(surface_gravity=surface_gravity, radius=radius)

    @property
    def mass(self):
        """Planet mass (:math:`kg`)."""
        return self.surface_gravity * (self.radius ** 2) / G

    @property
    def mass_jup(self) -> float:
        """Planet mass (in `Jupiter mass`)."""
        return (self.mass * u.Unit('kg')).to_value('Mjup')

    @property
    def radius_jup(self) -> float:
        """Planet radius (in `Jupiter radii`)."""

        return (self.radius * u.Unit('m')).to_value('Rjup')

    def gravity(self, height: float) -> float:
        r"""Gravity (:math:`m\cdot s^{-2}`) at height (:math:`m`) from planet."""

        return self.surface_gravity * (self.radius ** 2) / ((self.radius + height) ** 2)
