from typing import Optional, Union

import astropy.units as u
import numpy
import numpy as np
from astropy.units import Quantity
from exo_k import Spectrum

from .base import BaseStar


class SpectrumStar(BaseStar):
    """
    `SpectrumStar` allow to provide a custom flux at the star surface.

    With this kind of spectrum, it only makes sense to define the bolometric luminosity over the given wavenumbers
    range.
    Indeed, we have no way to get the energy distributed outside the range.
    """

    def __init__(self, spectrum: Spectrum, radius: Union[float, Quantity] = 695700000.,
                 mass: Union[None, float, Quantity] = None, **kwargs):
        super().__init__(radius, mass, **kwargs)

        self.__spectrum: Optional[Spectrum] = spectrum
        """Spectrum at the surface of the star"""

    @classmethod
    @u.quantity_input(bolometric_luminosity='power', radius='length', mass='mass', equivalencies=u.temperature())
    def fromBolometricLuminosity(cls, bolometric_luminosity: u.Quantity, spectrum: Spectrum,
                                 radius: u.Quantity, mass: u.Quantity):
        """
            Create a `SpectrumStar` object from a bolometric luminosity and spectrum.
        Args:
            bolometric_luminosity (Quantity['power']): Bolometric luminosity of the star when integrated on the
                spectrum range.
            spectrum (Spectrum): Spectrum of the star.
            radius (Quantity['length']): Stellar radius [Length].
            mass (Quantity['mass']): Stellar mass [Mass].

        Returns:
            An object behaving as a `Star`, with a custom flux.
        """
        spectrum = spectrum.copy()
        radius_si = radius.to_value(u.Unit('m'))
        star_surface = 4. * np.pi * radius_si ** 2

        alpha = bolometric_luminosity.to_value('W') / np.dot(spectrum.value, np.diff(spectrum.wnedges))
        spectrum.value = spectrum.value * (alpha / star_surface)

        return cls(spectrum=spectrum,
                   radius=radius_si,
                   mass=mass.to_value(u.Unit('kg')))

    def _spectrum(self, wnedges: numpy.ndarray, wns: numpy.ndarray):
        """Return the spectrum associated to the star.

        Args:
            wnedges (numpy.ndarray): Wavenumbers of the bin edges to be used.
            wns (numpy.ndarray): Wavenumbers of the bin centers to be used.
        """

        s = self.__spectrum.bin_down_cp(wnedges=wnedges)
        s.wns = wns

        return s
