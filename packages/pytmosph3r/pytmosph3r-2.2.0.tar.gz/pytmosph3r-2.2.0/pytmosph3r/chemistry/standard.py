from .chemistry import Chemistry


class StandardRatioHeH2(Chemistry):
    """Complete the atmosphere in He and H2 using a ratio_HeH2.

    Args:
        gases (:obj:`dict`): List of gases which are consider in the simulation.
        ratio_HeH2 (float): Ratio between the mixing ratio of He and H2. Exemple: ratio_HeH2 = 0.2577 (solar abundance)
    """

    def __init__(self, gases=None, ratio_HeH2=None):
        super().__init__(self.__class__.__name__)
        self.gases = gases
        self.ratio_HeH2 = ratio_HeH2

    def compute_vmr(self, gas, mix_ratio):
        return mix_ratio


    def build(self, atmosphere):
        super().build(atmosphere)
        total_vmr = sum(atmosphere.gas_mix_ratio.values())
        atmosphere.gas_mix_ratio["H2"] = (1-total_vmr)/(1+self.ratio_HeH2)
        atmosphere.gas_mix_ratio["He"] = 1 - sum(atmosphere.gas_mix_ratio.values())
        return

    def inputs(self):
        return Chemistry.inputs(Chemistry) + ["ratio_HeH2"]
