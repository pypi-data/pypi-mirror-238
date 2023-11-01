"""Model definition.
    You may run a simple example with :class:`~pytmosph3r.model.model.Model` by setting up a configuration file.
    See :any:`config_file` for more information.
"""
from .ATMOmodel import ATMOModel
from .diagfimodel import DiagfiModel
from .hdf5model import HDF5Model
from .model import Model
