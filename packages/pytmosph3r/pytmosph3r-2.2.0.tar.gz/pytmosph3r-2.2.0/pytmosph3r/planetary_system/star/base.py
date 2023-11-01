from abc import ABC, abstractmethod
from typing import Optional, Union

import astropy.units as u
import numpy
from astropy.units import Quantity
from exo_k import Spectrum

from pytmosph3r.log import Logger
from pytmosph3r.util import pt
from pytmosph3r.util.util import to_SI


class BaseStar(ABC, Logger):
    """
    This class represents the base properties of a star and the default methods implemented
    and required to be implemented.

    Subclasses should implement `_spectrum(self, wnedges: numpy.ndarray, wns: numpy.ndarray) -> Spectrum`
    """

    def __init__(self,
                 radius: Union[float, Quantity[pt.length]] = 695700000.,
                 mass: Union[None, float, Quantity[pt.mass]] = None,
                 **kwargs):
        """
        Args:
            radius (float, optional): Stellar radius in`m`
            mass (float, optional): Stellar mass in `kg`
        """
        Logger.__init__(self, name=self.__class__.__name__)

        if kwargs:
            raise DeprecationWarning(f"{kwargs=} is not empty.\n"
                                     f"API has been modified, you can now use astropy units.\n"
                                     f"Variables in float or int will be considered in SI.\n"
                                     f"For example the radius in solar radii:\n"
                                     f"radius = 1.5 * u.Rsun\n")

        self.radius: float = to_SI(radius, u.m)
        """Star radius (in `m`)."""

        self.mass: Optional[float] = to_SI(mass, u.kg)
        """Star mass (in `kg`)."""

    @property
    def mass_sol(self) -> Optional[float]:
        """Star mass (in `solar mass`)."""
        if self.mass is None:
            return None

        return (self.mass * u.kg).to_value('Msun')

    @property
    def radius_sol(self) -> float:
        """Star radius (in `solar radii`)."""
        return (self.radius * u.m).to_value('Rsun')

    def spectrum(self, wnedges: numpy.ndarray, wns: numpy.ndarray, distance: Optional[float] = None) -> Spectrum:
        """Return the spectrum of the flux at the star surface by default, or at the distance given in meters (m).

        Args:
            wnedges (numpy.ndarray): Wavenumbers of the bin edges to be used.
            wns (numpy.ndarray): Wavenumbers of the bin centers to be used.
            distance (Optional[float]): If distance is None, take the flux at the surface else take the flux seen at the
                given distance.
        Returns:
            Flux from the star.
        """
        s = self._spectrum(wnedges, wns)

        # Return the flux at the star surface.
        if distance is None:
            return s

        # Rescale the flux to take into account the distance from the star surface.
        return s * (self.radius / distance) ** 2

    @abstractmethod
    def _spectrum(self, wnedges: numpy.ndarray, wns: numpy.ndarray) -> Spectrum:
        """Return the spectrum of the flux at the surface of the star.

        Args:
            wnedges (numpy.ndarray): Wavenumbers of the bin edges to be used.
            wns (numpy.ndarray): Wavenumbers of the bin centers to be used.
        """

        raise NotImplementedError
