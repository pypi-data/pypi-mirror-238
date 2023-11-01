import ntpath
import os
from copy import deepcopy
from typing import Literal, Optional

import exo_k as xk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

from ..log import Logger
from ..util.util import *


def time_fmt(time, units=None):
    """Format time in days, hours or seconds."""
    if (np.ndim(time)==0 and time > 3600*24) or units in ("Days","days","d"): 
        return time/(3600*24), "days"
    elif (np.ndim(time)==0 and time > 3600) or units in ("Hours","hours","h"):
        return time/3600, "hours"
    else:
        return time, "s"
    
def units_from_dim(dim="wls"):
    """Get units from dim (wls/wns/phases/times)."""
    if dim == 'phases':
        return 'degrees'
    elif dim == 'times':
        return 's'
    elif dim == 'wls':
        return r"$\mu m$"
    else:
        return r"$cm^{-1}$"
    
def label_from_dim(dim="wls", units=None):
    """Returns spectral label (either wavelength or wavenumber)."""
    if units is None:
        units = units_from_dim(dim)
    if dim == 'phases':
        return 'Phase angle ({units})'
    elif dim == 'times':
        return f'Time ({units})'
    elif dim == 'wls':
        return rf"$\lambda$ ({units})"
    else:
        return rf"$\nu$ ({units})"


def get_spectral(wl, wn, w_units="wls"):
    """Returns either wavelength or wavenumber based on `w_units` value ('wls', 'wns')."""
    if w_units == "wls":
        return wl
    if w_units != "wns":
        Logger("plot").warning(f"w_units = {w_units} not recognized (should be wls/wns). We will use wavenumbers.")
    return wn

def clipped_colorbar(CS,
                     extend: Optional[Literal['neither', 'min', 'max', 'both']] = None,
                     **kwargs):
    # Source: https://stackoverflow.com/a/55403314/12774714
    from matplotlib.cm import ScalarMappable
    from numpy import arange, floor, ceil
    if CS is None:
        return
    try:
        fig = CS.ax.get_figure()
    except AttributeError as e:
        fig = CS.axes.get_figure()
    vmin = CS.get_clim()[0]
    vmax = CS.get_clim()[1]

    m = ScalarMappable(cmap=CS.get_cmap())
    m.set_array(CS.get_array())
    m.set_clim(CS.get_clim())

    step = CS.levels[1] - CS.levels[0]

    cliplower = CS.zmin < vmin
    clipupper = CS.zmax > vmax

    noextend = extend == 'neither'

    # set the colorbar boundaries
    boundaries = arange((floor(vmin / step) - 1 + 1 * (cliplower and noextend)) * step,
                        (ceil(vmax / step) + 1 - 1 * (clipupper and noextend)) * step, step)

    # if the z-values are outside the colorbar range, add extend marker(s)
    # This behavior can be disabled by providing extend='neither' to the function call

    if extend is None or extend in ['min', 'max']:
        extend_min = cliplower or extend == 'min'
        extend_max = clipupper or extend == 'max'

        if extend_min and extend_max:
            extend = 'both'
        elif extend_min:
            extend = 'min'
        elif extend_max:
            extend = 'max'

    return fig.colorbar(m, boundaries=boundaries,extend=extend, **kwargs)


def path_leaf(path):
    head, tail = ntpath.split(path)

    if (tail == "output_pytmosph3r.h5" or "output_pytmosph3r.h5") and head not in (".", ""):
        return head  # they all have the same name anyway

    return tail or ntpath.basename(head)


def legend_out(ax, x0=1,y0=1, direction = "v", padpoints = 3,**kwargs):
    otrans = ax.figure.transFigure
    t = ax.legend(bbox_to_anchor=(x0,y0), loc=1, bbox_transform=otrans,**kwargs)
    plt.tight_layout(pad=0)
    ax.figure.canvas.draw()
    plt.tight_layout(pad=0)
    ppar = [0,-padpoints/72.] if direction == "v" else [-padpoints/72.,0]
    trans2=matplotlib.transforms.ScaledTranslation(ppar[0],ppar[1],ax.get_figure().dpi_scale_trans)+\
             ax.figure.transFigure.inverted()
    tbox = t.get_window_extent().transformed(trans2 )
    bbox = ax.get_position()
    if direction=="v":
        ax.set_position([bbox.x0, bbox.y0,bbox.width, tbox.y0-bbox.y0])
    else:
        ax.set_position([bbox.x0, bbox.y0, tbox.x0 - bbox.x0, bbox.height])


