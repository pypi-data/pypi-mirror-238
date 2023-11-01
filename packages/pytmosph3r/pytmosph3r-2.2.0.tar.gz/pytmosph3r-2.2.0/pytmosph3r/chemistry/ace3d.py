import numpy as np

from .chemistry import Chemistry

try:
    import taurex # noqa
    from taurex.model import TransmissionModel # noqa
    from taurex.data.profiles.temperature.temparray import TemperatureArray # noqa
    from taurex_ace import ACEChemistry # noqa
except ModuleNotFoundError:
    pass


class ACE3D(Chemistry):
    """Use ACE chemistry on each vertical column. See taurex model (https://taurex3-public.readthedocs.io/en/latest/user/taurex/chemistry.html).
    Agúndez, M., Venot, O., Iro, N., et al. 2012, AandA, 548,A73

    Args:
        metallicity (float): Stellar metallicity in solar units
        co_ratio (float): C/O ratio
    """
    def __init__(self, gases=None, metallicity=1, co_ratio=0.457):
        super().__init__(self.__class__.__name__, gases)
        self.metallicity = metallicity
        self.co_ratio = co_ratio

    def inputs(self):
        return super().inputs() + ["metallicity", "co_ratio"]

    def build(self, atmosphere):
        self.atmosphere = atmosphere
        taurex.log.disableLogging()

        for lat,lon in self.atmosphere.grid.walk([1,2]):
            # pytmosph3r to taurex
            tp = TemperatureArray(tp_array=self.atmosphere.temperature[:, lat, lon], p_points=self.atmosphere.pressure[:, lat, lon], reverse=False)

            chemistryACE = ACEChemistry(metallicity=self.metallicity, co_ratio=self.co_ratio)

            #transmission model with equilibrium chemistry
            tm_eq = TransmissionModel(
                        temperature_profile=tp,
                        chemistry=chemistryACE,
                        atm_min_pressure=self.atmosphere.pressure[:, lat,lon].min(),
                        atm_max_pressure=self.atmosphere.pressure[:, lat,lon].max(),
                        nlayers=self.atmosphere.n_vertical)

            tm_eq.build()

            # taurex to pytmosph3r
            for i, gas in enumerate(tm_eq.chemistry.activeGases):
                if gas not in self.gases:
                    continue
                if gas not in atmosphere.gas_mix_ratio.keys():
                    atmosphere.gas_mix_ratio[gas] = np.ones(shape=atmosphere.shape)
                atmosphere.gas_mix_ratio[gas][:, lat,lon] = tm_eq.chemistry.activeGasMixProfile[i]
            for i, gas in enumerate(tm_eq.chemistry.inactiveGases):
                if gas not in self.gases:
                    continue
                if gas not in atmosphere.gas_mix_ratio.keys():
                    atmosphere.gas_mix_ratio[gas] = np.ones(shape=atmosphere.shape)
                atmosphere.gas_mix_ratio[gas][:, lat,lon] = tm_eq.chemistry.inactiveGasMixProfile[i]
        return
                      