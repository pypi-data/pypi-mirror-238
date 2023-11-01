import numba
import numpy as np
import scipy as sp
from numba.typed import List


@numba.vectorize
def nmin(x, y):
    return min(x, y)


@numba.vectorize
def nmax(x, y):
    return max(x, y)


@numba.vectorize
def nround(x, y):
    return np.round(x, y)


def interp1d(xx, yy, xkind='linear', ykind='linear', **kwargs):
    logx = xx
    if xkind == 'log':
        logx = np.log(xx)
    if ykind == 'log':
        yy[yy<0] = 0
        lin_interp = sp.interpolate.interp1d(logx, np.log(yy), **kwargs)
        log_interp = lambda x: np.exp(lin_interp(x))
        if xkind == 'log':
            log_interp = lambda x: np.exp(lin_interp(np.log(x)))
        return log_interp
    lin_interp = sp.interpolate.interp1d(logx, yy, kind=ykind, **kwargs)
    if xkind == 'log':
            return lambda x: lin_interp(np.log(x))
    return lin_interp

@numba.njit(nogil=True,fastmath=True, cache=True)
def bilinear_interpolation_array(z00, z10, z01, z11, x, y, res):
    """
    2D interpolation
    Applies linear interpolation across x and y between xmin,xmax and ymin,ymax.
    x, y and z must be 1D-arrays of the same length.

    Parameters
    ----------
        z00: array
            Array corresponding to xmin,ymin
        z10: array
            Array corresponding to xmax,ymin
        z01: array
            Array corresponding to xmin,ymax
        z11: array
            Array corresponding to xmax,ymax
        x: array
            weights on x coord
        y: array
            weights on y coord
    """
    xy = x*y
    for i in range(z00.shape[0]):
        res[i] = (z11[i]-z01[i]+z00[i]-z10[i])*xy[i] +(z01[i]-z00[i])*y[i] +(z10[i]-z00[i])*x[i] +z00[i]

def interp_ind_weights(x_to_interp,x_grid):
    """Finds the indices and weights to interpolate from a x_grid to a x_to_interp.
    """
    xmin=x_grid.min()
    xmax=x_grid.max()
    used_x=np.where(x_to_interp>xmax,xmax,x_to_interp)
    used_x=np.where(used_x<xmin,xmin,used_x)
    indices=np.searchsorted(x_grid,used_x)
    indices=np.where(indices==0,1,indices)
    return indices,(used_x-x_grid[indices-1])/(x_grid[indices]-x_grid[indices-1])

@numba.njit
def roots(a,b,c):
    r"""Find roots of a polynomial, i.e., find `x` for :math:`ax^2 + bx + c = 0`.
    """
    x = List()
    if a == 0:
        if b != 0:
            x.append(-c/b)
    else:
        bp=b/2
        delta=bp*bp-a*c
        if 0 > delta > -1e-10:
                delta = 0. ## rounding error
        x.append((-bp-delta**.5)/a)
        x.append(-x[0]-b/a)
    return x
