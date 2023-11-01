import numpy as np

# TODO: remove when new exo_k version is released
try:
    from exo_k.aerosol.util_aerosol import mmr_to_number_density, mmr_to_number_density_ratio # noqa
except ModuleNotFoundError:
    from exo_k.util import mmr_to_number_density, mmr_to_number_density_ratio  # noqa

from pytmosph3r.util.constants import RGP
from pytmosph3r.util.util import get, init_array


class PrepareAerosols:
    """Transform aerosols (from mmr, reff and condensate_density) to a format suitable to exo_k (reff and nb_density).
    """
    def __init__(self, model, atm, size):
        """Initialize the aer_reff_densities to a exo_k-compatible format.

        Args:
            model (:class:`~pytmosph3r.model.Model`): The model from which to extract some data.
            atm (:class:`~pytmosph3r.atmosphere.Atmosphere`): The atmosphere from which to extract some data.
            size (int): Size of the data (reff & nb_density) for each molecule.
        """
        self.model = model
        self.atmosphere = atm
        self.aer_reff_densities = {}
        """Dictionary that should be compatible with exo_k. Its keys should be the aerosol names and the values should be lists containing 2 floats (or arrays) as values. The values are the particle effective radii and number densities.  See `absorption_coefficient()`_ in the doc of exo_k:

        .. _absorption_coefficient():
        http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/adatabase/index.html?highlight=absorption_coefficient#exo_k.adatabase.Adatabase.absorption_coefficient
        """
        if atm.aerosols:
            for aerosol in atm.aerosols.keys():
                try:
                    key = atm.aerosols[aerosol]["optical_properties"]
                except:
                    key = self.model.aerosol(aerosol)

                self.aer_reff_densities[key] = np.empty(2, dtype=object)
                self.aer_reff_densities[key][0] = init_array(atm.aerosols[aerosol]["reff"], size)
                self.aer_reff_densities[key][1] = np.full((size), np.nan)

    def compute(self, i, coordinates):
        """Compute the value of aer_reff_densities at :attr:`coordinates`, which will be stored at index :attr:`i`. The input :attr:`aerosols` dictionary should contain a MMR :attr:`mmr` (in `kg/kg`), and effective radius :attr:`reff` (in `m`), and :attr:`condensate_density` (in :math:`kg/m^3`).

        Args:
            i (int, slice): index.
            coordinates (tuple): cell coordinates.

        Returns:
            dict: A dictionary with aerosol names as keys and lists containing 2 floats (or arrays) as values. The values are the particle effective radii and number densities.
        """
        atm = self.atmosphere
        gas_density = atm.molar_mass[coordinates] * atm.pressure[coordinates] / (RGP * atm.temperature[coordinates])
        for aerosol in atm.aerosols.keys():
            try:
                key = atm.aerosols[aerosol]["optical_properties"]
            except:
                key = self.model.aerosol(aerosol)

            mmr = get(atm.aerosols[aerosol]['mmr'], coordinates)
            reff = get(atm.aerosols[aerosol]['reff'], coordinates)
            condensate_density = get(atm.aerosols[aerosol]['condensate_density'], coordinates)
            # nb_density = mmr_to_number_density(mmr, gas_density, reff, condensate_density)
            nb_density = mmr_to_number_density_ratio(mmr, atm.molar_mass[coordinates], reff, condensate_density)

            if isinstance(self.aer_reff_densities[key][0], np.ndarray):
                self.aer_reff_densities[key][0][i] = reff
            self.aer_reff_densities[key][1][i] = nb_density
        return self.aer_reff_densities