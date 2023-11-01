import os
from copy import copy
from typing import Optional

import astropy.units as u
import exo_k as xk
import numpy as np
from exo_k.util.cst import C_LUM

from pytmosph3r.log import Logger
from pytmosph3r.observations import *
from pytmosph3r.planetary_system import *
from pytmosph3r.util.util import get_attributes, mol_key, update_dict
from ..atmosphere import InputAtmosphere
from ..interface.hdf5 import write_hdf5
from ..opacity import Opacity


class Model(Logger):
    """Main model structure which plays the role of the puppeteer.
    The main function are :func:`build`, which initializes some of the classes once you are sure of your input data (computes altitude for example), and :math:`run`, which basically computes everything (transit depth/emission, ..).

    All 'property' attributes are derived from :class:`~pytmosph3r.AltitudeAtmosphere`.
    """

    def __init__(self,
                 output_file: str = None,
                 n_vertical: Optional[int] = None,
                 noise=None,
                 interp=None,
                 gas_dict=None,
                 aerosols_dict=None,

                 input_atmosphere: Optional[InputAtmosphere] = None,
                 opacity: Optional[Opacity] = None,

                 planet: Optional[Planet] = None,
                 star: Optional[Star] = None,
                 observer: Optional[Observer] = None,
                 orbit: Optional[Orbit] = None,

                 radiative_transfer=None,
                 transmission: Optional[Transmission] = None,
                 emission: Optional[Emission] = None,
                 lightcurve: Optional[Lightcurve] = None,
                 phasecurve: Optional[Phasecurve] = None,
                 parallel=None,
                 **kwargs,
                 ):
        """Main class to control all submodules. Here you control *everything*.

        Args:
            output_file (str) : HDF5 output filename.
            n_vertical (int) : Number of vertical layers for the altitude-based  :py:attr:`atmosphere` (100 by default).

            noise (float, array) : If a float, it gives the width of the errorbar (the output spectrum will be noised with a normal distribution scaled with this value). if an array, the noise is simply added to the spectrum. 0 by default.

            interp : Interpolation of the pressure in the transformation of the input atmosphere into the altitude-based :py:attr:`atmosphere`. It may be either one the parameters to pass to scipy.interpolate.interp1d function (see 'kind' parameters) or False (default option). If it is set to false, the pressure will be recomputed using :class:`~pytmosph3r.atmosphere.AltitudeAtmosphere.compute_pressure`.

            gas_dict : Dictionary containing the names of the gas and the keys to find them in the input file (diagfi, hdf5). Defaults to {'H2O': 'h2o_vap'}.

            aerosols_dict : Similar to :py:attr:`gas_dict`, it's a dictionary containing the names of the aerosols (and their characteristics) and the keys to find them in the input file (diagfi, hdf5). If only the name of the molecule is given, the key is assumed to represent the MMR (mass molecular ratio in kg/kg). Example : {'H2O': 'h2o_ice', 'H2O_reff': 'H2Oice_reff'}.

            planet (:class:`~pytmosph3r.planet.Planet`) : Planet object.

            star (:class:`~pytmosph3r.star.Star`) : Star object (not optional).

            input_atmosphere (:class:`~pytmosph3r.atmosphere.inputatmosphere.InputAtmosphere`) : Input atmospheric grid based on levels (and inter-layers).

            observer (:class:`~pytmosph3r.rays.Observer`) : Position of the observer (latitude, longitude).

            opacity (:class:`~pytmosph3r.opacity.Opacity`) : Opacity parameters.

            transmission (:class:`~pytmosph3r.transmission.Transmission`) : Transmission parameters.
            emission (:class:`~pytmosph3r.emission.Emission`) : Emission parameters.
            lightcurve (:class:`~pytmosph3r.lightcurve.Lightcurve`) : Lightcurve parameters.
            phasecurve (:class:`~pytmosph3r.phasecurve.Phasecurve`) : Phasecurve parameters.

            kwargs (dict) : You can use set/override other parameters using this.
        """
        super().__init__()

        self.filename = None
        self.output_file = output_file
        self.planet = planet
        self.star = star
        self.noise = noise
        self.observer = observer
        self.orbit = orbit

        if isinstance(observer, dict):
            self.warning("You should send an observer.")
            self.observer = Observer(**observer)
        elif not isinstance(observer, Observer):
            self.info(f"Observer type {type(observer)} unknown. Proceed with care...")

        if isinstance(orbit, dict):
            self.warning('You should send an orbit like object.')
            self.orbit = CircularOrbit(**orbit)
        elif not isinstance(orbit, (CircularOrbit, type(None))):
            self.info(f"Orbit type {type(orbit)} unknown. Proceed with care...")

        self.opacity: Optional[Opacity] = opacity

        self._surface = None
        """Only used in Emission."""
        self.transmission = transmission
        self.emission = emission
        self.lightcurve = lightcurve
        self.phasecurve = phasecurve
        if radiative_transfer is not None:
            self.warning("'radiative_transfer' is a deprecated parameter. This will not be supported in the future. Use either 'emission', 'transmission', 'lightcurve' or 'phasecurve' parameters.")
            if isinstance(radiative_transfer, Emission):
                self.emission = radiative_transfer
            elif isinstance(radiative_transfer, Transmission):
                self.transmission = radiative_transfer
            elif isinstance(radiative_transfer, Lightcurve):
                self.lightcurve = radiative_transfer
            elif isinstance(radiative_transfer, Phasecurve):
                self.phasecurve = radiative_transfer

        self.noised_spectrum: Optional[xk.Spectrum] = None
        """Noiseless spectrum."""

        self.input_atmosphere = input_atmosphere

        self.emission_atmosphere = None
        self.transmission_atmosphere = None

        self.n_vertical = n_vertical
        self.interp = interp
        self.gas_dict = gas_dict
        self.aerosols_dict = aerosols_dict

        self.mode_keys = {
            'transmission': 'transmission_spectrum',
            'emission': 'emission_spectrum',
            'lightcurve': 'light_curve',
            'phasecurve': 'phase_curve',
        }
        self.modes = [
            'transmission',
            'lightcurve',
            'emission',
            'phasecurve',
        ]
        """Names of modes, and their order of computation."""

        self.parallel = parallel
        self._stats_file = None
        self._profile = None

        for key, value in kwargs.items():
            self.warning(f'Unknown keys added: `{key}`: `{value}`.')
            self.__dict__[key] = value

    @property
    def default_values(self):
        return {
            'n_vertical': 100,
            'noise': 0,
            'interp': 'log',
            'gas_dict': {},
            'aerosols_dict': {},
            'observer': Observer(),
            'orbit': CircularOrbit(),
            'opacity': Opacity(),
        }

    def outputs(self):
        outputs = ["input_atmosphere", "atmosphere",  "wns", "wnedges",
                   "transmission", "emission", "lightcurve",  "phasecurve",
                   "spectrum_value","spectrum_noised", ]

        return outputs

    @property
    def stats_file(self):
        """File with profiling statistics. Profiling is activated by :func:`start_profiling` and saved in :func:`dump_profiling`.
        Defaults to the same name as `output_file`, with '.prof' as a file extension."""
        if self._stats_file is None:
            self._stats_file = os.path.splitext(self.output_file)[0]+".prof"
        return self._stats_file
    @stats_file.setter
    def stats_file(self, value):
        self._stats_file = value
    
    def start_profiling(self, file=None):
        """Start profiling code. Can specify in which `file` (optional)."""
        import cProfile
        self._profile = cProfile.Profile()
        self._profile.enable()
        if file is not None: 
            self.stats_file = file
       
    def dump_profiling(self, file=None):
        """Save profiling stats in `file` (optional, defaults to `stats_file`). """
        try:
            self._profile.disable()
        except:
            raise KeyError("Profile has not been activated. You should call start_profiling() first.")
        self._profile.create_stats()
        if file is None:
            file = self.stats_file 
        self.info('Recording time stats in %s', file)
        self._profile.dump_stats(file)
    
    @property
    def atmosphere(self):
        if not (self.transmission or self.lightcurve):
            return self.emission_atmosphere
        else:
            return self.transmission_atmosphere

    @atmosphere.setter
    def atmosphere(self, value):
        if not (self.transmission or self.lightcurve):
            self.emission_atmosphere = value
        else:
            self.transmission_atmosphere = value

    @property
    def doppler(self):
        try:
            return self.opacity.doppler
        except:
            return False

    @property
    def grid(self):
        try:
            return self.atmosphere.grid
        except:
            return self.input_atmosphere.grid

    @property
    def shape(self):
        return self.n_layers, self.n_latitudes, self.n_longitudes

    @property
    def n_latitudes(self) -> int:
        return self.grid.n_latitudes

    @property
    def n_longitudes(self) -> int:
        return self.grid.n_longitudes
    @property
    def n_layers(self) -> int:
        return self.grid.n_vertical
    @property
    def n_levels(self) -> int:
        return self.atmosphere.n_levels
    @property
    def altitude(self):
        return self.atmosphere.altitude
    @property
    def pressure(self):
        return self.atmosphere.pressure
    @property
    def temperature(self):
        return self.atmosphere.temperature
    @property
    def molar_mass(self):
        return self.atmosphere.molar_mass
    @property
    def gas_mix_ratio(self):
        return self.atmosphere.gas_mix_ratio
    @property
    def aerosols(self):
        return self.atmosphere.aerosols
    def Rp(self):
        return self.planet.radius
    @property
    def Rs(self):
        return self.star.radius

    @property
    def surface(self):
        """Surface area at each latitude x longitude."""
        if not hasattr(self,"_surface") or self._surface is None:
            # if self.atmosphere is None:
            #     raise AttributeError("The model needs an atmosphere to compute a surface.
            #     Set the 'atmosphere' attribute by using build().")
            self._surface = np.zeros((self.n_latitudes, self.n_longitudes))
            self._surface[:] = np.abs((2*np.pi*self.planet.radius**2
            * (np.sin(self.grid.latitudes[1:])-np.sin(self.grid.latitudes[:-1])) / self.grid.n_longitudes))[:, None]

            assert np.isclose(np.sum(self._surface), 4*np.pi*self.planet.radius**2), "Total surface is not equal to the sum of the surfaces of each grid point (%g != %g)... Report this as a bug."%(np.sum(self._surface), 4*np.pi*self.planet.radius**2)

        return self._surface
    @surface.setter
    def surface(self, value):
        self._surface = value

    def gas(self, gas):
        """Return the key corresponding to :attr:`gas` using user dictionary :attr:`gas_dict`."""
        return mol_key(self.gas_dict, gas, "vap")

    def aerosol(self, aerosol):
        """Return the key corresponding to :attr:`aerosol` using user dictionary :attr:`aerosols_dict`."""
        return mol_key(self.aerosols_dict, aerosol, "ice")

    def read_data(self):
        if self.filename:
            self.warning("%s does not read any data file. %s is ignored."%(self.__class__.__name__, self.filename))

    def override_data_file(self, params):
        """This method allows subclasses to override the data read from data file (HDF5, diagfi, ...)
        """
        self.info("Loading model attributes from config file...")
        for key, value in params.items():
            self.override_file_param(key, value)

    def override_file_param(self, data_name, config):
        """Override an element from the datafile

        Args:
            data_name (string): name of attribute to override
            config (object): object read from config file
        """
        if data_name not in self.__dict__:
            self.error("%s is not initialized in model. Maybe set it to None before calling this method."%data_name)

        if isinstance(config, (int, float, str, list, np.ndarray, tuple)):
            self.__dict__[data_name] = config
            return

        data = self.__dict__[data_name]
        if config is None:
            # if data is None:
            #     self.error("%s needs to be defined at least in data or config file"%data_name)
            return
        if data is None: # no data: take config value
            self.__dict__[data_name] = config
        elif isinstance(data, dict) and isinstance(config, dict):
            data.update(config)
        else:

            # get attributes to copy
            # try:
            attrs = get_attributes(config)
            # except:
            #     try:
            #         if isinstance(config, dict):
            #             attrs = list(config)
            #         else:
            #             attrs = list(config.__dict__)
            #     except:
            #         attrs = [(i, getattr(config, i)) for i in config.inputs()]

            for attr, val in attrs:
                if val is not None:
                    if isinstance(val, dict) and attr in data.__dict__.keys() and isinstance(data.__dict__[attr], dict):
                        try:
                            update_dict(data.__dict__[attr], val)
                        except:
                            self.error("Couldn't override original %s - not same shape."%attr)
                    else:
                        data.__dict__[attr] = val
                    if isinstance(val, (float, int)):
                        self.info("Setting %s.%s = %s"%(data_name, attr, val))
                    elif hasattr(val, "__len__") and not isinstance(val, u.Quantity):
                        # for some reason, u.Quantity has len but len(val) doesn't work
                        self.info("Setting %s.%s (length = %s)"%(data_name, attr, len(val)))
                    else:
                        self.info("Setting %s.%s"%(data_name, attr))

    def default_value(self, data_name, value):
        if self.__dict__[data_name] is None:
            if not(hasattr(value, "inputs")):
                self.warning(f"Using default {data_name} ({value}).")
            else: # don't display classes (too long)
                self.warning(f"Using default {data_name}.")
            self.__dict__[data_name] = value

    def build(self):
        """Initialize the model once all the parameters have been set. Set default values if needed.
        """
        if 't' not in self.__dict__:
            self.t = 0

        if self.filename is not None and self.input_atmosphere is not None:
            if self.input_atmosphere.grid:
                self.warning("Ignoring Grid from .cfg file since we have an input file.")
                self.input_atmosphere.grid = None
            if self.input_atmosphere.max_pressure:
                self.warning("Ignoring max_pressure from .cfg file since we have an input file.")
                self.input_atmosphere.max_pressure = None

        # parameters are the values read from the config file / parameters
        self.params = {
            'filename': copy(self.filename),
            'n_vertical': copy(self.n_vertical),
            'interp': copy(self.interp),
            'gas_dict': copy(self.gas_dict),
            'aerosols_dict': copy(self.aerosols_dict),
            'planet': copy(self.planet),
            'star': copy(self.star),
            'input_atmosphere': copy(self.input_atmosphere),
            'emission_atmosphere': copy(self.input_atmosphere),
            'observer': copy(self.observer),
            'opacity': copy(self.opacity),
            'transmission': copy(self.transmission),
            'emission': copy(self.emission),
            'lightcurve': copy(self.lightcurve),
            'phasecurve': copy(self.phasecurve),
        }
        if self.gas_dict is None:
            self.gas_dict = {}
        # read input file...
        self.read_data()
        
        if self.emission_atmosphere is None: 
            # small fix if emission grid not set by user (copy from transmission)
            self.emission_atmosphere = copy(self.input_atmosphere)
        
        # ... and override file data with input 'params'
        self.override_data_file(self.params)

        for parameter in self.default_values.items():
            self.default_value(*parameter)
        self.n_vertical = int(self.n_vertical)
        del self.params # don't keep duplicates

        if not (self.transmission or self.emission or self.lightcurve or self.phasecurve):
            self.warning("No mode chosen. We will compute a transit depth (Transmission mode). You may replace it with emission, lightcurve or phasecurve.")
            self.transmission = Transmission()
        assert self.planet, "Planet not defined!"
        assert self.star, "Star not defined!"

        if self.output_file:
            os.makedirs(os.path.dirname(os.path.abspath(self.output_file)), exist_ok=True)

        # Initialize each module and modes, link with model, set default values
        for module in ("observer", "orbit", "star", "planet"):
            try:
                self.__dict__[module].build(self)
            except Exception as e:
                self.debug(f"{module} has failed. Full error:\n{e}")

        for mode in self.modes:
            if self.__dict__[mode] is not None:
                self.info("Building %s"%mode)
                self.__dict__[mode].build(self)

        if self.output_file:
            self.info('Saving model into %s ...', self.output_file)
            write_hdf5(self.output_file, self, "Model")
            self.info('Save - DONE')

    def run(self, profiling=False):
        """Run Pytmosph3R, i.e., compute the spectrum of a built model
        (the function :py:attr:`build` (or an equivalent) should have been called).
        """
        self.info("Running model...")
        if self.atmosphere is None:
            self.error("Altitude Grid not computed. Call build() first.")
        if profiling:
            self.start_profiling()
        self.opacity.load_gas_database(self) # includes clip spectral range

        for mode in self.modes:
            if self.__dict__[mode] is not None:
                self.info("Switching to %s"%mode)
                self.__dict__[self.mode_keys[mode]] = self.__dict__[mode].compute(self)
                self.info('Saving %s outputs into %s ...' %(mode, self.output_file))
                write_hdf5(self.output_file, self, "Output", items=[mode])
                self.info('Save - DONE')
                continue

        if self.opacity.doppler:
            #if hasattr(self.opacity.doppler, "Kp") and hasattr(self.opacity.doppler, "phi"):
            if "Kp" in self.opacity.doppler.keys() and "phi" in self.opacity.doppler.keys():
                V_doppler = self.opacity.doppler['Kp']*1e3*np.sin(2.*np.pi*self.opacity.doppler['phi'])
                self.spectrum.wns = self.spectrum.wns/(1+V_doppler/C_LUM)
                self.spectrum.wnedges = self.spectrum.wnedges/(1+V_doppler/C_LUM)
            else:
                self.warning("Could not compute Doppler because I do not know 'Kp' or 'phi'.")

        if self.noise is not None and self.noise is not False and self.spectrum is not None:
            noise = self.noise
            if isinstance(noise, (float, int)):
                # create a normal distribution around the spectrum values
                noise = np.random.normal(0, self.noise, self.opacity.k_data.Nw)
            noise_spectrum = xk.Spectrum(noise, wns=self.wns, wnedges=self.wnedges)
            self.noised_spectrum = self.spectrum + noise_spectrum
        
        if profiling:
            if isinstance(profiling, str):
                self.dump_profiling(profiling)
            else:
                self.dump_profiling(None)
            
        items = [o for o in self.outputs() if o not in self.modes]
        write_hdf5(self.output_file, self, "Output", items=items)
        self.info('Save - DONE')

    @property
    def spectrum(self):
        try:
            return self.transmission_spectrum
        except:
            try:
                return self.emission_spectrum
            except:
                return None
    @property
    def wns(self):
        try:
            return self._wns
        except:
            return self.opacity.k_data.wns
    @wns.setter
    def wns(self, value):
        self._wns = value
    @property
    def wnedges(self):
        try:
            return self._wnedges
        except:
            return self.opacity.k_data.wnedges
    @wnedges.setter
    def wnedges(self, value):
        self._wnedges = value
    @property
    def wls(self):
        return 10000/self.wns
    @property
    def wledges(self):
        return 10000/self.wnedges
    @property
    def spectrum_value(self):
        return self.spectrum.value

    @property
    def spectrum_noised(self):
        try:
            return self.noised_spectrum.value
        except AttributeError:
            return None


class FileModel(Model):
    """Model reading from a file. Same parameters as :class:`~pytmosph3r.model.model.Model`, with the addition of a :attr:`filename`."""
    def __init__(self, filename:str, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        
        if filename is None:
            raise FileNotFoundError(f"No input file given. `{self.__class__.__name__}` takes a 'filename' parameter")

        self.filename = filename
        self.search_path(filename) # replaces self.filename

    def read_data(self, *args, **kwargs):
        """Adapt this function according to your format. See :func:`~pytmosph3r.model.diagfimodel.DiagfiModel.read_data` for an example."""
        raise NotImplementedError

    def inputs(self):
        return Model.inputs(Model) + ["filename"]