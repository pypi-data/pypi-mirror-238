import os

import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .comparison import Comparison
from .modelplot import Plot
from ..log import debugLogging, warningLogging
from ..util.util import query_yes_no

# some global matplotlib vars
mpl.rcParams['axes.labelsize'] = 11  # set the value globally
mpl.rcParams['axes.linewidth'] = 1  # set the value globally
mpl.rcParams['text.antialiased'] = True
mpl.rcParams['errorbar.capsize'] = 2
prop_cycle = plt.rcParams['axes.prop_cycle']
prop_colors = prop_cycle.by_key()['color']


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pytmosph3R-Plotter')
    parser.add_argument("-i", "--input", dest='input_files', nargs='+', type=str, required=True,
                        help="Input hdf5 file from pytmosph3r")
    parser.add_argument("-o", "--output-dir", dest="output_dir", type=str, required=True,
                        help="output directory to store plots")
    parser.add_argument("-a", "--all", dest="all", default=False, action='store_true',
                        help="Generate all (relevant) plots")
    parser.add_argument("-aa", "--absolutely-all", dest="all", const=2, action='store_const',
                        help="Plot absolutely everything (probably too much information!)")
    parser.add_argument("-x", "--plot-xprofile", dest="xprofile", default=False,
                        help="Plot molecular profiles", action='store_true')
    parser.add_argument("-aer", "--aerosols", dest="aprofile", default=False, help="Plot aerosol profiles",
                        action='store_true')
    parser.add_argument("-t", "--plot-tpprofile", dest="tpprofile", default=False,
                        help="Plot Temperature profiles", action='store_true')
    parser.add_argument("-z", "--plot-zpprofile", dest="zpprofile", default=False,
                        help="Plot Altitude-Pressure profiles", action='store_true')
    parser.add_argument("-d", "--plot-tau", dest="tau", default=False, help="Plot optical depth contribution",
                        action="store_true")
    parser.add_argument("-s", "--plot-spectrum", dest="spectrum", nargs='*', default=False,
                        help="Plot spectrum")
    parser.add_argument("-tr", "--transmittance", dest="transmittance", nargs='*', default=False,
                        help="Plot transmittance (optional: choose wavenumbers)")
    parser.add_argument("-e", "--emission", dest="emission", nargs='*', default=False,
                        help="Plot emission (optional: choose wavenumbers)")
    parser.add_argument("-L", "--lightcurve", dest="lightcurve", nargs='*', default=False,
                        help="Plot lightcurves (and select phases)")
    parser.add_argument("-P", "--phasecurve", dest="phasecurve", nargs='*', default=False,
                        help="Plot phasecurves (and select phases)")
    parser.add_argument("-wns", "--wavenumbers", dest="wns", nargs='*', default=None,
                        help="Wavenumbers to plot")
    parser.add_argument("-wls", "--wavelengths", dest="wls", nargs='*', default=None,
                        help="Wavelengths to plot")
    parser.add_argument("-sl", "--substellar-longitude", dest="substellar_longitude", default=None,
                        type=float, help="Define longitude of the substellar point.")
    parser.add_argument("-2D", "--plot-2D", dest="plot_2D", default=False,
                        help="Plot all 2D profiles (T, P, gases, aerosols)", action="store_true")
    parser.add_argument("-g", "--debug", dest='debug', default=False, action="store_true",
                        help="Force to stop on fail.")
    parser.add_argument("-int", "--interactive", dest="interactive", default=False, help="Interactive plot",
                        action='store_true')
    parser.add_argument("-c", "--compare", dest="compare", default=None, nargs='+',
                        help="Override the list of models to compare in spectra difference. By default, compares every model to the first.",
                        action='append')
    parser.add_argument("-neg", "--negative", dest="negative", default=True,
                        help="Turn off absolute value of spectra difference (to differentiate negative from positive differences).",
                        action='store_false')

    parser.add_argument("-T", "--title", dest="title", type=str, help="Title of plots")
    parser.add_argument("-sx", "--suffix", dest="suffix", type=str, help="File suffix for outputs")

    parser.add_argument("-alt", "--altitudes", dest='altitudes', nargs='+', type=str,
                        default=["surface", "top", "middle"], help="Altitudes to print")
    parser.add_argument("-lat", "--latitudes", dest='latitudes', nargs='+', type=str, default=["equator"],
                        help="Latitudes to print")
    parser.add_argument("-lon", "--longitudes", dest='longitudes', nargs='+', type=str,
                        default=["day", "terminator", "night"], help="Longitudes to print")
    parser.add_argument("-m", "--color-map", dest="cmap", type=str, default="Paired",
                        help="Matplotlib colormap to use")
    parser.add_argument("-l", "--labels", dest="labels", nargs='+', type=str, default=None,
                        help="Set model name for labels")
    parser.add_argument("-R", "--resolution", dest="resolution", type=float, default=None,
                        help="Resolution to bin spectra to")
    parser.add_argument("-rad", "--radius-factor", dest="r_factor", default=1., type=float,
                        help="Radius factor. Should be between 0 and 1 (to make atmosphere bigger).")
    parser.add_argument("-zmax", "--max-altitude", dest="zmax", default=np.inf, type=float,
                        help="Max altitude to plot. By default, max altitude of the model.")

    parser.add_argument("-r", "--rays", dest="plot_rays", default=False, help="Plot Rays",
                        action="store_true")
    parser.add_argument("-rr", "--rays-coords", dest="rays", default=False, help="Plot rays coordinates",
                        action='store_true')
    parser.add_argument("-nrp", "--no-rays-points", dest="points", default=True,
                        help="Plot intersection points", action='store_false')
    parser.add_argument("-rm", "--rays-midpoints", dest="mid_points", default=False,
                        help="Plot mid-subray points", action='store_true')

    args = parser.parse_args()

    warningLogging()
    if args.debug:
        debugLogging()

    wns = args.wns
    wls = args.wls

    plot_xprofile = args.xprofile or args.all
    plot_aprofile = args.aprofile or args.all
    plot_tp_profile = args.tpprofile or args.all
    plot_zp_profile = args.zpprofile or args.all
    plot_spectrum = args.spectrum or (
                not isinstance(args.spectrum, bool) and not len(args.spectrum)) or args.all
    transmittance = args.transmittance or (
                not isinstance(args.transmittance, bool) and not len(args.transmittance)) or args.all
    emission = args.emission or (not isinstance(args.emission, bool) and not len(args.emission)) or args.all
    phasecurve = args.phasecurve or (
                not isinstance(args.phasecurve, bool) and not len(args.phasecurve)) or args.all
    lightcurve = args.lightcurve or (
                not isinstance(args.lightcurve, bool) and not len(args.lightcurve)) or args.all
    plot_rays = args.plot_rays or (args.all == 2) or args.mid_points
    if not (
            plot_xprofile or plot_tp_profile or plot_zp_profile or plot_spectrum or transmittance or args.plot_2D or plot_rays):
        plot_spectrum = True  # if no plot, then plot spectrum

    print("Plotting %s" % args.input_files)
    if len(args.input_files) > 1:
        # Superimpose multiple plots
        plots = []
        labels = args.labels
        if args.labels is None:
            labels = args.input_files
        for idx, file in enumerate(args.input_files):
            if args.labels is None:
                labels[idx] = os.path.splitext(file)[0]
            plot = Plot(file, cmap=args.cmap, interactive=args.interactive,
                        title=args.title, suffix=args.suffix,
                        out_folder=args.output_dir,
                        zmax=args.zmax,
                        r_factor=args.r_factor,
                        substellar_longitude=args.substellar_longitude,
                        label=labels[idx])
            plot.altitudes = args.altitudes
            plot.longitudes = args.longitudes
            plot.latitudes = args.latitudes
            plots.append(plot)

        comparison = Comparison(plots, interactive=args.interactive, cmap=args.cmap,
                                title=args.title, suffix=args.suffix, out_folder=args.output_dir)
        comparison.altitudes = args.altitudes
        comparison.longitudes = args.longitudes
        comparison.latitudes = args.latitudes

        if plot_spectrum:
            comparison.plot_diff_spectra(resolution=args.resolution, compares=args.compare,
                                         abs=(not args.negative))
            comparison.plot_spectra(resolution=args.resolution)
            comparison.diff_spectra(resolution=args.resolution, ids=args.compare, abs=(not args.negative))
        if plot_xprofile:
            comparison.plot_xprofiles()
        if plot_tp_profile:
            comparison.plot_tps()
        if plot_zp_profile:
            comparison.plot_zps()
        if phasecurve:
            comparison.plot_diff_spectra(mode="phasecurve", phase=phasecurve, resolution=args.resolution,
                                         compares=args.compare, abs=(not args.negative))
            comparison.plot_phasecurves(wl=wls, wn=wns)
            comparison.plot_diff_phasecurves(wl=wls, wn=wns)
        if lightcurve:
            comparison.plot_diff_spectra(mode="lightcurve", phase=lightcurve, resolution=args.resolution,
                                         compares=args.compare, abs=(not args.negative))
            comparison.plot_lightcurves(wl=wls, wn=wns)
            comparison.plot_diff_lightcurves(wl=wls, wn=wns)
            comparison.plot_2d_lightcurves_residuals()

        return

    if not args.interactive:
        matplotlib.use('Agg')

    file = args.input_files[0]  # only one plot
    plot = Plot(file, cmap=args.cmap, interactive=args.interactive,
                title=args.title, suffix=args.suffix,
                out_folder=args.output_dir,
                zmax=args.zmax,
                r_factor=args.r_factor,
                substellar_longitude=args.substellar_longitude,
                )

    plot.altitudes = args.altitudes
    plot.longitudes = args.longitudes
    plot.latitudes = args.latitudes

    if plot_spectrum:
        plot.plot_spectrum(resolution=args.resolution)
    if transmittance:
        if wls is None and wns is None and not isinstance(transmittance, bool):
            wls = transmittance
        plot.transmittance_map(wl=wls, wn=wns)
    if emission:
        if wls is None and wns is None and not isinstance(emission, bool):
            wls = emission
        plot.emission_map(wl=wls, wn=wns)
    if phasecurve:
        plot.plot_spectrum(mode="phasecurve", phase=phasecurve, resolution=args.resolution)
        plot.plot_phasecurve(wl=wls, wn=wns)
        plot.plot_2d_phasecurve()
        if emission:
            plot.emission_map(wl=wls, wn=wns, mode="phasecurve")
    if lightcurve:
        plot.plot_lightcurve(wl=wls, wn=wns)
        plot.plot_spectrum(mode="lightcurve", phase=lightcurve, resolution=args.resolution)
        plot.plot_2d_lightcurve()
        if transmittance:
            if wls is None and wns is None and not isinstance(transmittance, bool):
                wls = transmittance
            if isinstance(lightcurve, (float, int, str)) or len(lightcurve) < 10 or query_yes_no(
                    "Number of phases is %s. Computing transmittance maps could take a while. Do you want to continue?" % len(
                            lightcurve)):
                plot.transmittance_map(wl=wls, wn=wns, phase=lightcurve,
                                       mode="lightcurve",
                                       save_name="transmittances/transmittance")
                plot.transmittance_animation(wl=wls, wn=wns, phase=lightcurve)
    if plot_xprofile:
        plot.plot_xprofiles()
    if plot_tp_profile:
        plot.plot_tps()
    if plot_zp_profile:
        plot.plot_zps()
    if args.plot_2D or plot_tp_profile or args.all:
        plot.t_maps()
    if args.plot_2D or plot_tp_profile or (args.all > 1):
        plot.t_maps(dim="longitude")
        plot.t_maps(dim="altitude")
    if args.plot_2D or plot_xprofile or args.all:
        plot.x_maps()
    if args.plot_2D or plot_xprofile or (args.all > 1):
        plot.x_maps(dim="longitude")
        plot.x_maps(dim="altitude")
    if args.plot_2D or plot_aprofile or args.all:
        plot.a_maps()
    if args.plot_2D or plot_aprofile or (args.all > 1):
        plot.a_maps(dim="longitude")
        plot.a_maps(dim="altitude")
    if plot_rays:
        plot.plot_rays(points=args.points, mid_points=args.mid_points, rays=args.rays)


if __name__ == "__main__":
    main()
