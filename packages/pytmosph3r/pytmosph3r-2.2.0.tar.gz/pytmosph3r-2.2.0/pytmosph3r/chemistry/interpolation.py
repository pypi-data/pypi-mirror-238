import numpy as np
import pandas as pd

from pytmosph3r.util.math import bilinear_interpolation_array, interp_ind_weights
from .chemistry import Chemistry


class InterpolationChemistry(Chemistry):
    """Chemistry model interpolating Volume Mixing Ratios based on a datafile.
    See the `Abundances-TiO.dat <https://forge.oasu.u-bordeaux.fr/jleconte/pytmosph3r-public/-/tree/master/examples/parmentier/Abundances-TiO.dat>`_ for an example.
    VMRs should be in the logarithmic space.
    See :attr:`logp_grid` for details on the pressure format.

    Args:
        gases (:obj:`list`) : List of gases to consider for interpolation.
        filename (str) : The path to the datafile.
    """
    def __init__(self, gases=None, filename=None, t_min=260):
        super().__init__(self.__class__.__name__, gases)
        self.search_path(filename)
        self.df = pd.read_csv(self.filename,sep=r"\s{1,}", engine='python')
        self.df = self.df[self.df["T"] >= t_min]
        self.t_grid = np.unique(self.df["T"])
        """Temperature grid (in K)."""
        self.logp_grid = np.log10(np.exp(np.unique(self.df["P"])))+2
        """Log(P) grid in Pa. For this, the pressure 'x' from the file is transformed via :math:`log_{10}(exp(x)))+2`."""
        self.data = {}

        for i_g, gas in enumerate(self.df.columns):
            self.data[gas] = np.empty(self.logp_grid.shape + self.t_grid.shape)
            for i_t, t in enumerate(self.t_grid):
                for i_p, p in enumerate(self.logp_grid):
                    self.data[gas][i_p, i_t] = self.df[gas].iloc[i_t * len(self.logp_grid) + i_p]

    def compute_vmr(self, gas, mix_ratio):
        i_p,weight_p = interp_ind_weights(np.log10(self.atmosphere.pressure),self.logp_grid)
        i_t,weight_t = interp_ind_weights(self.atmosphere.temperature,self.t_grid)

        p1t1=self.data[gas][i_p,  i_t  ].ravel()
        p0t1=self.data[gas][i_p-1,i_t  ].ravel()
        p1t0=self.data[gas][i_p,  i_t-1].ravel()
        p0t0=self.data[gas][i_p-1,i_t-1].ravel()
        res = np.zeros_like(p0t0)

        bilinear_interpolation_array(p0t0, p1t0, p0t1, p1t1, weight_p.ravel(), weight_t.ravel(), res)
        return np.reshape(np.exp(res), (mix_ratio.shape))

    def inputs(self):
        return Chemistry.inputs(Chemistry) + ["filename"]
