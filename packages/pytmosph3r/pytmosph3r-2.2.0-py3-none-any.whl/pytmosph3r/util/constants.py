"""Physical constants used in pytmosph3r.
"""
import astropy.units as u

AMU: float = 1.660538921e-27  # 1e-3/AMU = N_A = 6.022141290116741e+23
KBOLTZ: float = 1.380648813e-23
G: float = 6.67384e-11
RSOL: float = u.Rsun.to(u.m)  # 6.957e8
RJUP: float = u.Rjup.to(u.m)  # 71492000 in astropy
RGP: float = 8.31446
PI: float = 3.14159265359
MSOL: float = u.Msun.to(u.kg)  # equal to 1.9884099e+30
MJUP: float = 1.898e27
AU: float = 1.49597871e+11
PLANCK: float = 6.62606957e-34
SPDLIGT: float = 299792458.
