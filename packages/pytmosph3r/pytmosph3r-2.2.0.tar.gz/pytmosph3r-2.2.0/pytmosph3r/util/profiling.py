import cProfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional


@contextmanager
def profiler(filename: Optional[Path] = None) -> cProfile.Profile:
    """
    Profile some part of the code using a context block.

    .. code-block:: python

        with profiler() as pr:
            m = np.random.random((1000,1000)) ** 2

        # After the context block, the profile can be accessed.
        print(pr.stats)


    Args:
        filename (Optional[Path]): name of the file where to save the profile

    Returns:
        Return the profile of the code previously executed. 
    """
    profile = cProfile.Profile()

    try:
        profile.enable()
        yield profile
    finally:
        profile.disable()
        profile.create_stats()

        if filename is not None:
            profile.dump_stats(filename)
