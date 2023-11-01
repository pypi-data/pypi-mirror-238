import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # for x.p_id in ids issue
from typing import Literal, Optional

import matplotlib as mpl
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt, ticker

from .modelplot import CurvePlot, Plot
from .plotutils import *


class Comparison(Plot):
    """Compare (and plot) multiple models."""
    def __init__(self, models=None,title=None,suffix=None,cmap='Paired',out_folder='.', interactive=None):
        """Select models to compare with :attr:`models`."""

        BasePlot.__init__(self, self.__class__.__name__)
        self.models = np.array([x for x in models if x is not None])
        if len(self.models) <= 1:
            self.warning("No models to compare ("+str(len(models))+")")
        self.title = title
        if interactive in (False, True):
            self.interactive = interactive
        self.cmap = mpl.cm.get_cmap(cmap)
        self.suffix=suffix
        if self.suffix is None:
            self.suffix = "comp_output"
        self.out_folder=out_folder

        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)

    @property
    def wns(self):
        try:
            return self.models[0].wns
        except:
            return None
    @property
    def wls(self):
        try:
            return self.models[0].wls
        except:
            return None

    def transmittance_map(self, ids=None, *args, **kwargs):
        """Same parameters as :func:`.plot.Plot.transmittance_map`.

        Args:
            ids (list, optional) : List of ids (`label` parameter) of models to plot. For example ['1D', '2D', '3D'] if you created :code:`Plot(model, label='1D')`, etc.
        """
        if ids is None:
            ids=np.array([m.p_id for m in self.models])
        for model in filter(lambda x: x.p_id in ids, self.models):
            model.transmittance_map(*args, **kwargs)

    def plot_spectra(self, mode=None, title="Spectra", ids=None, ax=None, figsize=(4,4), legend=True, ref=0, savename=None, func="plot_spectrum", *args, **kwargs):
        """Plot spectra (select `mode` for emission/transmission, etc).

        Args:
            mode (str, optional): Among [transmission, emission, lightcurve, phasecurve]. Defaults to None (in which case the default spectrum is chosen).
            ids (list, optional) : List of ids (`label` parameter) of models to plot. For example ['1D', '2D', '3D'] if you created :code:`Plot(model, label='1D')`, etc.
            ref (int, optional): Index of the reference curve (plot as dashed). Defaults to None.
            savename (str, optional): Name of output file. Defaults to title.
            func (str, optional): Plot function to call for each model. Defaults to :func:`~pytmosph3r.plot.modelplot.ModelPlot.plot_spectrum`.
        """
        fig, ax, save = self.figure(ax, figsize)
        if ids is None:
            ids=np.array([m.p_id for m in self.models])
        dashes=[]
        for i, model in enumerate(list(filter(lambda x: x.p_id in ids, self.models))):
            if i == ref % len(self.models): # plot reference curve as dashed
                dashes=[5,2]
            err = getattr(model, func)(mode=mode, ax=ax, dashes=dashes, color=None, label=model.label, title=title, *args, **kwargs) # call plot_spectrum() by default
            if err:
                return err # error somewhere, don't plot
        if legend: # in case you don't need it
            ax.legend()
        if save:
            plt.tight_layout()
            if savename is None:
                savename = title.lower()
                if mode is not None:
                    savename = f"{savename}_{mode}"
            self.save_plot(savename)

    def plot_curves(self, mode="lightcurve", title="Lightcurves", wl=None, wn=None, *args, **kwargs):
        """Same parameters as :func:`~pytmosph3r.plot.modelplot.CurvePlot.plot_curve`. You can select IDs the same way as for :func:`plot_spectra`."""
        return self.plot_spectra(mode=mode, title=title, wl=wl, wn=wn, savename=title.lower(), func="plot_curve", *args, **kwargs)

    def plot_lightcurves(self, *args, **kwargs):
        """Same arguments as :func:`plot_curves`."""
        return self.plot_curves(mode="lightcurve", title="Lightcurves", *args, **kwargs)
    def plot_phasecurves(self, *args, **kwargs):
        """Same arguments as :func:`plot_curves`."""
        return self.plot_curves(mode="phasecurve", title="Phasecurves", *args, **kwargs)

    def diff_fluxes(self, mode=None, title="Spectra", ids=None, ax=None, time=None, phase=None, wl=None, wn=None, xlog=True, ylog=False, ppm=None, abs=False, resolution=None, figsize=(4,4), ylabel="Residual", x_axis="wls", x_units=None, ref=-1, ref_phase=None, savename=None, *args, **kwargs):
        """Compare fluxes together.

        Args:
            mode (str, optional): Among [transmission, emission, lightcurve, phasecurve]. Defaults to None (in which case the default spectrum is chosen).
            ids (list, optional) : List of differences of ids (`label` parameter). Example of use: :code:`comparison.diff_fluxes(ids=[["3D", "1D"],["2D", "1D"]])` if you created :code:`Plot(model, label='1D')`, etc..
            ref (int, optional): Index of model to take as a reference. Defaults to -1.
            ref_phase (float, optional) : if you want to compare the flux at `phase` against `ref_phase`.
            ppm (bool) : Y units in ppm or not.
            x_axis (str) : Choose X axis as "wls" or "wns", for wavelengths or wavenumbers, respectively.
            abs (bool, optional): Plot absolute difference. Defaults to False.
        """
        fig, ax, save = self.figure(ax, figsize)

        label = None
        unit = ""
        suffix = ""
        p_label = ""
        if ppm is None and mode in (None, "transmission", "lightcurve"):
            ppm = True
            unit = " ppm"

        # INFO: Set default value to x_label, to prevent it to be undefined
        xlabel = ''

        # we assume that all curves have the same spectral dimension here
        ws, wl, wn, w_units = self.models[ref].init_spectral(wl, wn)
        phase, time, label_prefix, time_units = self.models[ref].init_time(phase, time)

        if ids is None:
            ids = [[m.p_id, self.models[ref].p_id] for i, m in enumerate(self.models) if i != ref % len(self.models)]
        if ref_phase is None:
            ref_phase = np.atleast_1d(phase)

        for comp in ids:
            model0 = list(filter(lambda x: comp[0] == x.p_id, self.models))
            model1 = list(filter(lambda x: comp[1] == x.p_id, self.models))
            if len(model0) and len(model1):
                model0 = model0[0]
                model1 = model1[0]

            # either make phase OR wn vary, not both
            for j, ph in enumerate(np.atleast_1d(phase)):
                for i, w in enumerate(np.atleast_1d(wn)):
                    try:
                        spectrum0 = model0.flux(mode, phase=ph, wn=w)
                        ref = ref_phase[j] if ref_phase is not None else ph
                        spectrum1 = model1.flux(mode, phase=ref, wn=w)
                    except Exception as e:
                        continue
                    if spectrum0 is None or spectrum1 is None:
                        continue
                    if resolution:
                        spectrum0 = self.bin_down(resolution, spectrum0)
                        spectrum1 = self.bin_down(resolution, spectrum1)

                    # get x
                    if x_axis in ("phases","times"):
                        x_0, xlabel = model0.x_axis_curve(x_axis=x_axis, x_units=x_units, mode=mode)
                        x_1, xlabel = model1.x_axis_curve(x_axis=x_axis, x_units=x_units, mode=mode)
                    else:
                        x_0 = getattr(spectrum0, x_axis)
                        x_1 = getattr(spectrum1, x_axis)
                        xlabel = label_from_dim(x_axis)

                    # get y
                    y_1 = spectrum1.value
                    # if models don't have the same spectral ranges
                    y_0 = interp1d(x_0, spectrum0.value, assume_sorted=False)(x_1)
                    diff = (y_0 - y_1)
                    if ppm:
                        diff *= 1e6
                    if abs:
                        diff = np.abs(diff)
                    err = np.mean(np.abs(diff))

                    # labelling
                    if np.atleast_1d(time)[0] is not None:
                        t, units = time_fmt(time[model1.ph_index], time_units)
                        suffix = f" @ {t:.2f} {units}"
                    elif ph is not None:
                        suffix = f" @ {np.degrees(model1.getattr(mode, 'phases')[model1.ph_index]):.1f}°"
                    if w is not None:
                        suffix = f" @ {get_spectral(10000/w, w, w_units):.1f} {units_from_dim(w_units)}"
                    if (np.ndim(phase) and len(phase)>1) or (np.ndim(wn) and len(wn)>1):
                        p_label = suffix
                    label = f"{model0.label} - {model1.label}{p_label} = {err:.3g}{unit}"

                    ax.plot(x_1, diff, label=label, *args, **kwargs)
        if ylog:
            ax.set_yscale('log')
        if xlog:
            ax.set_xscale('log')
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        # ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))
        ax.set_xlabel(xlabel)
        if ppm:
            ax.set_ylabel(f"{ylabel} [ppm]")
        else:
            ax.set_ylabel(f"{ylabel}")
        #ax.grid()
        if label is None:
            return 1 # no plot
        if save:
            ax.legend()
            if (np.ndim(phase) and len(phase)<2) or (np.ndim(wn) and len(wn)<2):
                p_title = f"{suffix}"
            if title and suffix:
                p_title = f"{title} @ {suffix}"
            ax.set_title(f"{p_title}")
            plt.tight_layout()
            if savename is None:
                savename = title.lower()
            self.save_plot(f"diff_{savename}")
        return 0

    def diff_spectra(self, phase=None, *args, **kwargs):
        """
        Compare models using ids. Example of use: :code:`comparison.diff_spectra(ids=[["3D", "1D"],["2D", "1D"]])` if you created :code:`Plot(model, label='1D')`, etc..  See :func:`diff_fluxes` for more information.
        """
        return self.diff_fluxes(phase=phase, *args, **kwargs)

    def diff_curves(self, x_axis: Literal["times","phases"] = "times",  xlog=False, *args, **kwargs):
        """
        Compare phase/light-curves together. See :func:`diff_fluxes` for more information.
        """
        return self.diff_fluxes(xlog=xlog, x_axis=x_axis, *args, **kwargs)

    def diff_lightcurves(self, wl=None, wn=None, *args, **kwargs):
        """See :func:`diff_fluxes` for more information."""
        return self.diff_curves(mode="lightcurve", wl=wl, wn=wn, *args, **kwargs)
    def diff_phasecurves(self, wl=None, wn=None, *args, **kwargs):
        """See :func:`diff_fluxes` for more information."""
        return self.diff_curves(mode="phasecurve", wl=wl, wn=wn, *args, **kwargs)

    def plot_tp(self, ax=None, title="PT profile", logx=False, logy=True, figsize=(9,3)):
        """TP profile of one column."""
        fig, ax, save = self.figure(ax, figsize=(9,3))
        for model in self.models:
            self.plot_column(ax, model.temperature, model.pressure, label=model.label)
        if logy:
            ax.set_yscale('log')
        if logx:
            ax.set_xscale('log')
        if save:
            ax.set_title(title)
            self.tp_legend(ax, fig=ax.get_figure())
            self.save_plot("tp")

    def plot_zp(self, ax=None, title="ZP profile", logx=True, logy=False, figsize=(9,3)):
        """ZP profile of one column."""
        fig, ax, save = self.figure(ax, figsize=figsize)
        for model in self.models:
            self.plot_column(ax, model.pressure, model.z, label=model.label)
        if logy:
            ax.set_yscale('log')
        if logx:
            ax.set_xscale('log')
        # ax.legend()
        if save:
            ax.set_title(title)
            self.zp_legend(ax, fig)
            self.save_plot("zp")

    def plot_xprofile(self, ax=None, figsize=(9,3), *args, **kwargs):
        """Mixing ratio. longitude = 1 plots the terminator. Outdated?"""
        fig, ax, save = self.figure(ax, figsize=figsize)
        num_models = len(self.models)
        xmin=1
        gas_legends = {}
        models = []
        for model_idx, model in enumerate(self.models):
            dashes = [(num_models-model_idx)+2, (model_idx*3)+3]

            model_gas_legend, model_min, model_max = model.plot_xprofile(ax, dashes=dashes, *args, **kwargs)

            try:
                xmin = min(model_min, xmin)
            except:
                pass
            models.append(mpl.lines.Line2D([0], [0], dashes=dashes, label=model.label))
            gas_legends.update(model_gas_legend)

        ax.set_xlim(max(1e-12,xmin))
        if save:
            self.save_plot("vmr")
        return models, gas_legends

    def x_legend(self, axes, fig, legends):
        """Place legend with model + gas labels."""
        if isinstance(axes, (np.ndarray)):
            self.legend2D(axes)
            ax = axes.flatten()[0]
        else:
            ax = axes
        ax.invert_yaxis()
        plt.xlabel('Mixing ratio')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()

        fig.subplots_adjust(right=0.9, wspace=0.25, hspace=0.35)
        legends
        plt.gca().add_artist(fig.legend(handles=legends[0], loc=1))
        plt.gca().add_artist(fig.legend(handles=legends[1].values(), loc=4))

    def tp_legend(self, axes, fig, *args, **kwargs):
        Plot.tp_legend(self, axes, *args, **kwargs)
        self.comp_legend(axes, fig, *args, **kwargs)

    def zp_legend(self, axes, fig, *args, **kwargs):
        Plot.zp_legend(self, axes, *args, **kwargs)
        self.comp_legend(axes, fig, *args, **kwargs)

    def comp_legend(self, axes, fig, *args, **kwargs):
        """Place legend with model labels."""
        if isinstance(axes, (np.ndarray)):
            self.legend2D(axes)
            ax1 = axes.flatten()[-1]
        else:
            ax1 = axes
        plt.tight_layout()

        h, labels = ax1.get_legend_handles_labels()
        fig.legend(h, labels, loc=4)

    def legend2D(self, axes):
        """Legend for rows and columns (latitudes and longitudes) when using :func:`Plot.plot_columns`."""
        if not hasattr(axes, "__len__") or len(axes.flatten()) == 1:
            return
        for ax, lat in zip(axes[:,0], self.latitudes):
            ax.annotate("Latitude:\n %s"% lat,
                xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 10, 0), xycoords=ax.yaxis.label,
                textcoords='offset points', size='large', ha='right', va='center')
        for ax, lon in zip(axes[0], self.longitudes):
            ax.annotate("Longitude:\n %s"% lon,
                xy=(0.5, 1), xytext=(0, 5), xycoords='axes fraction',
                textcoords='offset points', size='large', ha='center', va='baseline')

    def plot_diff_spectra(self, mode=None, plots=None, compares=None, suffix=None, abs=False, figsize=(9,5), *args, **kwargs):
        """Plot spectra and their differences. See parameters of :func:`plot_spectra` and :func:`diff_spectra` for more information.

        Args:
            mode (str, optional): Among [transmission, emission, lightcurve, phasecurve]. Defaults to None (in which case the default spectrum is chosen).
            plots (list, optional) : List of ids (`label` parameter) of models to plot. see parameter `ids` of :func:`plot_spectra`.
            compares (list, optional) : List (`label` parameter) of differences of ids to plot. see parameter `ids` of :func:`diff_fluxes`.
            phase (ndarray, optional): List of phases to plot (in curve modes only) in degrees.
        """
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        err = self.plot_spectra(mode=mode, ids=plots, ax=ax[0], xlabel='', *args, **kwargs)
        if err:
            return 1
        err = self.diff_spectra(mode=mode, ids=compares, ax=ax[1], abs=abs, *args, **kwargs)
        if err:
            return 1
        ax[0].legend(loc="upper left", bbox_to_anchor=(1, 1.04), ncol=int(np.ceil(len(ax[0].lines)/7)))
        ax[1].legend(loc="lower left", bbox_to_anchor=(1, -0.06), ncol=int(np.ceil(len(ax[1].lines)/11)))
        if suffix is None:
            suffix=f"{mode}_{self.suffix}"
        self.save_plot("spectra_diff", suffix=suffix)

    def plot_diff_curves(self, mode="lightcurve", plots=None, compares=None, suffix=None, abs=False, figsize=(9,5), *args, **kwargs):
        """Plot light/phase-curves and their differences. See parameters of :func:`plot_curves` and :func:`diff_curves` for more information.

        Args:
            plots (list, optional) : List of ids (`label` parameter) of models to plot. see parameter `ids` of :func:`plot_spectra`.
            compares (list, optional) : List (`label` parameter) of differences of ids to plot. see parameter `ids` of :func:`diff_fluxes`.
            wl/wn (float, optional): Wavelength/wavenumber of the curve (can be a list).
        """
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        err = self.plot_curves(mode=mode, ids=plots, ax=ax[0], xlabel='', *args, **kwargs)
        if err:
            return 1
        err = self.diff_curves(mode=mode, ids=compares, ax=ax[1], abs=abs, *args, **kwargs)
        if err:
            return 1
        ax[0].legend(loc="upper left", bbox_to_anchor=(1, 1.04), ncol=int(np.ceil(len(ax[0].lines)/7)))
        ax[1].legend(loc="lower left", bbox_to_anchor=(1, -0.06), ncol=int(np.ceil(len(ax[1].lines)/11)))
        # plt.tight_layout()
        self.save_plot(f"{mode}s_diff", suffix=suffix)

    def plot_diff_lightcurves(self, *args, **kwargs):
        """See :func:`plot_diff_curves` for more information."""
        return self.plot_diff_curves(mode="lightcurve", *args, **kwargs)
    def plot_diff_phasecurves(self, *args, **kwargs):
        """See :func:`plot_diff_curves` for more information."""
        return self.plot_diff_curves(mode="phasecurve", *args, **kwargs)

    def plot_2d_fluxes_residuals(self, mode="lightcurve", ax=None, title="Lightcurve residuals", ids=None, ref=0, ppm=True, x_axis="wls", figsize=(5,3.5), savename="residuals_2d", colorbar_kwargs={}, **kwargs):
        """Plot curve residuals (select `mode` for light/phase-curve).
        See :func:`~pytmosph3r.plot.modelplot.CurvePlot.plot_curves` for more parameters.

        Args:
            mode (str, optional): Among [lightcurve, phasecurve]. Defaults to lightcurve.
            ids (list, optional) : List of ids (`label` parameter) of models to plot. For example ['1D', '2D', '3D'] if you created :code:`Plot(model, label='1D')`, etc.
            ref (int, optional): Index of the reference curve (plot as dashed). Defaults to None.
            savename (str, optional): Prefix for output filenames. Defaults to 'residuals_2d'.
        """
        if ids is None:
            ids = [[m.p_id, self.models[ref].p_id] for i, m in enumerate(self.models) if i != ref % len(self.models)]
        for i, comp in enumerate(ids):
            model0 = list(filter(lambda x: comp[0] == x.p_id, self.models))
            model1 = list(filter(lambda x: comp[1] == x.p_id, self.models))
            if len(model0) and len(model1):
                model0 = model0[0]
                model1 = model1[0]

                flux0 = model0.curve(mode)
                flux1 = model1.curve(mode)
                flux = flux0-flux1
                colorbar_kwargs['label'] = None
                if ppm:
                    flux *= 1e6
                    colorbar_kwargs['label'] = 'ppm'
                    if 'format' not in colorbar_kwargs:
                        colorbar_kwargs['format'] = '%.1f'
                else:
                    if 'format' not in colorbar_kwargs:
                        colorbar_kwargs['format'] = '%.3f'
                x = model0.get_spectral(w_units=x_axis, mode=mode)[0]
                y = np.degrees(model0.mode(mode).phases)
                err = CurvePlot.plot_2d_flux(self, mode=mode, ax=ax, title=title, figsize=figsize, x=x, y=y, flux=flux, x_axis=x_axis, savename=f"{savename}_{i}", colorbar_kwargs=colorbar_kwargs, **kwargs)

    def plot_2d_lightcurves_residuals(self, *args, **kwargs):
        """See :func:`plot_2d_fluxes_residuals`."""
        return self.plot_2d_fluxes_residuals(*args, **kwargs)
    def plot_2d_phasecurves_residuals(self, title='Phasecurve residuals', mode='phasecurve', *args, **kwargs):
        """See :func:`plot_2d_fluxes_residuals`."""
        return self.plot_2d_fluxes_residuals(mode=mode, title=title, *args, **kwargs)
