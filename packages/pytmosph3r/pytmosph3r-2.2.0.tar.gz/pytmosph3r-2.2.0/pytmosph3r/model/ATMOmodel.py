import netCDF4 as nc
import numpy as np

from .model import Model
from ..atmosphere import InputAtmosphere
from ..grid import Grid3D


def find_mol(mol, mols):
    found_mol = False
    for imol, name in enumerate(mols):
        if mol == name.tostring().decode('utf-8').strip():
            found_mol = True
            break
    if found_mol:
        return imol
    return None

class ATMOModel(Model):
    """Model reading from a netcdf file generated via ATMO."""
    def __init__(self, pt_file=None, chem_file=None, gases=None, var_dict=None, is_2d=None, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        
        self.pt_file = pt_file
        self.chem_file = chem_file
        self.gases = gases if gases is not None else []
        self.var_dict_2d = dict(t='temperature_2d',
                        p='pressure_2d',
                        u='wind_2d',
                        v='dwind_2d',
                        w='windz_2d')
        self.var_dict = dict(t="temperature",
                             p="pressure")
        if var_dict is not None:
            if is_2d:
                self.var_dict_2d.update(var_dict)
            else:
                self.var_dict.update(var_dict)

    def inputs(self):
        return Model.inputs(Model) + Model.inputs(self)

    def read_data(self):
        pt_file=nc.Dataset(self.pt_file)
        chem_file=nc.Dataset(self.chem_file)
        if 'temperature_2d' in pt_file.variables:
            # last longitude is a repeat
            temperature  = pt_file.variables[self.var_dict_2d["t"]][...].T[::-1][:, None, :-1]
            pressure  = pt_file.variables[self.var_dict_2d["p"]][...].T[::-1][:, None, :-1]
            u  = pt_file.variables[self.var_dict_2d["u"]][...].T[::-1][:, None, :-1]
            v = pt_file.variables[self.var_dict_2d["v"]][...].T[::-1][:, None, :-1]
            w = pt_file.variables[self.var_dict_2d["w"]][...].T[::-1][:, None, :-1]
            winds = np.stack((u,v,w), axis=-1)
        else:
            temperature  = pt_file.variables[self.var_dict["t"]][:, None, None]
            pressure  = pt_file.variables[self.var_dict["p"]][:, None, None]
            winds = None

        grid = Grid3D(*pressure.shape)
        pressure *= .1  # conversion Barye to Pascal
        
        gas_mix_ratio = {}
        for gas in self.gases:
            imol = find_mol(gas, chem_file.variables['molname'])
            if imol is not None:
                gas_mix_ratio[gas] = chem_file.variables['abundances'][imol]

        self.input_atmosphere = InputAtmosphere(grid=grid, pressure=pressure, temperature=temperature, gas_mix_ratio=gas_mix_ratio, winds=winds)
