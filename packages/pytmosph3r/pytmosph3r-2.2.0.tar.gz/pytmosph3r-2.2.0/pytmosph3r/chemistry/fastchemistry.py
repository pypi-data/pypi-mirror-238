import tempfile
from shutil import copyfile

from pytmosph3r.log import Logger
from pytmosph3r.util.constants import KBOLTZ
from .chemistry import Chemistry

try:
    from pytmosph3r.external.fastchem import PyFastChem  # noqa
except ModuleNotFoundError:
    pass


def fastchem_name(gas):
    char = 0
    while char < len(gas):
        if gas[char].isupper() and (char >= len(gas)-1  or gas[char+1].isupper()):
            gas = gas[:char+1]+"1"+gas[char+1:]
        char = char+1
    return gas

def create_tempfile(name="tmp"):
    tmpfile = tempfile.NamedTemporaryFile(mode='w+b', prefix=name, dir=tempfile.gettempdir(), delete=False)
    tmpfile.close()
    return tmpfile.name

class FastChemistry(Chemistry):
    """Chemistry model based on FastChem: https://github.com/exoclime/FastChem

    Args:
        gases (:obj:`list`) : List of gases in the atmosphere
        filename (str) : The path to the `parameter file used by FastChem <https://github.com/exoclime/FastChem/blob/master/input/parameters.dat>`_.
    """
    def __init__(self, gases=None, filename=None):
        super().__init__(self.__class__.__name__, gases)
        self.search_path(filename)
        """FastChem parameter file."""

    def build(self, atmosphere, input_atmosphere=None):
        with open(self.filename) as f:
            data = f.readlines()
            x_file = Logger("")
            x_file.search_path(data[1].rstrip('\n'))
            self.abundances_file = x_file.filename
            x_file.search_path(data[4].rstrip('\n'))
            self.elements_data_file = x_file.filename
            x_file.search_path(data[7].rstrip('\n'))
            self.species_data_file = x_file.filename
        data[1] = self.abundances_file+"\n"
        data[4] = self.elements_data_file+"\n"
        data[7] = self.species_data_file+"\n"

        self.tmp_file = create_tempfile('fastchem_params_')
        copyfile(self.filename, self.tmp_file)
        with open(self.tmp_file, 'w') as f:
            f.writelines(data)

        self.info('Calling Fastchem...')
        try:
            self.fastchem = PyFastChem(self.tmp_file, 0)
        except:
            raise ImportError("Could not find FastChem. Please set FASTCHEM_DIR=/path/to/fastchem, and re-install Pytmosph3R.")

        self.fastchem_output = self.fastchem.calcDensities(atmosphere.temperature, atmosphere.pressure)
        self.info('Done')

        super().build(atmosphere)

    def compute_vmr(self, gas, mix_ratio):
        T, P, densities, h_densities, mean_mol_weight = self.fastchem_output
        total_density = 10*self.atmosphere.pressure/(KBOLTZ*1e7 * self.atmosphere.temperature) # use fastchem units (P in dyn cm-2, kB in erg⋅K−1)
        mol_id = self.fastchem.getSpeciesIndex(fastchem_name(gas))
        return densities[mol_id].reshape(self.atmosphere.shape)/total_density

    def inputs(self):
        return Chemistry.inputs(Chemistry) + ["filename"]