class BasePlot(Logger, xk.util.spectral_object.Spectral_object):
    x_colors = {'H2O': 'red', 'CO': '#BFFF00','H2': 'black',  'He': 'blue', 'TiO': 'green', 'VO': 'purple',
                'H': '#ff69b4', 'K': 'cyan', 'CH4': 'cyan', 'NH3': 'magenta', 'N2': '#faebd7',
                'PH3': '#2e8b57', 'H2S': '#eeefff', 'Fe': '#da70d6', 'FeH': '#ff7f50',
                'CrH': '#cd853f', 'Na': '#bc8f8f', 'CO2': '#5f9ea0', 'HCN': '#daa520'}
    modes = ["transmission", "emission", "lightcurve", "phasecurve"]
    interactive = True

    def __init__(self, name, *args, **kwargs):
        """Default values for plots."""
        self.altitudes = ["surface", "middle", "top"]
        """Altitudes to plot. Possible values are indices or :attr:`surface`, :attr:`top` or :attr:`middle`."""

        self.latitudes = ["north", "equator", "south"]
        """Latitudes to plot. Possible values are indices or :attr:`north`, :attr:`south` or :attr:`equator`. :attr:`north` is latitude :attr:`0`."""

        self.latitude = "north"
        self.longitudes = ["day", "terminator", "night"]
        """Longitudes to plot. Possible values are indices or :attr:`day`, :attr:`night` or :attr:`terminator`. :attr:`night` is longitude :attr:`0`."""

        self.longitude = "day"

        self.w_index = None

        super().__init__(name or self.__class__.__name__)

    @staticmethod
    def figure(ax=None, figsize=None):
        """Simply create a figure. Returns a boolean 'save' on top of fig and ax, to know if we should save the figure or not."""

        save = False
        fig = None

        if ax is None:
            save = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        return fig, ax, save

    def plot_columns(self, func,
                     latitudes=None, longitudes=None,
                     name="plot", legend=None, figsize=None, nrows=None, ncols=None, title=None,
                     *args, **kwargs):
        """Iterate over vertical columns (lat,lon)."""
        if latitudes is None:
            latitudes=self.latitudes
        else:
            self.latitudes=latitudes

        if longitudes is None:
            longitudes=self.longitudes
        elif longitudes == "all":
            longitudes = np.arange(self.model.n_longitudes)
        else:
            self.longitudes=longitudes

        longitudes = np.atleast_1d(longitudes)[:self.model.n_longitudes]
        latitudes = np.atleast_1d(latitudes)[:self.model.n_latitudes]
        if nrows is None:
            nrows = len(latitudes)
        if ncols is None:
            ncols = len(longitudes)
        
        if figsize is None:
            figsize = (3.2 * (ncols+1), 3.2 * nrows)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True, figsize=figsize)
        ax = axes
        if nrows > 1 and ncols > 1: 
            axes = np.reshape(axes, (nrows, ncols))

        for i, lat_idx in enumerate(latitudes):
            for j, lon_idx in enumerate(longitudes):
                self.latitude = lat_idx
                self.longitude = lon_idx
                if nrows > 1:
                    ax = axes[i]
                    if ncols > 1: 
                        ax = axes[i,j]
                elif ncols > 1: 
                    ax = axes[j]
                label = None
                if nrows == 1 and ncols == 1: 
                    lat_value = np.degrees(self.model.grid.mid_latitudes[get_latitude_index(lat_idx, self.n_latitudes)])
                    lon_value = np.degrees(self.model.grid.mid_longitudes[get_longitude_index(lon_idx, self.n_longitudes)])
                    label = (lat_value, lon_value)
                    if len(latitudes) < 2:
                        label = lon_value
                    if len(longitudes) < 2:
                        label = lat_value
                        
                results = func(ax=ax, latitude=lat_idx, longitude=lon_idx, label=label, *args, **kwargs)

        ax = fig.add_subplot(111, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)

        if legend is not None:
            legend(ax=axes, fig=fig, title=title)

        self.save_plot(name)

    def plot_column(self, ax, x, y, latitude=None, longitude=None, *args, **kwargs):
        """Plot something at column (lat,lon)."""

        if latitude is None:
            latitude = self.latitude

        if longitude is None:
            longitude = self.longitude

        hx = get_column(x, latitude, longitude)
        hy = get_column(y, latitude, longitude)

        if isinstance(hx, (float, str)):
            hx = np.full(hy.shape, hx)
        elif isinstance(hy, (float, str)):
            hy = np.full(hx.shape, hy)

        ax.plot(hx, hy, *args, **kwargs)

    def save_column(self, label):
        return label + "_" + self.latitude + "_" + self.longitude

    def set_title(self, ax=None, title=None, *args, **kwargs):
        if title is None:
            try:
                title = self.title
            except:
                return # No title to plot

        try:
            ax.set_title(title, *args, **kwargs)
        except:
            plt.title(title, *args, **kwargs)

    def legend(self, ax=None, fig=None, ncol=1, prop={'size':11}, 
               frameon=False,  *args, **kwargs):
        if ax is not None:
            legend = ax.legend(ncol=ncol, prop=prop, frameon=frameon, *args, **kwargs)
        else:
            legend = plt.legend(ncol=ncol, prop=prop, frameon=frameon, *args, **kwargs)

        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('white')
        legend.get_frame().set_alpha(0.8)

    def save_plot(self, name="plot", suffix=None, out_folder=None, interactive=None, *args, **kwargs):
        if suffix is None:
            try:
                suffix = self.suffix
            except:
                suffix = "pytmosph3r"
        if out_folder is None:
            try:
                out_folder = self.out_folder
            except:
                out_folder = "."
        if interactive is None:
            try:
                interactive = self.interactive
            except:
                interactive = True
        filename = os.path.join(out_folder, f'{name}_{suffix}.pdf')
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        plt.savefig(filename, bbox_inches='tight', *args, **kwargs)
        print(f"Saved to `{filename}`")

        if interactive:
            plt.show()
        else:
            plt.close('all')


    def legend2D(self, axes):
        if not hasattr(axes, "__len__") or len(axes.flatten()) == 1:
            return

        axes_latitudes = axes
        if np.ndim(axes) > 1:
            axes_latitudes = axes[:,0]
        if len(axes_latitudes) == len(self.latitudes):
            for ax, lat in zip(axes_latitudes, self.latitudes):
                ax.annotate("Latitude:\n %s"% get_latitude_index(lat, self.n_latitudes),
                    xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 10, 0), xycoords=ax.yaxis.label,
                    textcoords='offset points', size='large', ha='right', va='center')
        
        axes_longitudes = axes
        if np.ndim(axes) > 1:
            axes_longitudes = axes[0]
        if len(axes_longitudes) == len(self.longitudes):
            for ax, lon in zip(axes_longitudes, self.longitudes):
                ax.annotate("Longitude:\n %s"% get_longitude_index(lon, self.n_longitudes),
                    xy=(0.5, 1), xytext=(0, 5), xycoords='axes fraction',
                    textcoords='offset points', size='large', ha='center', va='baseline')

    def spectrum_label(self, mode):
        """Label for 'spectra' plots.

        Args:
            mode (str): Among transmission/emission/lightcurve/phasecurve. Defaults to transmission.
        """
        if mode in ("emission", "phasecurve"):
            if self.mode(mode).planet_to_star_flux_ratio:
                return r"$F_P/F_S$"
            return r"Flux $(W/m^2/cm^{-1})$"
        return r"$(R_p/R_s)^2$"  # by default plot transmission spectra

    def get_value_dim(self, index, dim):
        """Returns the value at :attr:`index` in the dimension :attr:`dim`.

        Args:
            index (int): Index of the value we're looking for.
            dim (str): Dimension of the value we're looking for. Among "altitude", "latitude" or "longitude".
        """

        if isinstance(index, (str,)):
            return index  # return text as is

        unit = "°"

        if dim == "altitude":
            if self.vertical_in_pressure:
                unit = 'Pa'
                array = self.pressure_levels
            else:
                unit = 'm'
                if self.h_unit == 1e6:
                    unit = 'Mm'
                elif self.h_unit == 1e3:
                    unit = 'Km'
                array = self.z
        elif dim == "latitude":
            array = np.degrees(self.grid.mid_latitudes)
        elif dim == "longitude":
            array = np.degrees(self.grid.mid_longitudes)
        else:
            self.error(f"I don't know dimension {dim}")
            return -1

        return f"{array[index]:.1f} {unit}"

    def bin_down(self, resolution=200, spectrum=None, copy=True):
        if spectrum is None:
            if self.spectrum:
                spectrum = self.spectrum
            else:
                return

        bingrid = xk.wavenumber_grid_R(spectrum.wnedges.min(),
                                       spectrum.wnedges.max(), resolution)

        if copy:
            return spectrum.bin_down_cp(bingrid)

        self.old_spectrum = deepcopy(spectrum)  # save just in case

        spectrum.bin_down(bingrid)

    def flux(self, mode=None, phase=None, wl=None, wn=None, resolution=None, noise=True, ax=None, color=None):
        """Get flux (spectrum or curve) of a mode, with a resolution of N points, noised or not. Equal to :math:`(Rp/Rs)^2` (if normalized).

        Args:
            mode (str, optional): transmission/emission/lightcurve/phasecurve. Defaults to None.
            phase (array | float, optional): Phase(s) to select. Incompatible with `wl` or `wn`. Defaults to None.
            wl (array | float, optional): Wavelength to select. Incompatible with `phase` or `wn`. Defaults to None.
            wl (array | float, optional): Wavenumber to select. Incompatible with `phase` or `wl`. Defaults to None.
            resolution (int, optional): Number of points to bin to. Not used with `wl` or `wn`. Defaults to None.
            noise (bool, optional): Noise the spectrum? Defaults to True.

        Returns:
            flux (`exo_k.Spectrum`) of which the X axis is either wavelengths, or phases.
        """
        phase = to_SI(phase) # just in case
        if (phase is not None or wl is not None or wn is not None) and mode not in ("lightcurve", "phasecurve"):
            self.warning(f"Mode {mode} does not have phases, so we will use light/phase-curve mode. If you want to select a specific mode, please use the 'mode' parameter.")
            if mode == "emission":
                mode = "phasecurve"
            elif mode == "transmission":
                mode = "lightcurve"
            else:
                try: # try to guess automatically which mode has been computed
                    return self.flux(mode="lightcurve", phase=phase, wl=wl, wn=wn, resolution=resolution, ax=ax, color=color)
                except (AttributeError, TypeError):
                    return self.flux(mode="phasecurve", phase=phase, wl=wl, wn=wn, resolution=resolution, ax=ax, color=color)
        if phase is not None:
            phases = np.asarray(self.getattr(mode, "phases"))
            ph_index = np.clip(phases.searchsorted(np.float_(phase)), 0, len(phases)-1)
            wns = self.getattr(mode, "wns")
            wnedges = self.getattr(mode, "wnedges")
            flux = xk.Spectrum(self.getattr(mode, "flux")[ph_index], wns, wnedges)
            self.ph_index = ph_index
        elif wl is not None or wn is not None and self.getattr(mode, "phases") is not None: # added `and self.getattr(mode, "phases") is not None` to patch bug
            # BUG: TypeError: loop of ufunc does not support argument 0 of type NoneType which has no callable degrees method
            phases = np.degrees(self.getattr(mode, "phases"))
            phases_edges = phases[1:]+np.diff(phases)/2
            phases_edges = np.concatenate([phases[:2]-np.diff(phases[:3])/2, phases_edges])
            i = self.find_spectral(wl, wn, mode=mode)
            flux = xk.Spectrum(self.getattr(mode, "flux")[..., i], phases, phases_edges)
            flux.phases = self.mode(mode).phases
            # flux.times = self.mode(mode).times # BUG: times disabled due to issue if not existing
            # NOTE: X axis is phases here! not wns (a bit of a trick)
        elif mode:
            try:
                if mode in ("lightcurve", "phasecurve"):
                    flux = self.mode(mode).flux.copy()
                else:
                    flux = self.mode(mode).spectrum.copy()
                    flux = xk.Spectrum(flux["value"], flux["wns"], flux["wnedges"])
            except Exception as e:
                self.info("Failed to get 'flux' from '%s' mode from %s."%(mode, self.f.filename))
                return None
        else:
            flux = self.spectrum
            if flux is None:
                for mode in self.modes:
                    try: # try other modes, maybe it has been computed
                        flux = self.flux(mode=mode, phase=phase, wl=wl, wn=wn, resolution=resolution, ax=ax, color=color)
                        assert flux is not None
                        self.info(f"Will try to plot spectrum from '{mode}' mode ('None' given).")
                        break
                    except:
                        continue # mode doesn't have flux

        if noise:
            if not isinstance(noise, (bool)):
                if isinstance(noise, (float, int)):
                    noise = np.random.normal(0, noise, len(flux.wns))

                noise_spectrum = xk.Spectrum(noise, wns=flux.wns, wnedges=flux.wnedges)
                flux = flux + noise_spectrum
            elif self.noise:
                noise = self.noise
                if isinstance(self.noise, (float, int)):
                    noise = np.random.normal(0, noise, len(flux.wns))

                noise_spectrum = xk.Spectrum(noise, wns=flux.wns, wnedges=flux.wnedges)
                flux = flux + noise_spectrum
            elif self.noised_spectrum is not None and mode is None:
                # this should probably not happen, since self.noise will be used first
                noise = xk.Spectrum(np.full_like(self.noised_spectrum.wns, self.noise), self.noised_spectrum.wns, self.noised_spectrum.wnedges)
                flux = self.noised_spectrum

                try:
                    below = flux.value-noise.value
                    above = flux.value+noise.value
                    ax.fill_between(flux.wls, below, above, alpha=0.4, zorder=-2, edgecolor='none', color=color)
                except:
                    pass

        if resolution:
            flux = self.bin_down(resolution, flux)

        return flux

    def curve(self, mode=None, **kwargs):
        """Returns light/phasecurve (as an array). Lightcurve is :math:`1-(Rp/Rs)^2`."""
        if mode in ("transmission", "lightcurve"):
            flux = self.flux(mode="lightcurve", **kwargs)
            if isinstance(flux, xk.Spectrum):
                return 1-flux.value
            return 1-flux
        flux = self.flux(mode="phasecurve", **kwargs)
        if isinstance(flux, xk.Spectrum):
            return flux.value
        return flux

    def x_axis_curve(self, x_axis="phases", x_units=None, mode="lightcurve"):
        x = np.degrees(self.mode(mode).phases)
        if x_axis == "times":
            try:
                times = self.mode(mode).times
                assert times is not None
                x = times
            except Exception as e:
                self.info(f"Could not use time as x-axis. Maybe missing period in Orbit()? Full error:\n{e}")
                x_axis = "phases"

        xlabel = 'Phase angle (degrees)'
        if x_axis == "times":
            if x_units is None:
                x_units = time_fmt(x[-1])[-1] # use last value as scale for units
            x = time_fmt(x, x_units)[0]
            xlabel = f'Time ({x_units})'
        
        return x, xlabel
    
    def init_time(self, phase=None, time=None, time_units=None):
        phase = to_SI(phase, u.rad)
        if isinstance(time, u.Quantity):
            time_units = time.unit
        time = to_SI(time, u.s)
        label_prefix = r"$\phi$"
        if time: # time has priority
            try:
                phase = self.model.orbit.phase(time)
                label_prefix = "t"
            except Exception as e:
                self.error(f"time was provided ({time}), but self.model.orbit.period is missing. Please set it if you want plots in time. Will use phases meanwhile...")
                time = None
        return phase, time, label_prefix, time_units
        
    
    def init_spectral(self, wl=None, wn=None, default_wl=15, mode=None):
        """Init both wavelengths and wavenumbers to equivalent values.

        Returns:
            tuple: (ws, wl, wn, w_units) where ws is the spectral array corresponding to w_units (either wls or wns).
        """
        obj = self
        if mode is not None:
            try:
                self.mode(mode).wls
                obj = self.mode(mode)
            except:
                obj = self #
        ws = obj.wns
        w_units = "wns"

        if wl is None and wn is None or wn is True:
            wl = default_wl
            wn = 10000./default_wl
        elif wn is None:
            wn = 10000./np.float_(wl)
            w_units = "wls"
            ws = obj.wls
        else:
            wl = 10000./np.float_(wn)

        wn = np.float_(np.float_(wn)) # don't ask
        wl = np.float_(np.float_(wl))

        return ws, wl, wn, w_units

    def get_spectral(self, wl=None, wn=None, w_units=None, default_wl=15, mode=None):
        """Choose which spectral units to plot (wavelengths or wavenumbers)."""
        obj = self
        if mode is not None:
            try: # curve modes could have subsets of wns (faster calculations)
                assert (self.mode(mode).wls is not None)
                obj = self.mode(mode)
            except:
                obj = self #
        if w_units:
            return getattr(obj, w_units), get_spectral(wl, wn, w_units), w_units
        if wl is None and wn is None:
            return obj.wns, 10000./np.float_(default_wl), "wns"
        elif wn is None:
            return obj.wls, np.float_(np.float_(wl)), "wls"  # don't ask
        else:
            return obj.wns, np.float_(np.float_(wn)), "wns"

    def find_spectral(self, wl=None, wn=None, **kwargs):
        """Find the index of spectral point equal to either wavelength `wl` or wavenumber `wn`. Defines :attr:`w_index`.
        """
        ws, w, w_units = self.get_spectral(wl, wn, **kwargs)

        # assume array is sorted
        sorter = None; a = 0; b = 1

        # check if array is reverse sorted
        if w_units != "wns":
            if np.size(ws)>1 and ws[1] < ws[0]:
                sorter = np.arange(ws.size)[::-1]
                a = len(ws)
                b = -1

        self.w_index = np.clip(a+b*ws.searchsorted(np.float_(w), sorter=sorter), 0, len(ws)-1)
        return self.w_index #, ws[self.w_index]

    def mode(self, mode):
        """Returns 'mode' object (transmission/lightcurve/emission/phasecurve). Returns self if None."""
        if mode is None:
            return self
        return getattr(self.__class__,mode).__get__(self, self.__class__)

    def getattr(self, mode, attr):
        """Get attribute :attr:`attr` from mode :attr:`mode`."""

        if mode is None:
            try:
                value = getattr(self.mode("lightcurve"), attr)
            except:
                value = getattr(self.mode("phasecurve"), attr)
        else:
            try: # get attr from mode
                value = getattr(self.mode(mode), attr)
            except:
                try: # if failed, try to get it from main class
                    value = getattr(self, attr)
                except:
                    return None

        return value


