"""Chemistry modules that can be used to compute the volume mixing ratios based on atmospheric data (pressure, temperature, ...). These modules include for now :class:`fastchem <pytmosph3r.chemistry.fastchem.FastChemistry>`, :class:`parmentier2018 <pytmosph3r.chemistry.dissociation.Parmentier2018Dissociation>` and :class:`interpolation <pytmosph3r.chemistry.interpolation.InterpolationChemistry>`.
You can create you own module by inheriting from :class:`~pytmosph3r.Chemistry`.
If you don't want to inherit from :class:`~pytmosph3r.chemistry.chemistry.Chemistry`, the module should at least have a function build() that follows the same arguments.
See :attr:`~pytmosph3r.atmosphere.inputatmosphere.InputAtmosphere.chemistry` for more information.
"""

from .chemistry import Chemistry
from .dissociation import Parmentier2018Dissociation
from .fastchemistry import FastChemistry
from .interpolation import InterpolationChemistry
from .standard import StandardRatioHeH2

try:
    from .ace3d import ACE3D
except ModuleNotFoundError:
    # Taurex is not installed
    pass
