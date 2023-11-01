"""
@author: A. Falco

Logging module,
 inspired from TauREX 3 (https://github.com/ucl-exoplanets/TauREx3_public/tree/master/taurex/log).
"""

import logging

from pytmosph3r.util.memory import MemoryUtils
from pytmosph3r.util.pkg_dir import pkg_dir
from pytmosph3r.util.util import get_attributes, get_methods

__all__ = ['Logger', 'root_logger']

root_logger = logging.getLogger('pytmosph3r')
root_logger.propagate = False
"""Root logger for pytmosph3r"""

rh = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
rh.setFormatter(formatter)
rh.setLevel(logging.DEBUG)
root_logger.handlers = []
root_logger.addHandler(rh)
root_logger.setLevel(logging.INFO)


class Logger(MemoryUtils):
    """
    Standard logging using logger library

    Parameters
    -----------
    name : str
        Name used for logging
    """
    verbose = 0

    def __init__(self, name=None):
        name = name if name is not None else self.__class__.__name__
        self._log_name = f'pytmosph3r.{name}'

        self._logger = logging.getLogger(f'pytmosph3r.{name}')

        self.filename = None

    def info(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.warning(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.debug(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.critical(message, *args, **kwargs)

    def isEnabledFor(self, level):
        return self._logger.isEnabledFor(level)

    def search_path(self, filename):
        """Search for filename in current folder, then in :attr:`~pytmosph3r.relative_dir`, and finally in the `examples/` folder of the `pytmosph3r` code. It then set the attribute :attr:`filename` to its path.
        """
        self.filename = None
        if filename:
            import os
            self.filename = filename
            if not os.path.isfile(filename):
                import pytmosph3r as p3
                self.filename = os.path.realpath(os.path.join(pkg_dir.relative_dir, filename))
                if os.path.exists(self.filename):
                    self.warning(f"File ./{filename} doesn't exist. Using {self.filename}")
                else:
                    relative_filename = self.filename
                    self.filename = os.path.realpath(os.path.join(pkg_dir.root_dir, "examples", filename))
                    if os.path.exists(self.filename):
                        self.warning(
                            f"File ./{filename} and {relative_filename} don't exist. Using {self.filename}")
                    else:
                        raise IOError(f"Couldn't find file {filename}")
        return self.filename

    def inputs(self):
        code = self.__init__.__code__
        return list(code.co_varnames[1:code.co_argcount]) # 1 to exclude 'self'

    def inputs_values(self):
        return get_attributes(self, self.inputs())
    
    def summary(self):
        """Prints all attributes and values of object. WARNING: could be verbose."""
        return get_attributes(self)
    
    def __repr__(self) -> str:
        if not ("inputs" in get_methods(self) or "outputs" in get_methods(self)):
            return super().__repr__()
        msg = " " + self.__class__.__name__ + "()\n"
        if "inputs" in get_methods(self):
            msg += f"- Inputs: {self.inputs()}\n"
        if "outputs" in get_methods(self):
            msg += f"- Outputs: {self.outputs()}\n"
        msg += f"- Methods: {get_methods(self)}\n"
        return msg
