from typing import Optional, Union

import astropy.units as u
import numpy as np
from astropy.units import Quantity
from tqdm.auto import tqdm

from pytmosph3r.util import pt
from pytmosph3r.util.util import merge_attrs, to_SI
from .emission import Emission


class Phasecurve(Emission):
    """The Phasecurve module relies on the :class:`~pytmosph3r.emission.Emission` module: we iterate over
    :attr:`n_phases` observer longitudes and scale the flux using the projection of the surface onto that direction.
    You can use the same parameters as :class:`~pytmosph3r.emission.Emission` for this module.
    IMPORTANT NOTE: :attr:`top_flux_from_star` and :attr:`mu_from_obs` will add a considerable computing time since
    the emission flux has to be re-computed at EACH phase.

    Args:
        n_phases (int) : Number of phases for the phase curve. Defaults to 100.
        start (float) : Phase at which to start the phasecurve, in SI (radians) or astropy units.
        end (float) : Phase at which to end the phasecurve, in SI (radians) or astropy units.
        phases (array) : List of phases (ignores :attr:`n_phases`, :attr:`start` and :attr:`end`). Assumed to be in
        SI, or astropy units.
        kwargs (dict): Parameters passed to the :class:`~pytmosph3r.emission.Emission` module.

    Returns:
        (array): A series of :attr:`n_phases` Emission fluxes.
    """

    def __init__(self,
                 n_phases: Optional[int] = None,
                 start: Union[None, float, Quantity[pt.angle]] = None,
                 end: Union[None, float, Quantity[pt.angle]] = None,

                 phases: Union[None, np.ndarray, Quantity[pt.angle]] = None,

                 wns=None, *args, **kwargs):
        """
        We provide two methods to select the phases, the first one (1) provide an array with the phases wanted.
        The second one (2) create the phases array from a number of phase and the bounds.

        Args:
            n_phases (Optional[int]): (2)
            start (None, float, Quantity[pt.angle]): (2)
            end (None, float, Quantity[pt.angle]): (2)

            phases (Union[None, np.ndarray, Quantity[pt.angle]]): Typed array (1)

            wns ():
            *args ():
            **kwargs ():
        """

        super().__init__(*args, **kwargs)

        self.n_phases: int = n_phases
        """Number of phases in the phase curve."""

        self.start : float = to_SI(start, u.rad)
        self.end: float = to_SI(end, u.rad)

        self.phases: np.ndarray = to_SI(phases, u.rad)

        self.wns: np.ndarray = wns

        self.store_raw_flux: bool = True  # INFO: always activates this in phasecurves

    def build(self, model):
        self.model = model
        # Get emission parameters...
        e = model.emission
        if e is not None: # ... from emission object if computed
            self = merge_attrs(self, e)
        else: # ... by recomputing them otherwise
            super().build(model)

        # Set default parameters
        if self.phases is not None:
            if isinstance(self.phases, (int, float)):
                self.phases=[self.phases] # handle one phase case
            assert hasattr(self.phases, "__len__"), "Phases should be given as a list or array."
            self.warning("You have set a list of 'phases', so 'n_phases' is ignored.")
            self.n_phases = len(self.phases)
        if self.n_phases is None:
            self.n_phases = 100
            self.warning("Number of phases set to 100.")
        self.n_phases = int(self.n_phases)

        if self.start is None:
            self.start = to_SI(-180*u.deg, u.rad)
        if self.end is None:
            self.end = to_SI(180*u.deg, u.rad)

        if self.phases is None:
            self.phases = to_SI(np.linspace(self.start, self.end, self.n_phases)*u.rad, u.rad)

    def compute(self, model):
        """Computation of a phase curve, along :attr:`n_phases` observer longitudes. This function is called by :func:`compute`."""
        self.info(f"Computing phase curve with {self.n_phases} points...")

        self.flux = np.zeros((self.n_phases,self.model.opacity.k_data.Nw))

        initial_longitude = self.model.observer.longitude # save longitude since we're going to overwrite it during the phase curve
        if self.wns is None:
            self.wns = model.opacity.k_data.wns
            # TODO pick wns for calculations, as in lightcurve module

        # re-calculate raw flux if possible
        # Check the case where we only need to perform one call to `compute`.
        #     - Planet is tidally locked
        # and - mu_from_obs is False
        # Then the position of the observer does not affect the `raw_flux` computed.
        if self.model.orbit.is_tidal_locked and not self.mu_from_obs:
            try:
                self.raw_flux = model.emission.raw_flux
                # self.flux = model.emission.flux
                self.factor = model.emission.factor
                self.factor_normalized = model.emission.factor_normalized
            except:
                super().compute(model) # compute self.flux

        for i, phase in enumerate(tqdm(self.phases)):
            self.model.observer.position_from_phase(phase)

            if not self.model.orbit.is_tidal_locked or self.mu_from_obs:
                # `raw_flux` need to be computed for each phase.
                super().compute(model)  # re-compute self.flux # very costly
            else:
                # Only need to update the projection
                self.compute_projection()

            self.flux[i] = np.sum(self.raw_flux * self.projected_surface[..., None], axis=(0,1))

        self.model.observer.longitude = initial_longitude   # resurrect initial setup

        if self.planet_to_star_flux_ratio is True:
            self.flux_normalized = np.copy(self.flux)
            try:
                self.flux_normalized /= self.factor_normalized.value
            except:
                self.flux_normalized /= self.factor_normalized

        try:
            self.flux /= self.factor.value
        except:
            self.flux /= self.factor # float case

    def outputs(self):
        return ['wns', 'flux', 'flux_normalized']