class LoadPlot:
    """Class to load HDF5 file or :attr:`model` attribute. Inherited by :class:`~pytmosph3r.plot.plot.Plot`.
    """

    @property
    def model(self):
        if not hasattr(self, "_model") or self._model is None:
            if self.f:
                self._model = self.f.read('Model')
                self._model.output_file = None # don't write it again!
                # self._model.build()
                self._model.atmosphere = self._model.input_atmosphere
                self._model.atmosphere.__dict__.update(self.atmosphere.__dict__)

                try:
                    self._model.wns = self.f.read('Output/wns')
                    self._model.wnedges = self.f.read('Output/wns')
                except:
                    pass

        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def atmosphere(self):
        """Dict."""
        if not hasattr(self, "_atmosphere") or self._atmosphere is None:
            if self.f:
                self._atmosphere = self.f.read('Model/input_atmosphere')
                atmosphere = self.f.read('Output/atmosphere', dict)
                try:
                    self._atmosphere.__dict__.update(atmosphere.__dict__)
                except AttributeError as e:
                    try:
                        self._atmosphere.__dict__.update(atmosphere)
                    except TypeError as e:
                        return self._atmosphere
            else:
                self._atmosphere = self.model.atmosphere
        if self._atmosphere.altitude is None:
            self._atmosphere.build()
        return self._atmosphere

    def set_mode_attr(self, mode):
        """Set attributes for modes (emission/phasecurve/transmission/lightcurve), which have parameters both in Model and in Output.
        """

        if not hasattr(self, "_"+mode) or self.__dict__["_"+mode] is None:
            if self.f:
                self.__dict__["_"+mode] = self.f.read('Model/'+mode)
                if self.__dict__["_"+mode] is None:
                    return
                try:
                    output_mode = self.f.read('Output/'+mode, class_obj=dict)
                    self.__dict__["_"+mode] = merge_attrs(self.__dict__["_"+mode],  output_mode)
                    self.__dict__["_"+mode].model = self.model
                except:
                    self.__dict__["_"+mode].build(self.model)
                    # pass
            else:
                self.__dict__["_"+mode] = self.model.__dict__[mode]
            if hasattr(self.__dict__["_"+mode], "kwargs") and self.__dict__["_"+mode].kwargs is not None:
                self.__dict__["_"+mode].__dict__.update(self.__dict__["_"+mode].kwargs)

        return self.__dict__["_"+mode]

    def transmission(self):
        return self.set_mode_attr("transmission")

    def emission(self):
        return self.set_mode_attr("emission")

    def lightcurve(self):
        return self.set_mode_attr("lightcurve")

    def phasecurve(self):
        return self.set_mode_attr("phasecurve")

    def mode(self, mode):
        """Returns 'mode' object (transmission/lightcurve/emission/phasecurve). Returns self if None."""
        if mode is None:
            return self
        return getattr(self.__class__,mode).__get__(self, self.__class__)()

    @property
    def wns(self):
        if not hasattr(self, "_wns") or self._wns is None:
            if self.f:
                self._wns = self.f.read('Output/wns')
            else:
                self._wns = self.model.wns

        return self._wns
    @property
    def wnedges(self):
        if not hasattr(self, "_wnedges") or self._wnedges is None:
            if self.f:
                self._wnedges = self.f.read('Output/wnedges')
            else:
                self._wnedges = self.model.wnedges
        return self._wnedges
    @property
    def spectrum(self):
        if not hasattr(self, "_spectrum") or self._spectrum is None:
            if self.f:
                value = self.f.read('Output/spectrum_value')
                wns = self.f.read('Output/wns')
                wnedges = self.f.read('Output/wnedges')
                if value is None:
                    return None
                self._spectrum = xk.Spectrum(value, wns, wnedges)
            else:
                try:
                    self._spectrum = self.model.spectrum.copy()
                except AttributeError:
                    return None
        return self._spectrum

    @spectrum.setter
    def spectrum(self, value):
        self._spectrum = value
        self._wns = value.wns
        self._wnedges = value.wnedges
        self._noised_spectrum = value.copy()

    @property
    def noised_spectrum(self):
        try:
            if not hasattr(self, "_noised_spectrum") or self._noised_spectrum is None:
                if self.f:
                    self._noised_spectrum = self.spectrum.copy()
                    self._noised_spectrum.value = self.f.read('Output/spectrum_noised')
                else:
                    self._noised_spectrum = self.model.noised_spectrum
            return self._noised_spectrum
        except:
            return None

    @noised_spectrum.setter
    def noised_spectrum(self, value):
        self._noised_spectrum = value
        self._wns = value.wns
        self._wnedges = value.wnedges


    @property
    def noise(self):
        """Planet radius."""
        if self.f:
            return self.f.read('Model/noise')
        else:
            return self.model.noise

    def transmittance(self, phase=None, wl=None, wn=None):
        if phase is not None:
            try:
                ph_min = self.mode("lightcurve").transmittance_phases.min()
                if phase < ph_min:
                    phase = ph_min
                ph_max = self.mode("lightcurve").transmittance_phases.max()
                if phase > ph_max:
                    phase = ph_max
                if not hasattr(self.mode("lightcurve"), "rays_opacities"):
                    pass # we will try transmission transmittance, below
                else:
                    return self.interp_transmittances(phase, wl, wn)
            except ValueError:
                pass # we will try transmission transmittance, below

        if not hasattr(self, "_transmittance") or self._transmittance is None:
            try:
                i = self.find_spectral(wl, wn)
                self._transmittance = self.mode("transmission").transmittance[..., i]
            except:
                return None

        return self._transmittance

    def interp_transmittances(self, phase, wl=None, wn=None):
        if not hasattr(self, "_interp_transmittances") or self._interp_transmittances is None:
            lc = self.mode("lightcurve")
            i = self.find_spectral(wl, wn, mode="lightcurve")
            rays_opacities = lc.rays_opacities[..., i] # no need to load every wn

            if lc.n_transmittances > 1:
                self._interp_transmittances = sp.interpolate.interp1d(lc.transmittance_phases, 1-rays_opacities, axis=(0))
            else:
                self._interp_transmittances = lambda x: 1-rays_opacities[0]

        return self._interp_transmittances(phase)

    @property
    def grid(self):
        if not hasattr(self, "_grid") or self._grid is None:
            self._grid = self.atmosphere.grid

        return self._grid

    @property
    def n_layers(self):
        return self.grid.n_vertical

    @property
    def n_levels(self):
        return self.n_layers+1

    @property
    def n_longitudes(self):
        return self.grid.n_longitudes

    @property
    def n_latitudes(self):
        return self.grid.n_latitudes

    @property
    def Rp(self):
        """Planet radius."""
        if self.f:
            return self.f.read('Model/planet/radius')/self.h_unit
        else:
            return self.model.planet.radius/self.h_unit
    @property
    def Rs(self):
        """Star radius."""
        if self.f:
            return self.f.read('Model/star/radius')/self.h_unit
        else:
            return self.model.star.radius/self.h_unit

    @property
    def R(self):
        """Planet radius scaled using :attr:`r_factor`."""
        return self.Rp * self.r_factor

    @property
    def z_idx(self):
        if not hasattr(self, "_z_idx") or self._z_idx is None:
            try:
                if self.vertical_in_pressure:
                    self._z_idx = np.where(self.pressure_levels >= self.p_min)
                else:
                    self._z_idx = np.where(self.input_z < self.z_levels.max())
                self.grid.n_vertical = len(self._z_idx[0])
            except:
                self._z_idx = slice(0,self.n_layers)

        return self._z_idx

    @property
    def input_z(self):
        return self.atmosphere.altitude/self.h_unit

    @property
    def input_z_levels(self):
        try:
            return self.atmosphere.altitude_levels/self.h_unit
        except:
            return self.input_z

    @property
    def z_levels(self):
        if not hasattr(self, "_z_levels") or self._z_levels is None:
            self._z_levels = self.input_z_levels[np.where(self.input_z_levels < self.zmax)]

        return self._z_levels

    @property
    def z(self):
        if not hasattr(self, "_z") or self._z is None:
            self._z = self.input_z[self.z_idx]

        return self._z

    @property
    def altitude(self):
        return self.z

    @property
    def r(self):
        return self.R + self.z

    def rays(self, mode="transmission"):
        if not hasattr(self, "_rays") or self._rays is None:
            if self.f:
                try:
                    self._rays = self.f.read(f'Model/{mode}/rays')
                    output_rays = self.f.read(f'Output/{mode}/rays', class_obj=dict)
                    self._rays.__dict__.update(output_rays)
                except Exception as e:
                    pass

            if self._model is not None:
                try:
                    self._rays = self.model.__dict__[mode].rays
                except Exception as ex:
                    return None
            try:
                self._rays.build(self.model)
            except Exception as e:
                self.error("Could not build rays: %s"%e)

        return self._rays

    @property
    def pressure(self):
        if not hasattr(self, "_pressure") or self._pressure is None:
            self._pressure = self.atmosphere.pressure

        return self._pressure[self.z_idx]

    @property
    def pressure_levels(self):
        if not hasattr(self, "_pressure_levels") or self._pressure_levels is None:
            if self.f:
                self._pressure_levels = self.f.read('Model/input_atmosphere/pressure')
            else:
                self._pressure_levels = self.model.input_atmosphere.pressure

            if self._pressure_levels.ndim > 1:
                self._pressure_levels = self._pressure_levels[:,0,0]

        return self._pressure_levels

    @property
    def p_min(self):
        if not hasattr(self, "_p_min") or self._p_min is None:
            try:
                if self.f:
                    self._p_min = self.f.read('Model/input_atmosphere/min_pressure')
                else:
                    self._p_min = self.model.input_atmosphere.min_pressure
            except:
                self._p_min = 0

        return self._p_min

    @property
    def temperature(self):
        if not hasattr(self, "_temperature") or self._temperature is None:
            self._temperature = self.atmosphere.temperature

        return self._temperature[self.z_idx]

    @property
    def gas_mix_ratio(self):
        if not hasattr(self, "_gas_mix_ratio") or self._gas_mix_ratio is None:
            self._gas_mix_ratio = self.atmosphere.gas_mix_ratio

            for gas, value in self._gas_mix_ratio.items():
                if not isinstance(self._gas_mix_ratio[gas], (float, str)):
                    self._gas_mix_ratio[gas] = self._gas_mix_ratio[gas][self.z_idx]

        return self._gas_mix_ratio

    @property
    def aerosols(self):
        if not hasattr(self, "_aerosols") or self._aerosols is None:
            self._aerosols = self.atmosphere.aerosols

            for a, a_dict in self._aerosols.items():
                for key, value in a_dict.items():
                    if hasattr(self._aerosols[a][key], "__len__") and not isinstance(self._aerosols[a][key], str):
                        self._aerosols[a][key] = self._aerosols[a][key][self.z_idx]

        return self._aerosols

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    @property
    def shape(self):
        return self.grid.shape

