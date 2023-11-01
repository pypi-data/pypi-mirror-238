import numpy as np

from pytmosph3r.log import Logger


class Chemistry(Logger):
    """Base class to inherit from to compute abundances based on atmospheric properties.

    Args:
        gases (:obj:`list`): List of gases to put in atmosphere
    """
    def __init__(self, name=None, gases=None):
        name = name if name else self.__class__.__name__
        self.gases = gases
        if gases is None:
            self.gases = []
        """Gases in atmosphere to take into account in the chemistry."""
        super().__init__(name)

    def build(self, atmosphere):
        """General function that will be called to compute the chemistry after :attr:`atmosphere` has been initialized. It iterates over :attr:`gases` by calling :func:`compute_vmr` on each gas.

        Args:
            atmosphere (:class:`~pytmosph3r.atmosphere.altitudeatmosphere.AltitudeAtmosphere`): Altitude-based atmosphere in which to compute the volume mixing ratios of :attr:`gases`.
            input_atmosphere (:class:`~pytmosph3r.atmosphere.inputatmosphere.InputAtmosphere`, optional): Input atmosphere if you need it (with input mix_ratios for example).
        """
        if atmosphere.gas_mix_ratio is not None and self.gases is not None and len(self.gases):
            self.warning("Gases [%s] in atmosphere. Overriding %s." % (list(atmosphere.gas_mix_ratio.keys()), self.gases))

        self.atmosphere = atmosphere
        if self.gases is None:
            try:
                self.gases = atmosphere.gas_mix_ratio
            except:
                raise ValueError("No gases defined. Either define some in the atmosphere or in the chemistry module.")
        if isinstance(self.gases, str):
            self.gases = [self.gases]
        try:
            self.gases = self.gases.flatten() # ensure 1D list
        except:
            pass

        if atmosphere.gas_mix_ratio is None:
            atmosphere.gas_mix_ratio = {}
        self.input_vmr = atmosphere.gas_mix_ratio.copy()

        for gas in self.gases:
            mix_ratio = np.ones(shape=atmosphere.shape)
            if gas in atmosphere.gas_mix_ratio.keys():
                try:
                    mix_ratio *= atmosphere.gas_mix_ratio[gas]
                except TypeError:
                    self.error("Input VMR of %s cannot be used in chemistry. Maybe a background gas?"%gas)
            atmosphere.gas_mix_ratio[gas] = self.compute_vmr(gas, mix_ratio)

    def compute_vmr(self, gas, mix_ratio):
        """This function can be overridden to compute the volume mixing ratio of a gas :attr:`gas` using :attr:`mix_ratio`, initialized to an array with the :attr:`~pytmosph3r.Grid3D.shape` of the atmosphere.

        Args:
            gas (str): Name of the gas
            mix_ratio (array, np.ndarray): Array full of ones of shape :attr:`~pytmosph3r.Grid3D.shape`. The array is filled with the values in the atmosphere is the gas was already present, or else ones.
        """
        raise NotImplementedError

    @property
    def shape(self):
        return self.atmosphere.shape

    def inputs(self):
        return ["gases", "type"]
