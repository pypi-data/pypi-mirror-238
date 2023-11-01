from typing import Union
import datetime
import inspect
import sys
import warnings
from functools import wraps
from typing import Literal, Optional

import astropy.units as u
import numpy as np


def get_attributes(obj, attr=None):
    """Returns attributes of an object if they do not start nor end with an underscore.
    """
    if isinstance(obj, dict):
        return obj.items()
    attrs = dir(obj)
    items = []
    for a in attrs:
        try:
            if (not (a.startswith('_') or a.endswith('_'))) and ((attr is None) or (a in attr)):
                value = getattr(obj, a)
                if not inspect.ismethod(value):
                    items.append([a, value])
        except:
            continue
    return items

def get_methods(obj):
    """Returns methods of an object."""
    f = inspect.getmembers(obj.__class__, lambda a: inspect.isroutine(a))
    return [m[0] for m in f  if not (m[0].startswith('_') or m[0].endswith('_'))]


def retrieve_name(var, up=0):
    """Retrieve the name of a variable :py:attr:`var` as a string. For example if :py:attr:`var` is named \'temperature\', the function will return \"temperature\". Example::
        def test(hello, up=0):
            return retrieve_name(hello, up)
        bonjour = \"bonjour\"
        test(bonjour) # returns \"hello\"
        test(bonjour, up=1) # returns \"bonjour\"

    Args:
        var: Variable

        up: context to retrieve from (default is the current context, i.e., the function in which the function has been called)
    """
    callers_local_vars = None
    if up == 0:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    elif up == 1:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    elif up == 2:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def to_radians(array, units="deg"):
    """Convert an array from 'units' to rad."""
    if isinstance(array, u.Quantity):
        return array.to_value(u.rad) # ignore "units" if Quantity
    try:
        to_rad = u.Unit(units).to(u.rad)
    except:
        to_rad = u.Unit(units, format="cds").to(u.rad)
    return to_rad * array


def to_SI(obj: object, unit:Union[u.Unit, str]=None):
    """Convert astropy quantity to 'units' (SI by default)."""

    if obj is None:
        return obj

    if isinstance(obj, u.Quantity):
        if unit is None:
            # No unit passed, use Quantity `si` attribute to convert the Quantity to the correct unit
            return obj.si.value

        # `unit` is provided, use it
        return obj.to_value(unit)

    # INFO: the  unit should be attached to the container, ie: [1, ..., 3]*u.m, not [1*u.m, ..., 3*u.m]
    if isinstance(obj, (tuple, np.ndarray, list)):
        return [to_SI(x, unit) for x in obj]

    return obj


def get_altitude_index(altitude: Literal['surface', 'middle', 'top'], n_vertical: int):
    """Return altitude index associated with keyword `altitude` (within \"surface\",\"top\",\"middle\"). If not among this keyword, return as is.
    """
    if altitude == "surface":
        return 0

    if altitude == "top":
        return n_vertical - 1

    if altitude == "middle":
        return int(n_vertical / 2)

    if not isinstance(altitude, (int, list, np.ndarray)):
        raise TypeError("Altitude %s not recognized." % altitude)

    # TODO: check usefulness of this return, ie should we allow only allow literal.

    return altitude


def get_latitude_index(latitude: Literal['north', 'equator', 'south'], n_latitudes: int):
    """Return latitude index associated with keyword `latitude` (within \"north\",\"pole\",\"equator\").
    """
    if latitude == "north":
        return 0
    elif latitude == "south":
        return n_latitudes - 1
    elif latitude == "equator":
        return int(n_latitudes / 2)

    # TODO: check usefulness of this return, ie should we allow only allow literal.
    try:
        latitude = int(latitude)
    except TypeError:
        raise TypeError("Latitude %s not recognized." % latitude)

    return latitude