def plot_sector_star(rS, aS, Rs, r, a, r_i=None, a_i=None, ax=None):
    """Plot star at position (rS, aS), radius Rs over sector(s) with bounds r and a. r_i and a_i are (optional) intersection points with a and r, respectively."""
    from matplotlib.transforms import Affine2D
    import pylab as pl
    import matplotlib.pyplot as plt
    show = False
    if ax is None:
        fig = plt.figure(figsize=(5,3.5))
        ax = fig.add_subplot(111, projection='polar')
        show = True
    if np.ndim(r) == 0:
        r = [0, r]
    st = pl.Circle((rS, aS), Rs, transform=(Affine2D().rotate(ax._theta_offset.get_matrix()[0, 2]) + ax.transProjectionAffine + ax.transAxes), color="yellow", alpha=0.4)
    core = pl.Circle((0, 0), r[0], transform=(Affine2D().rotate(ax._theta_offset.get_matrix()[0, 2]) + ax.transProjectionAffine + ax.transAxes), color="black", alpha=0.4)
    atmo = pl.Circle((0, 0), r[-1], transform=(Affine2D().rotate(ax._theta_offset.get_matrix()[0, 2]) + ax.transProjectionAffine + ax.transAxes), color="black", alpha=0.2)
    ax.add_artist(atmo)
    ax.add_artist(core)
    ax.add_artist(st)
    ax.set_theta_zero_location("N")
    if a_i is not None:
        a_i = np.asarray(a_i).T
        r_i = np.asarray(r_i).T
        for a_j in a_i:
            ax.scatter(a_j, r, marker='.', color="blue")
        for r_j in r_i:
            idx = np.where(r_j > 0)
            ax.scatter(a[idx], r_j[idx], marker='.', color="red")
    r = np.insert(r,0,0)
    for a_j in a:
        ax.plot(np.full_like(r, a_j), r)
    ax.set_rmax(1.2*r[-1])
    if show:
        plt.show()