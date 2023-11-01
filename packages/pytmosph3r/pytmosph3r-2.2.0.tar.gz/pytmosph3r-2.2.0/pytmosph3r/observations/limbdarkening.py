import numba
import numpy as np

from pytmosph3r.log import Logger


@numba.njit(cache=True)
def ld_uniform(x, c):
    return np.ones_like(x)

@numba.njit(cache=True)
def ld_linear(x, c):
    mu = np.sqrt(1-np.power(x,2))
    return 1 - c[0]*(1-mu)

@numba.njit(cache=True)
def ld_quadratic(x, c):
    mu = np.sqrt(1-np.power(x,2))
    return 1 - c[0]*(1-mu) - c[1]*np.power((1-mu), 2)

# @numba.njit(cache=True)
# def norm_quadratic(x, c):
#     return 1 - c[0]/3 - c[1]/6

@numba.njit(cache=True)
def ld_power2(x, c):
    mu = np.sqrt(1-np.power(x,2))
    return 1 - c[0]*(1-np.power(mu, c[1]))

@numba.njit(cache=True)
def ld_nonlinear(x, c):
    mu = np.sqrt(1-np.power(x,2))
    return 1 - c[0]*(1-np.power(mu, .5)) - c[1]*(1-mu) - c[2]*(1-np.power(mu, 1.5)) - c[3]*(1-np.power(mu, 2))

class LimbDarkening(Logger):
    """BEWARE: Work In Progress. Contributions are welcome.
    
    Module handling multiple limb darkening methods (linear,quadratic,power2,nonlinear,uniform)."""
    
    factor_dict = {
        "linear": ld_linear,
        "quadratic": ld_quadratic,
        "power2": ld_power2,
        "nonlinear": ld_nonlinear,
        "uniform": ld_uniform,
    }
        
    # norm_dict = {
    #     "linear": ld_linear,
    #     "quadratic": norm_quadratic,
    #     "power2": ld_power2,
    #     "nonlinear": ld_nonlinear,
    #     "uniform": ld_uniform,
    # }
    
    def __init__(self, method=None, coeffs=None):
        """Parameters for the limb darkening method.

        Args:
            method (str, optional): Method (among linear,quadratic,power2,nonlinear,uniform). Defaults to uniform (no limb darkening).
            coeffs (list, optional): List of coefficients c1, c2, c3, c4 (depends on the method). Defaults to None.
        """
        super().__init__()
        self.critical("FEATURE UNDER DEVELOPMENT. Not supported yet.")
        self.method = method
        self.coeffs = coeffs

    def get_func(self, method=None, coeffs=None):
        if coeffs is None: coeffs = self.coeffs
        if method is None: method = self.method
        if isinstance(coeffs, (type(None))):
            coeffs=[]
        elif isinstance(coeffs, (int,float)):
            coeffs=[coeffs]
        # if len(coeffs) < 4: # functions need 4 coefficients
        #     coeffs += list(np.full(4-len(coeffs), None))
        return self.factor_dict[method], np.asarray(coeffs)

    def compute(self, dist_star, method=None, coeffs=None):
        """Function that parses which method should be used and return the corresponding darkening over an array of (normalized) distance to the center of the star.

        Args:
            dist_star (array): Distance to star center normalized over the star radius (center = 0, edge = 1).
            method (str, optional): Method to be used (see :attr:`factor_dict`). Defaults to None.

        Returns:
            array: Darkening coefficient (0 at star center).
        """
        f, coeffs = self.get_func(method, coeffs)
        darkening = f(dist_star, coeffs)
        if isinstance(darkening, (float, int)):
            if np.isnan(darkening):
                return 0
        else:
            darkening[np.where(np.isnan(darkening))] = 0 # out of star?
        return darkening


LD = LimbDarkening