def get_longitude_index(longitude: Literal['day', 'night', 'terminator'], n_longitudes=None):
    """Return longitude index associated with keyword `longitude` (within \"day\",\"night\",
    \"terminator\"). The keywords refer to the position of the star if the direction of the rays has been
    defined as (latitude, longitude) = (0,0).
    """

    if longitude == "day":
        return int(n_longitudes / 2)

    if longitude == "night":
        return 0

    if longitude == "terminator":
        return int(n_longitudes / 4)

    try:
        longitude = int(longitude)
    except TypeError:
        raise TypeError("Longitude %s not recognized." % longitude)
    return longitude


def get_index(array, location, dim: Literal['altitude', 'latitude', 'longitude'] = 'altitude'):
    """Return the index of `location` in `array` at the dimension `dim` (altitude/latitude/longitude). For
    example, if `dim` is 'altitude' and `location` is 'surface', it will return 0. """

    if isinstance(array, (float, str)) or array.ndim != 3:
        warnings.warn("%s doesn't have 3 dimensions" % type(array))
        return array

    if dim == "altitude":
        return get_altitude_index(location, array.shape[0])
    if dim == "latitude":
        return get_latitude_index(location, array.shape[1])

    if dim == "longitude":
        return get_longitude_index(location, array.shape[2])

    warnings.warn(
        f"Dimension '{dim}' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. "
        f"Returning 0...")

    return 0


def get_2D(array, location, dim: Literal['altitude', 'latitude', 'longitude'] = 'altitude'):
    """Return a 2D slice of array `array` at the dimension `dim` (among altitude, latitude and longitude).
    For example if `dim` is 'altitude', it will return the 2D array of all latitudes and longitudes at this
    altitude. """

    if isinstance(array, (float, str)) or array.ndim != 3:
        warnings.warn("%s doesn't have 3 dimensions" % type(array))
        return array

    if dim == "altitude":
        return array[get_altitude_index(location, array.shape[0])]

    if dim == "latitude":
        return array[:, get_latitude_index(location, array.shape[1])]

    if dim == "longitude":
        return array[:, :, get_longitude_index(location, array.shape[2])]

    warnings.warn(
        f"Dimension '{dim}' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. "
        f"Returning whole array but the program will be probably fail...")

    return array


def get_column(array, latitude, longitude):
    """Return a vertical column of array `array` at the position (`latitude`, `longitude`).
    """
    if isinstance(array, (float, str)) or array.ndim != 3:
        return array
    return array[:, get_latitude_index(latitude, array.shape[1]),
           get_longitude_index(longitude, array.shape[2])]


def convert_log(array, units: Optional[Literal['log', 'ln']] = None):
    """Convert :attr:`array` from log space to normal space. :attr:`units` determines if the space is log
    or ln. """
    if units == 'log':
        return np.power(10, array)

    if units == 'ln':
        return np.exp(array)

    warnings.warn(f'Unable to determine the kind of log. `units` should be set to `log` or `ln`, provided: `{units}`.')

    return array


def mol_key(mol_dict, mol, mol_type="vap", data=""):
    """Returns the key corresponding to `mol` in `mol_dict`.
    """
    key = mol + data
    if mol_dict is not None and key in mol_dict.keys():
        return mol_dict[key]

    return mol.lower() + "_" + mol_type + data


def aerosols_array_iterator(dictionary):
    """Returns an iterator over arrays of an aerosols dictionary.
    For example, if the dictionary looks like this:
    :code:`{'H2O':{'mmr':np.array([1, 2]), 'reff':1e-5}}`.
    The code will iterate over the mmr (array) but not reff (float).
    """
    for element, value in dictionary.items():
        for key_element, element_val in value.items():
            if isinstance(element_val, np.ndarray):
                yield element, key_element


def arrays_to_zeros(dictionary, shape):
    """Returns a copy of `dictionary` of which subarrays are initialized as an array of shape `shape`
    filled with zeros. Used for aerosols, to initialize the arrays before interpolating.
    """

    new_dict = dictionary.copy()
    for element, value in dictionary.items():
        new_dict[element] = value.copy()
        for key_element, element_val in value.items():
            if isinstance(element_val, np.ndarray):
                new_dict[element][key_element] = np.zeros(shape)
    return new_dict


