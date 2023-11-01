from abc import ABC

import netCDF4 as nc
import numpy as np

from pytmosph3r.log import Logger
from pytmosph3r.util.util import mol_key
from .io import Input, Output


class ncInput(Input):
    def __init__(self, filename):
        Logger.__init__(self, 'ncInput')
        super().__init__(filename)

    def _openFile(self):
        self.f = nc.Dataset(self.filename)

    def keys(self, path="."):
        return self.f.variables

    def getclass(self, path):
        return self.f[path].description

    def get(self, path):
        raise NotImplementedError


class ncOutput(Output, ncInput):
    def __init__(self, filename, append=False):
        Logger.__init__(self, 'ncOutput')
        Output.__init__(self, filename, append)

        self.group_func = nc.Group.createGroup
        self.group_class = ncGroup

    def getclass(self, path):
        raise NotImplementedError

    def _openFile(self):
        self.f = nc.Dataset(self.filename, mode="w")
        self.f.description = "NETCDF4_CLASSIC data model, file format classic"

    def createDimension(self, *args, **kwargs):
        return self.f.createDimension(*args, **kwargs)

    def createVariable(self, *args, **kwargs):
        return self.f.createVariable(*args, **kwargs)

    def write_model(self, model, output=None, radius_scale: float = 1.):
        from ..atmosphere.altitudeatmosphere import AltitudeAtmosphere

        if model.atmosphere is None and output is None:
            model.build()

        if output is not None:
            atmosphere = AltitudeAtmosphere(model)
            atmosphere.__dict__ = output["atmosphere"]
        else:
            atmosphere = model.atmosphere

        grid = atmosphere.grid
        radius = model.planet.radius*radius_scale

        n_vertical = int(grid.n_vertical)
        n_latitudes = int(grid.n_latitudes)
        n_longitudes = int(grid.n_longitudes)+1
        n_inter = int(grid.n_vertical+1)
        n_index = 100

        self.f.createDimension('Time', None)
        self.f.createDimension('index', n_index)
        self.f.createDimension('latitude', n_latitudes)
        self.f.createDimension('longitude', n_longitudes)
        self.f.createDimension('interlayer', n_inter)
        self.f.createDimension('altitude', n_vertical)

        try:
            self.f.createDimension('wavenumber', len(model.spectrum.wns))
            spectrum = True
        except:
            self.warning("No spectrum to write.")
            spectrum = False

        Time = self.f.createVariable('Time', 'f4', ('Time',))
        Time.units = "days since 0000-00-0 00:00:00"

        controle = self.f.createVariable('controle', 'f8', ('index',))

        latitude = self.f.createVariable('latitude', 'f8', ('latitude',),)
        latitude.units = 'degrees_north'

        longitude = self.f.createVariable('longitude', 'f8', ('longitude',))
        longitude.units = 'degrees_east'

        if model.transmission is None and model.lightcurve is None:
            altitude = self.f.createVariable('altitude', 'f8', ('altitude', 'latitude', 'longitude'))
            if spectrum and hasattr(model.emission, 'raw_flux'):
                flux = self.f.createVariable('flux', 'f8', ('latitude', 'longitude', 'wavenumber'))
                wavenumber = self.f.createVariable('wavenumber', 'f8', ('wavenumber',))
        else:  # transmission mode has one altitude-based grid
            altitude = self.f.createVariable('altitude', 'f8', ('altitude',))

        altitude.units = "km"
        altitude.positive = "up"

        p = self.f.createVariable('p', 'f8',
                                  ('Time', 'altitude', 'latitude', 'longitude',))
        ps = self.f.createVariable('ps', 'f8',
                                   ('Time', 'latitude', 'longitude',))
        temp = self.f.createVariable('temp', 'f8',
                                     ('Time', 'altitude', 'latitude', 'longitude',))

        Time[:] = 1

        controle[:] = np.zeros(n_index, dtype=int)
        controle[0] = n_longitudes-1
        controle[1] = n_latitudes-1
        controle[2] = n_vertical
        controle[4] = model.planet.radius
        controle[6] = model.planet.surface_gravity

        try:
            controle[7] = atmosphere.molar_mass
        except:
            self.warning("controle[7] set as the mean of the molar mass 'molar_mass'.")
            controle[7] = np.mean(atmosphere.molar_mass)

        latitude[:] = np.degrees(grid.mid_latitudes)
        longitude[:-1] = np.degrees(grid.mid_longitudes)

        if grid.to_east:  # increasing
            longitude[-1] = longitude[0] + 360
        else:  # decreasing
            longitude[-1] = longitude[0] - 360

        if model.transmission is None and model.lightcurve is None:
            input_atm = model.emission_atmosphere
            altitude[:, :, :-1] = radius + atmosphere.altitude
            altitude[:, :, -1] = radius + atmosphere.altitude[..., 0]
            if spectrum and hasattr(model.emission, 'raw_flux'):
                flux[:, :-1] = model.emission.raw_flux
                flux[:, -1] = model.emission.raw_flux[:, 0]
                wavenumber[:] = model.spectrum.wns
        else:
            input_atm = model.input_atmosphere
            altitude[:] = radius + atmosphere.altitude

        p[0, :, :, :-1] = atmosphere.pressure
        p[0, :, :, -1] = atmosphere.pressure[:, :, 0]
        ps[0, :, :-1] = input_atm.ps
        ps[0, :, -1] = input_atm.ps[..., 0]

        temp[0, :, :, :-1] = atmosphere.temperature
        temp[0, :, :, -1] = atmosphere.temperature[:, :, 0]

        self.write_mol_dict(atmosphere.gas_mix_ratio, model.gas_dict)
        self.write_mol_dict(atmosphere.aerosols, model.aerosols_dict, "ice")

    def write_mol_dict(self, mol_list, mol_dict, mol_type="vap"):
        """Write list of molecules (gas or aerosols)."""

        for mol in mol_list.keys():
            if isinstance(mol_list[mol], dict):  # aerosols (dict {mmr, reff,...})
                for data in mol_list[mol].keys():
                    extension = "_" + data
                    if data == "mmr":
                        extension = ""
                    self.write_mol(mol_list[mol][data], mol_dict, mol, mol_type, extension)
            else:  # gas (volume mix ratio)
                self.write_mol(mol_list[mol], mol_dict, mol, mol_type)

    def write_mol(self, mol_data, mol_dict, mol, mol_type="vap", data=""):
        """Write one molecule."""
        key = mol_key(mol_dict, mol, mol_type, data)

        if isinstance(mol_data, str):
            mol_var = self.f.createVariable(key, f'S{len(mol_data)}', 'Time')
        else:
            mol_var = self.f.createVariable(key, 'f8', ('Time', 'altitude', 'latitude', 'longitude',))

        mol_var.title = key

        if mol_type == "vap":
            mol_var.units = "m^3/m^3"
        elif data == "_reff":
            mol_var.units = "m"
        elif data in ("_mmr", ""):
            mol_var.units = "kg/kg"
        elif data == "_condensate_density":
            mol_var.units = "kg/m^3"

        if isinstance(mol_data, (float, str)):
            mol_var[0] = mol_data
        else:
            mol_var[0, :, :, :-1] = mol_data
            try:
                mol_var[0, :, :, -1] = mol_data[:, :, 0]
            except:
                mol_var[0, :, :, -1] = mol_data

    def get(self, path):
        raise NotImplementedError


class ncGroup(ncOutput, ABC):
    def __init__(self, f):
        super().__init__('ncGroup')
        self.f = f

    def get(self, path):
        pass


def write_netcdf(filename, model, radius_scale: float = 0.):
    """Write a netCDF file using :attr:`model`, which can be viewed using ncview, ParaView, etc.

    Args:
        filename (string): Name of the netCDF output file.
        model (:class:`~pytmosph3r.model.model.Model`): Model to write.
        radius_scale (float): Scale for planet radius (for visualization purposes). ncview prefers a scale of 0.
    """

    with ncOutput(filename) as nc:
        nc.write_model(model, radius_scale=radius_scale)
