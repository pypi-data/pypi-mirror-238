import numpy as np

from .chemistry import Chemistry


class Parmentier2018Dissociation(Chemistry):
    """Chemistry model based on :cite:`parmentier2018`.

    A few notes: the dissociation of :math:`H_2` will create :math:`H` and :math:`He` automatically to fill the atmosphere.
    If you do not have cross-section data for them, you should also add them to the list of `transparent_gases`.

    Args:
        gases (:obj:`dict`) : List of gases for which to consider dissociation, and eventually override the coefficients associated with each gas. Example: :code:`{'H2O':(2.,2.83,15.9),'H2':True}`. This overrides the coefficients for :math:`H_2O` but uses the default values for :math:`H_2`.
        T_min (float) : Minimum temperature for which to compute dissociation.
    """

    wasp121b_coeffs = {
    'H2':(1, 2.41, 6.5),
    'H2O':(2, 4.83, 15.9),
    'TiO':(1.6, 5.94, 23.0),
    'VO':(1.5, 5.40, 23.8),
    'H-':(0.6, -0.14, 7.7),
    'Na':(0.6, 1.89, 12.2),
    'K':(0.6, 1.28, 12.7),
    }
    wasp121b_deep_abundances_log = {
    'H2':-0.1,
    'H2O':-3.3,
    'TiO':-7.1,
    'VO':-9.2,
    'H-':-8.3,
    'Na':-5.5,
    'K':-7.1,
    }

    def __init__(self, gases=None, T_min=0, H2_dissociation=None, ratio_HeH2=None):
        super().__init__(self.__class__.__name__)
        self.gases = {}
        self.deep_abundances = {}
        self.T_min = T_min
        self.H2_dissociation = H2_dissociation
        """H2 dissociation will create H. He is also added (see :attr:`ratio_HeH2`).
        """
        self.ratio_HeH2 = ratio_HeH2
        """When H2 dissociates, we add He using this ratio to define their deep abundances. :attr:`ratio_HeH2` = x_He_deep / x_H2_deep.
        """
        if gases is None:
            return
        if isinstance(gases, str):
            gases = [gases]
        for gas in gases:
            self.gases[gas] = self.wasp121b_coeffs[gas]
            value = True
            if isinstance(gases, (dict)):
                value = gases[gas]
            if isinstance(value, (tuple, list, np.ndarray)):
                self.gases[gas] = value

    def build(self, atmosphere):
        super().build(atmosphere)

        if self.H2_dissociation:
            '''Take into account H2 dissociation by diluting all gases and add H into the mix.'''
            if self.ratio_HeH2 is None:
                self.ratio_HeH2 = 0
                self.warning("ratio_HeH2 not defined. x_He = 0.")
            total_vmr = sum(atmosphere.gas_mix_ratio.values())
            total_input_vmr = sum(self.input_vmr.values())
            x_H2_solar = (1-total_input_vmr)/(1+self.ratio_HeH2)
            self.gases["H2"] = self.wasp121b_coeffs["H2"]
            atmosphere.gas_mix_ratio["H2"] = self.compute_vmr("H2", np.full(self.shape, x_H2_solar))
            atmosphere.gas_mix_ratio["H"] = 2*(1-atmosphere.gas_mix_ratio["H2"]*(1+self.ratio_HeH2)-total_vmr)/(2+self.ratio_HeH2)
            atmosphere.gas_mix_ratio["He"] = 1 - sum(atmosphere.gas_mix_ratio.values())
            return

    def compute_vmr(self, gas, mix_ratio):
        T = self.atmosphere.temperature
        P = self.atmosphere.pressure
        if np.alltrue(np.equal(mix_ratio, 1)):
            mix_ratio *= np.power(10, (self.wasp121b_deep_abundances_log[gas]))
        self.input_vmr[gas] = np.copy(mix_ratio)

        idx = T > self.T_min
        mix_ratio[idx] = (1. / (np.power(1. / np.sqrt(mix_ratio[idx]) + 1. /
                    np.sqrt((np.power(10, self.gases[gas][1]*1e4 / T[idx] - self.gases[gas][2]))
                    * (np.power((P[idx]*1e-5), self.gases[gas][0]))), 2)))
        return mix_ratio

    def inputs(self):
        return Chemistry.inputs(Chemistry) + ["T_min"]