def init_array(obj, size):
    """Returns `obj` if float, else array of size `size`."""
    if isinstance(obj, float):
        return obj
    else:
        return np.full(size, np.nan)


def get(obj, i):
    """Returns obj if float, else return the value of obj at `i`"""
    try:
        return obj[i]
    except:
        return obj


def update_dict(d, u):
    """Recursive update of nested dictionaries."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def merge_attrs(obj, other):
    """Merge attributes from `other` into `obj` if they do not exist/are None.
    """
    try:
        if isinstance(other, dict):
            obj.__dict__.update(
                {k: other[k] for k in other if (not hasattr(obj, k) or getattr(obj, k) is None)})
        else:
            obj.__dict__.update({k: getattr(other, k) for k in other.__dict__ if
                                 (not hasattr(obj, k) or getattr(obj, k) is None)})
    except:
        pass  # maybe `other` is not well-constructed/does not exist
    return obj


def spectral_chunks(k_database, n):
    chunk_size = len(k_database.wns) / n
    wn_ranges = []
    for chunk in range(n):
        try:
            wn_range = [k_database.wnedges[int((chunk * chunk_size) - 1)],
                        k_database.wnedges[int(min(len(k_database.wnedges) - 1, (chunk + 1) * chunk_size))]]
            if chunk == 0:
                wn_range[0] = -1
            wn_ranges.append(wn_range)
        except IndexError:
            pass  # Outside of wns range now
    return wn_ranges


def get_chunk(i, n, size):
    """Get i-th chunk out `n` chunks dividing `size`."""
    if hasattr(size, "__len__") and len(size) == 2:  # 2 dimension
        chunk_size = size[0] * size[1] / n
        idx = int(i * chunk_size), int(min(int((i + 1) * chunk_size), size[0] * size[1]))
        chunk_0 = [idx[0] % size[0], idx[1] % size[0]]  # chunk in 1st  dimension
        chunk_1 = [int(idx[0] / size[0]), int(idx[1] / size[0])]  # chunk in 2nd dimension
        if idx[1] == size[0] * size[1]:
            chunk_0[1] = size[0]
            chunk_1[1] = size[1] - 1
        chunk = [chunk_0, chunk_1]
    else:
        chunk_size = size / n
        chunk = [int(i * chunk_size), min(int((i + 1) * chunk_size), size)]
    return chunk


def get_chunk_size(chunk, chunk_size, total_size):
    start = chunk * chunk_size  # start of chunk
    end = min((chunk + 1) * chunk_size, total_size)  # last chunk may be shorter
    return end - start


def get_wls(array, wls, array_wls):
    """Get subset of :attr:`array` at wavelengths :attr:`wls` when the wavelengths of :attr:`array` are
    :attr:`array_wls`
    """

    return array[..., -np.asarray(array_wls[::-1]).searchsorted(wls)]


def make_array(lis):
    """Get array from a list of lists. Missing data is replaced with -1."""
    n = len(lis)
    lengths = np.array([len(x) for x in lis])
    max_len = np.max(lengths)
    try:
        shape_element = lis[0][0].shape
        arr = np.full((n, max_len) + shape_element, -1.)
    except:
        arr = np.full((n, max_len), -1.)

    for i in range(n):
        arr[i, :lengths[i]] = lis[i]
    return np.array(arr)


def timer(f):
    """A decorator to time a function in debug mode."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = f(*args, **kwargs)
        end_time = datetime.datetime.now()
        total_time = end_time - start_time
        args[0].debug("%s run in %.2fs" % (f.__name__, total_time.total_seconds()))
        return result

    return wrapper


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        try:
            choice = input().lower()
        except EOFError:
            return valid[default]
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
