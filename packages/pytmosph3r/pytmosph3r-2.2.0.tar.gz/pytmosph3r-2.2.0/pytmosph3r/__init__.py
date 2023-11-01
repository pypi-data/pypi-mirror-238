from .__version__ import __version__

if True:
    # Import numpy to enable warnings suppression
    # noinspection PyUnresolvedReferences
    import numpy

# import submodules
from . import atmosphere
from . import chemistry
from . import external
from . import interface
from . import log
from . import model
from . import observations
from . import planetary_system
from . import plot
from . import util

# import files
from . import aerosols, grid, opacity, rays

# import content from files to match old behavior
from .rays import Rays
from .aerosols import PrepareAerosols
from .grid import Grid3D, Grid
from .opacity import Opacity

# import content from submodules to match old behavior
from .log import *
from .atmosphere import *
from .chemistry import *
from .model import *
from .observations import *
from .planetary_system import *
from .plot import *

# import specific content from submodules
from .util import constants

from .interface import write_netcdf, write_hdf5
from .interface.hdf5 import HDF5Input, HDF5Output
from .interface.io import write_spectrum
from .interface.netcdf import ncInput, ncOutput


# from .plot import Plot
# from .plot.plotutils import BasePlot


def debug(value=True):
    """Activates or deactivates debug mode.

    Args:
        value (bool, optional): If True, debug mode. If False, deactivates most of the logging. Defaults to True.
    """
    from .log import criticalLogging, debugLogging
    from .plot import Plot

    if value:
        debugLogging()
    else:
        criticalLogging()
