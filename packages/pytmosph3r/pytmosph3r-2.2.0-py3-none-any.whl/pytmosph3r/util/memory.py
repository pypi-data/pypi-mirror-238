import platform
import re
import sys

import numpy as np
import psutil

from .util import retrieve_name


class MemoryUtils:
    """This class is inherited from :class:`Logger`."""

    margin = 1
    """Margin (in ratio wrt available memory) that we can allow to allocate (to avoid swapping)."""

    def check_memory(self, to_check, name=None):
        """Check if memory of :py:attr:`to_check` is lower than available memory.

        Args:
            to_check (array, int): If an array, calculate its theoretical memory based on its shape and dtype. If the
            number of elements (for example before creating an array), multiply by the size of :py:attr:`obj_type`
            name (str, optional): Name to print in message. Defaults to None. If :py:attr:`to_check` is an array,
            it will try to retrieve the variable name.
        """

        if name is None:
            try:
                name = retrieve_name(to_check, 1)
            except:
                name = "Object"

        mem, mem_available = self.available_memory(to_check)

        if mem > MemoryUtils.margin * mem_available:
            raise MemoryError(
                    f"{name} ({mem / 1e9} GB) won't fit in memory ({mem_available / 1e9} GB available). You can "
                    f"release some RAM (preferable) or try to increase pytmosph3r.MemoryUtils.margin (= "
                    f"{MemoryUtils.margin}), if you are not afraid of swapping or crashing...")
        else:
            self.debug(f"{name} will use as much as {mem / 1e6} MB")

    def available_memory(self, to_check, obj_type=float):
        """Returns how much of the available memory an object is consuming.

        Args:
            to_check (array, int): If an array, calculate its theoretical memory based on its shape and dtype. If the
            number of elements (for example before creating an array), multiply by the size of :py:attr:`obj_type`
            obj_type (type, optional): Type of :py:attr:`to_check` (to use only if it's a number, not an array).
            Defaults to `float`.
        """

        if isinstance(to_check, np.ndarray):
            mem = np.prod(to_check.shape) * to_check.dtype.itemsize
        else:
            mem = to_check * sys.getsizeof(obj_type())

        mem_available = psutil.virtual_memory().available

        return mem, mem_available


def memory_usage(pattern="VmR"):
    """Returns overall memory usage of process. (Linux only)"""

    if platform.system() != "Linux":
        return

    with open("/proc/self/status") as file:
        for line in file:
            if re.search(pattern, line):
                return " ".join(line.split()[1:]).strip()
