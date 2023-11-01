"""
@author: A. Falco

Create objects from config file, forked from TauREX 3 (https://github.com/ucl-exoplanets/TauREx3_public/tree/master/taurex/parameter/factory.py).
"""

from pytmosph3r.log import Logger

log = Logger('Factory')


def create_obj(config, name, *args, **kwargs):
    """Creates an object with parameters from the configuration file."""

    args, class_obj = determine_class(config, name, 'type', factory)
    args.update(kwargs)

    obj_type = None
    if isinstance(class_obj, tuple):
        obj_type = class_obj[1]
        class_obj = class_obj[0]

    if class_obj is None:
        return None

    obj = class_obj(**args)

    if obj_type is not None and 'type' not in obj.__dict__:
        obj.type = obj_type  # save type for potential reload of output data

    return obj


def determine_class(config, name, field, factory):
    args = {}
    class_field = None

    if name in config:
        try:
            args = config[name]
            class_field = config[name].pop(field)
            log.info(f"Setting {name} to {class_field}")
        except KeyError:
            class_field = None
        except AttributeError:
            args = {}

    class_obj = factory(name, class_field)

    return args, class_obj


def factory(name, obj_type):
    obj = None

    if name in ('Model',):
        return model_factory(obj_type)

    if name in ('Chemistry',):
        return chemistry_factory(obj_type)

    if name in ('Parallel',):
        return parallel_factory(obj_type)
    if name in ('Star',):
        return star_factory(obj_type)

    if name in ('Planet',):
        from pytmosph3r.planetary_system import Planet as obj
    elif name in ('Grid',):
        from pytmosph3r.grid import Grid3D as obj
    elif name in ('Atmosphere',):
        from pytmosph3r.atmosphere import InputAtmosphere as obj
    elif name in ('Observer',):
        from pytmosph3r.planetary_system import Observer as obj
    elif name in ('Opacity',):
        from pytmosph3r.opacity import Opacity as obj
    elif name in ('Transmission',):
        from pytmosph3r.observations import Transmission as obj
    elif name in ('Emission',):
        from pytmosph3r.observations import Emission as obj
    elif name in ('Lightcurve',):
        from pytmosph3r.observations import Lightcurve as obj
    elif name in ('Phasecurve',):
        from pytmosph3r.observations import Phasecurve as obj
    else:
        raise NotImplementedError(f"Class '{name}' not implemented")

    return obj


def parallel_factory(obj_type):
    raise NotImplementedError
    if obj_type is None:
        log.info("Using MultiProc by default.")
        from pytmosph3r.parallel import MultiProcTransit as parallel
    elif obj_type.lower() in ('mp', 'multiproc', 'multiprocessing'):
        from pytmosph3r.parallel import MultiProcTransit as parallel
    elif obj_type.lower() in ('mpi',):
        log.warning("MPI parallelization not supported anymore. Using MultiProc.")
        from pytmosph3r.parallel import MultiProcTransit as parallel
    else:
        log.error("Parallel type '{}' not implemented. Sequential run.".format(obj_type))
        return None

    return parallel, obj_type


def model_factory(obj_type):
    if obj_type is None or obj_type.lower() in ('simple',):
        from pytmosph3r.model import Model as model
    elif obj_type.lower() in ('hdf5',):
        from pytmosph3r.model import HDF5Model as model
    elif obj_type.lower() in ('diagfi',):
        from pytmosph3r.model import DiagfiModel as model
    else:
        model = get_class(obj_type)

    return model


def chemistry_factory(obj_type):
    if obj_type is None:
        log.debug("No chemistry given. If you want one, set chemistry type. See pytmosph3r.chemistry and pytmosph3r.InputAtmosphere.chemistry for more information.")
        return None

    if obj_type.lower() in ('parmentier2018', 'dissociation'):
        from pytmosph3r.chemistry import Parmentier2018Dissociation as chemistry
    elif obj_type.lower() in ('fastchem', 'fastchemistry'):
        from pytmosph3r.chemistry import FastChemistry as chemistry
    elif obj_type.lower() in ('interpolation', 'interp'):
        from pytmosph3r.chemistry import InterpolationChemistry as chemistry
    elif obj_type.lower() in ('standard',):
        from pytmosph3r.chemistry.standard import StandardRatioHeH2 as chemistry
    elif obj_type is None:
        log.debug("No chemistry given. If you want one, set chemistry type with %s.")
        chemistry = None
    else:
        from pytmosph3r.chemistry import Chemistry
        chemistry = get_class(obj_type, Chemistry)

    return chemistry, obj_type


def star_factory(obj_type):
    if obj_type is None or obj_type.lower() in ('blackbody',):
        from pytmosph3r.planetary_system import BlackbodyStar as star
    elif obj_type.lower() in ('sun','solar'):
        from pytmosph3r.planetary_system import SunStar as star
    elif obj_type.lower() in ('spectrum','file'):
        from pytmosph3r.planetary_system import SpectrumStar as star
    else:
        star = get_class(obj_type)
    return star


def get_class(python_file, baseclass=None):
    import importlib.util
    import inspect

    log.search_path(python_file)
    python_file = log.filename
    spec = importlib.util.spec_from_file_location("module", python_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        candidates = [m[1] for m in inspect.getmembers(module, inspect.isclass)]
        classes = [c for c in candidates if c
                   is not baseclass and issubclass(c, baseclass)]
    except:
        classes = candidates

    if len(classes) == 0:
        log.error('Could not find class of type %s in file %s', baseclass, python_file)
        raise Exception(f'No class inheriting from {baseclass} in '
                        f'{python_file}')

    return classes[0]
