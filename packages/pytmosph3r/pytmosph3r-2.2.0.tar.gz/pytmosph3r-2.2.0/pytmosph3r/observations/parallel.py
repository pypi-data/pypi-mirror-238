import multiprocessing as mp
from multiprocessing import Pool

import numpy as np
from tqdm.auto import tqdm

from pytmosph3r.log import Logger
from pytmosph3r.util.util import get_chunk


def transit_depth_angle(transmission, rk, nprocs, *args, **kwargs):
    integrals = []
    iterations = range(*get_chunk(rk, nprocs, transmission.rays.n_angular))
    if rk == 0:
        iterations = tqdm(iterations, leave=False)
    for i in iterations:
        transmission.per_angle = True
        transmission.rays.angle_idx = i
        integrals.append(transmission.angle_to_integral())
    return integrals

def transit_depth_grid(transmission, rk, nprocs, *args, **kwargs):
    # raise NotImplementedError # not functional yet
    rays = transmission.rays
    bounds = get_chunk(rk, nprocs, rays.shape)
    return transmission.grid_to_transmittance(bounds)

def transit_depth_wn(transmission, rk, nprocs, *args, **kwargs):
    # raise NotImplementedError  # not functional yet
    chunk = get_chunk(rk, nprocs, transmission.opacity.k_data.Nw)
    wn_range = [transmission.opacity.k_data.wnedges[chunk[0]-1],
                transmission.opacity.k_data.wnedges[chunk[1]]]
    if rk == 0:
        wn_range[0] = -1
    return transmission.wn_to_integral(wn_range=wn_range, *args, **kwargs)

def transit_depth_i(transmission, rk, nprocs, dimension, *args, **kwargs):
    """Returns a list of integrals that will be concatenated/stacked together with the rest."""
    if dimension == "angles":
        return transit_depth_angle(transmission, rk, nprocs, *args, **kwargs)
    if dimension == "rays":
        return transit_depth_grid(transmission, rk, nprocs, *args, **kwargs)
    if dimension == "spectral":
        return transit_depth_wn(transmission, rk, nprocs, *args, **kwargs)

class Parallel(Logger):
    """
    Base class for a parallel version of the transit depth (see :class:`~pytmosph3r.transmission.Transmission`).

    Args:
        nprocs (int): number of procs (by default, maximum).
        dimension (str): Dimension to subdivide among workers. Possible values are `spectral`, `angles`, or `rays`. A `spectral` subdivision shares the spectral range among the workers, `angles` means the angular points of the rays grid are used, while `rays` means all of the rays grid is shared among the workers.
    """
    nprocs = None
    def __init__(self, name, nprocs=None, dimension="rays"):
        name =  self.__class__.__name__ if name is None else name
        super().__init__(name)
        Parallel.nprocs = nprocs
        if nprocs:
            Parallel.nprocs = int(nprocs)
        else:
            Parallel.nprocs = mp.cpu_count()
        self.dimension = dimension

    def synchronize(self, model):
        self.info("Running on %s procs. (on %s dimension)"%(Parallel.nprocs, self.dimension))
        self.model = model
        return model

    def compute_integral(self, transmission, *args, **kwargs):
        """Compute integral over :attr:`nprocs` processes by subdividing the work along the spectral dimension (if :attr:`dimension` is "spectral) or rays dimension(s).
        """
        self.transmission = transmission
        self.model = transmission.model
        integrals = self._compute_integral(transmission, *args, **kwargs)
        integral = self.retrieve_results(integrals)
        return integral


    def retrieve_results(self, results):
        results = [result for result in results if len(result)] # if too many workers, some may have not worked at all! :-O
        if self.dimension == "rays":
            transmittance = np.concatenate(results)
            transmittance = transmittance.reshape(self.transmission.rays.shape+ (self.transmission.opacity.k_data.Nw,))
            # this mode's only computed transmittance for now
            return self.transmission.transmittance_to_integral(transmittance)
        return np.concatenate(results)

class MultiProcTransit(Parallel):
    def __init__(self, nprocs=None, *args, **kwargs):
        super().__init__(self.__class__.__name__, nprocs, *args, **kwargs)
        self.rk = 0

    def _compute_integral(self, transmission, *args, **kwargs):
        with Pool(Parallel.nprocs) as p:
            integrals = p.starmap(transit_depth_i, tqdm([(transmission, rk, self.nprocs, self.dimension, *args, *kwargs) for rk in range(self.nprocs)], total=self.nprocs, leave=False))
        return integrals
