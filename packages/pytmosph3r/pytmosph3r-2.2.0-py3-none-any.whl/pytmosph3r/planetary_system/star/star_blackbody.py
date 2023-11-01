from typing import Optional

import astropy.units as u
import numpy as np
from astropy.constants.codata2018 import sigma_sb
from exo_k import Bnu_integral_num, Spectrum

from pytmosph3r.util import pt
from .base import BaseStar


@u.quantity_input
def luminosity_from_temperature(temperature: u.Quantity[pt.temperature], radius: u.Quantity[pt.length]) -> u.W:
    """
    This function allows retrieving of the luminosity [Power] of a star behaving as a blackbody from
    its temperature [Temperature] and its radius [Length].

    Args:
        temperature (u.Quantity): Effective temperature of the star.
        radius (u.Quantity): Radius of the star.

    Returns:
        Luminosity of the star in Watt [Power].
    """

    return 4 * np.pi * sigma_sb * radius.to(u.m) ** 2 * temperature.to(u.K) ** 4


@u.quantity_input(luminosity='power', radius='length')
def temperature_from_luminosity(luminosity: u.Quantity, radius: u.Quantity) -> u.K:
    """
    This function allows retrieving of the effective temperature [Temperature] of a star behaving as a blackbody from
    its luminosity [Luminosity] and its radius [Length].

    Args:
        luminosity (u.Quantity): Luminosity of the star.
        radius (u.Quantity): Radius of the star.

    Returns:
        Effective temperature of the star in Kelvin [Temperature].
    """

    a = 4. * np.pi * radius.to(u.m) ** 2 * sigma_sb

    t4 = luminosity.to(u.W) / a

    return np.power(t4, 1. / 4.)


class BlackbodyStar(BaseStar):
    """Star which behave as a blackbody.
    """

    def __init__(self, temperature: float = 5780, radius: float = 695700000., mass: Optional[float] = None, **kwargs):
        """
        Args:
            temperature (float, optional): Stellar temperature in `K`. Default to the solar effective temperature.
            radius (float, optional): Radius of the star in `m`. Default to the solar radius.
            mass (float, optional): Mass of the star in `kg`. Optional.
        Returns:
            An object behaving as a `Star`, with a flux matching a blackbody of the given effective temperature.
        """
        super().__init__(radius, mass, **kwargs)

        self.temperature = temperature
        """Star effective temperature (in `K`)."""

    @classmethod
    @u.quantity_input(radius='length', mass='mass', temperature='temperature', equivalencies=u.temperature())
    def fromEffectiveTemperature(cls, temperature: u.Quantity, radius: u.Quantity, mass: Optional[u.Quantity] = None):
        """
            Create a `BlackbodyStar` object from its effective temperature.
        Args:
            temperature (Quantity['temperature']): Stellar effective temperature [Temperature].
            radius (Quantity['length']): Stellar radius [Length].
            mass (Quantity['mass']): Stellar mass [Mass].

        Returns:
            `BlackbodyStar` matching the provided effective temperature.
        """

        return cls(temperature=temperature.to_value(u.Unit('K'), equivalencies=u.temperature()),  # noqa
                   radius=radius.to_value(u.Unit('m')),
                   mass=mass.to_value(u.Unit('kg')) if mass is not None else None)

    @classmethod
    @u.quantity_input(radius='length', mass='mass', bolometric_luminosity='power')
    def fromBolometricLuminosity(cls, bolometric_luminosity: u.Quantity,
                                 radius: u.Quantity, mass: Optional[u.Quantity] = None):
        """
            Create a `BlackbodyStar` object from its bolometric luminosity.
        Args:
            bolometric_luminosity (Quantity['power']): Bolometric luminosity of the star [Power].
            radius (Quantity['length']): Stellar radius [Length].
            mass (Quantity['mass']): Stellar mass [Mass].

        Returns:
            `BlackbodyStar` matching the provided luminosity.
        """

        temperature = temperature_from_luminosity(luminosity=bolometric_luminosity, radius=radius)

        return cls.fromEffectiveTemperature(temperature=temperature,
                                            radius=radius, mass=mass)

    @classmethod
    def fromSolar(cls, temperature: float = 5770, radius: float = 1., mass: float = 1.):
        """Create a `Star` object using solar values (except temperature, which is in Kelvin).

        Args:
            temperature (Quantity['temperature']): Stellar effective temperature [Temperature].
            radius (float): radius, scaled to the Sun.
            mass (float): Mass of the star in `Msun`.
        """
        return cls(temperature=temperature,
                   radius=(radius * u.Rsun).to_value('m'),
                   mass=(mass * u.Msun).to_value('kg'))

    def _spectrum(self, wnedges: np.ndarray = None, wns: np.ndarray = None):
        """Return the spectrum of the flux associated to the star.

        Args:
            wnedges (numpy.ndarray): Wavenumbers of the bin edges to be used in `cm-1`.
            wns (numpy.ndarray): Wavenumbers of the bin centers to be used in `cm-1`.
        """

        piB = np.pi * Bnu_integral_num(wnedges, self.temperature) / np.diff(wnedges)

        return Spectrum(value=piB, wns=wns, wnedges=wnedges)
