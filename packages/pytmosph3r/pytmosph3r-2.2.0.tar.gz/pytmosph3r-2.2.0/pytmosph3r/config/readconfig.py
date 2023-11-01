"""
@author: A. Falco

Transform config file into a model, forked from TauREX 3 (https://github.com/ucl-exoplanets/TauREx3_public/blob/master/taurex/parameter/parameterparser.py).
"""
import os

import configobj
import exo_k as xk

from pytmosph3r.log.logger import Logger
from pytmosph3r.util.memory import MemoryUtils
from pytmosph3r.util.pkg_dir import pkg_dir
from .factory import create_obj
from ..opacity import Opacity


class Config(Logger):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self._read = False

    def transform(self, section, key):
        val = section[key]
        newval = val
        if isinstance(val, list):
            try:
                newval = list(map(float,val))
            except:
                pass
        elif isinstance(val, (str)):
            if val.lower() in ['true']:
                newval = True
            elif val.lower() in ['false']:
                newval = False
            else:
                try:
                    newval = float(val)
                except:
                    pass
        section[key]=newval
        return newval

    def setup_globals(self):
        if 'Global' in self.config:
            try:
                pkg_dir.relative_dir = os.path.join(pkg_dir.root_dir, self.config['Global']['relative_dir'])
                self.info("Relative directory set to: %s"%pkg_dir.relative_dir)
            except KeyError:
                self.warning('Relative directory automatically set to root folder of pytmosph3r (%s)'%pkg_dir.relative_dir)
            try:
                MemoryUtils.margin = self.config['Global']['memory_margin']
                self.info("Setting memory margin to %s"%MemoryUtils.margin)
            except KeyError:
                pass

        convert =  True
        log_interp =  False
        _remove_zeros =  True
        try:
            opacity_path = self.config['Exo_k']['xsec_path']
            if isinstance(opacity_path, list):
                for i, path in enumerate(opacity_path):
                    opacity_path[i] = self.search_path(path)
            else:
                opacity_path = self.search_path(opacity_path)
            self.info("Exo_k: xsec search path = %s"%opacity_path)
        except KeyError:
            self.warning('Exo_k: xsec search path automatically set to root folder of Pytmosph3R.')
            opacity_path = pkg_dir.relative_dir
        try:
            cia_path = self.search_path(self.config['Exo_k']['cia_path'])
            self.info("Exo_k: cia search path = %s"%cia_path)
        except KeyError:
            self.warning('Exo_k: cia search path automatically set to root folder of Pytmosph3R.')
            cia_path = pkg_dir.relative_dir
        try:
            aerosol_path = self.search_path(self.config['Exo_k']['aerosol_path'])
            self.info("Exo_k: aerosols search path = %s"%aerosol_path)
        except KeyError:
            self.warning('Exo_k: aerosols search path automatically set to root folder of Pytmosph3R.')
            aerosol_path = pkg_dir.relative_dir
        try:
            convert = self.config['Exo_k']['convert']
            self.info("Exo_k: convert mks = %s"%convert)
        except KeyError:
            self.warning('Exo_k: Converting mks by default.')
        try:
            log_interp = self.config['Exo_k']['log_interp']
            self.info("Exo_k: log interpolation = %s"%log_interp)
        except KeyError:
            self.warning('Exo_k: Log interpolation.')
        try:
            _remove_zeros = self.config['Exo_k']['_remove_zeros']
            self.info("Exo_k: Remove zeros = %s"%_remove_zeros)
        except KeyError:
            self.warning('Exo_k: Remove zeros by default.')
        try:
            if isinstance(opacity_path, list):
                xk.Settings().set_search_path(*opacity_path)
            else:
                xk.Settings().set_search_path(opacity_path)
            xk.Settings().set_cia_search_path(cia_path)
            xk.Settings().set_aerosol_search_path(aerosol_path)
        except:
            raise Exception("Exo_k: one of the paths does not exist:\n %s\n %s\n %s\n OR you may not be up-to-date on exo_k."%(opacity_path, cia_path, aerosol_path))
        xk.Settings().set_mks(convert)
        xk.Settings().set_log_interp(log_interp)
        Opacity._remove_zeros = _remove_zeros

    def read(self,filename):
        import os.path
        if not os.path.isfile(filename):
            raise Exception('Input file {} does not exist'.format(filename))
        self._raw_config = configobj.ConfigObj(filename)
        self.debug('Raw Config file {} parameters are: {}'.format(filename,self._raw_config))
        self._raw_config.walk(self.transform)
        self.config = self._raw_config.dict()
        self.debug('Config file is {}'.format(self.config))

    def generate_model(self):
        planet = self.generate_class('Planet')
        if 'Star' not in self.config:
            self.warning("No star in config file. Default star will be used.")
        star  = create_obj(self.config, 'Star') # always create a star
        grid = self.generate_class('Grid')
        input_atmosphere = self.generate_class('Atmosphere', grid=grid)
        if 'Rays' in self.config:
            raise configobj.ConfigObjError("Outdated configuration file. Please refer to the documentation and split [Rays] into [RadiativeTransfer] and [Observer].")
        if 'RadiativeTransfer' in self.config:
            self.error("[RadiativeTransfer] is obsolete, replace it with either [Transmission] or [Emission].")
            if "type" in self.config["RadiativeTransfer"] and self.config["RadiativeTransfer"]["type"] == "emission":
                self.config["Emission"] = self.config["RadiativeTransfer"]
                self.warning("Replacing automatically [RadiativeTransfer] with [Emission].")
            else:
                self.config["Transmission"] = self.config["RadiativeTransfer"]
                self.warning("Replacing automatically [RadiativeTransfer] with [Transmission].")

        observer = self.generate_class('Observer')
        opacity = create_obj(self.config, 'Opacity') # always create opacity
        transmission = self.generate_class('Transmission')
        emission = self.generate_class('Emission')
        lightcurve = self.generate_class('Lightcurve')
        phasecurve = self.generate_class('Phasecurve')
        parallel = self.generate_class('Parallel')
        model = self.generate_class('Model', planet=planet, star=star,
                                    input_atmosphere=input_atmosphere,
                                    observer=observer, opacity=opacity, transmission=transmission,
                                    emission=emission,
                                    lightcurve=lightcurve,
                                    phasecurve=phasecurve,
                                    parallel=parallel)
        return model

    def generate_class(self, name, *args, **kwargs):
        if name in self.config:
            return create_obj(self.config, name, *args, **kwargs)
        else:
            return None
