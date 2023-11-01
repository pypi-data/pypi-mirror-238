from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib as mpl
import matplotlib.pylab as pl
from ai import cs
from matplotlib import ticker
from matplotlib.transforms import Affine2D

from .plotutils import *

from ..interface.hdf5 import HDF5Input
from ..util.util import *

if TYPE_CHECKING:
    from ..model import Model

class ModelPlot(BasePlot):
    """Intermediary class that can be inherited from by classes from pytmosph3r, to make plots from them directly."""

    def plot_rays(self, points=True, mid_points=False, rays=False, rays_bottom=False, rays_top=True,
                  rays_terminator=True, figsize=None, mode="transmission"):
        """Plot rays with matplotlib.

        Args:
            rays_bottom (bool, optional): Display the bottom layer (surface) of the planet. Defaults to False.
            rays_top (bool, optional): Display the top layer of the planet. Defaults to False.
            rays_terminator (bool, optional): Display the terminator plane. Defaults to False.
        """

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        lat, lon = np.meshgrid(self.grid.mid_latitudes, self.grid.all_longitudes)

        if rays_bottom:
            points_b = cs.sp2cart(self.R, lat, lon)
            s = ax.plot_surface(points_b[0], points_b[1], points_b[2], label="surface", alpha=.3)
            s._facecolors2d = s._facecolors3d
            s._edgecolors2d = s._edgecolors3d

        if rays_top:
            points_t = cs.sp2cart(self.r.max(), lat, lon)
            s = ax.plot_wireframe(points_t[0], points_t[1], points_t[2], label="top", alpha=.4)

        if rays_terminator:
            # terminator plane
            scale = 1
            num = 2
            A = self.rays(mode).cartesian_system.direction.x
            B = self.rays(mode).cartesian_system.direction.y
            C = self.rays(mode).cartesian_system.direction.z
            if C != 0:
                x = np.linspace(-self.R * scale, self.R * scale, num)
                y = np.linspace(-self.R * scale, self.R * scale, num)
                X, Y = np.meshgrid(x, y)
                Z = -(A * X + B * Y) / C
            elif B != 0:
                x = np.linspace(-self.R * scale, self.R * scale, num)
                z = np.linspace(-self.R * scale, self.R * scale, num)
                X, Z = np.meshgrid(x, z)
                Y = -(A * X + C * Z) / B
            else:
                y = np.linspace(-self.R * scale, self.R * scale, num)
                z = np.linspace(-self.R * scale, self.R * scale, num)
                Y, Z = np.meshgrid(y, z)
                X = -(C * Z + B * Y) / A
            s = ax.plot_surface(X, Y, Z, label="terminator", alpha=.5)
            s._facecolors2d = s._facecolors3d
            s._edgecolors2d = s._edgecolors3d

        try:
            if points:
                self.plot_points(ax, self.rays(mode).points)
            if mid_points:
                self.plot_points(ax, self.rays(mode).mid_points)
        except:
            self.debug("No points in output file. Try running pytmosph3r with -v")
        if rays:
            raise NotImplementedError

        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()

        self.save_plot("rays")

    def plot_points(self, ax, points,mode=None):
        if isinstance(points, (dict,)):
            iterator = points.items()
        elif isinstance(points, (list,)):
            iterator = enumerate(points)
            if isinstance(points[0], (list,)):
                for p_angle in points:
                    for p_radius in p_angle:
                        self.plot_points_ray(ax, p_radius)
                return
        elif isinstance(points, (np.ndarray,)):
            if mode is None:
                raise ValueError('`mode` should be set.')
            iterator = enumerate([points[radius, angle] for radius, angle in self.rays(mode).walk()])

        for i, ray in iterator:
            self.plot_points_ray(ax, ray)

    def plot_points_ray(self, ax, ray):
        if len(ray) < 1:  # no points
            return

        if isinstance(ray, dict):
            points = cs.sp2cart(ray["radius"] / self.h_unit + self.R, ray["latitude"], ray["longitude"])
        else:
            points = cs.sp2cart(ray[:, 1] / self.h_unit, ray[:, 2], ray[:, 3])

        ax.plot(points[0], points[1], points[2])

    def plot_2Dmap(self, ax, location, dim, x, y, z, p_levels=None, cmap="YlOrRd",
                   log=False, vmin=None, imshow=False, figsize=(5, 3.5), *args, **kwargs):
        """Plot a 2D map at a specific location and dimension (core function). Called by :func:`map_2D`.

        Args:
            location (str, int): Name ("equator", ...) or index of location to plot
            dim (str, int): Dimension of location (altitude/latitude/longitude)
            x (ndarray): Meshgrid
            y (ndarray): Meshgrid
            z (ndarray): Values to plot
            p_levels (list, optional): Pressure levels to plot over the map. Defaults to [1e-4, 1, 100, 10**4].
            cmap (str, optional): Colormap to be used. Defaults to "YlOrRd".
            log (bool): Log scale for colors. Defaults to False.
            vmin (float): Minimum value for colorbar.
            vmax (float): Maximum value for colorbar.
            imshow (bool): If True, the map will use plt.imshow() instead of plt.contourf(). imshow() shows exactly the temperature map used, while contourf() makes it smoother. Defaults to False (i.e., contourf).
        """

        if p_levels is None:
            p_levels = [1e-4, 1, 100, 10 ** 4]

        hz = get_2D(z, location, dim)

        if isinstance(hz, (float, str)):
            hz = np.full((len(x), len(y)), hz)

        if hz.ndim < 2 or 1 in hz.shape:
            # check which dim is 0D
            dim_0D = hz.shape.index(1)
            aspect = "1"
            if dim_0D:
                aspect = ".1"
            
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            cs = ax.imshow(hz, aspect=aspect, cmap=cmap, vmin=vmin,
                           *args, **kwargs)
            plt.colorbar(cs)
            ax.set_yticklabels(['%.2f' % i for i in y[0].tolist()])
            
            if not dim_0D:
                ax.set_xticklabels(['%g' % i for i in x[0].tolist()])
    
            if dim == "latitude":
                ax.set_xlabel('East Longitude')
                ax.set_ylabel('Altitude (Mm)')
            elif dim == "longitude":
                ax.set_xlabel('Latitude')
                ax.set_ylabel('Altitude (Mm)')
            elif dim == "altitude":
                ax.set_xlabel('East Longitude')
                ax.set_ylabel('Latitude')
            return ax

        if dim != "longitude":
            hz = np.concatenate((hz, hz[:, 0:1]), axis=1)

        if dim != "altitude":
            if p_levels is not None:
                zp = get_2D(self.pressure, location, dim)

                if dim == "latitude":
                    zp = np.concatenate((zp, zp[:, 0:1]), axis=1)
                ax.contour(x, y, zp, colors="black", linewidths=.2,
                           locator=ticker.FixedLocator(p_levels), )

        locator = ticker.LinearLocator(100)
        formatter = None
        extend = 'neither'

        if log:
            locator = ticker.LogLocator(base=1.01, subs=(1.0,), numticks=100)
            formatter = ticker.LogFormatter(1.01, labelOnlyBase=False)

        if vmin:
            hz[np.where(hz < vmin)] = vmin
            extend = 'min'
        
        if imshow:
            cs = ax.imshow(hz, extent=[x.min(), x.max(), y.min(), y.max()], cmap=cmap, vmin=vmin, *args,
                           **kwargs)
        else:
            cs = ax.contourf(x, y, hz, cmap=cmap, vmin=vmin, locator=locator, extend=extend, *args, **kwargs)

        plt.colorbar(cs, format=formatter, pad=0.08)

        return None

    def plot_2D(self, func, dim=None, altitudes=None, latitudes=None, longitudes=None, *args, **kwargs):
        """Calls :attr:`func` on all `locations` of :attr:`dim` for a 2D plot. Can also select altitudes, latitudes and longitudes separately."""

        if altitudes is not None:
            loop = altitudes
            dim = "altitude"
        elif latitudes is not None:
            loop = latitudes
            dim = "latitude"
        elif longitudes is not None:
            loop = longitudes
            dim = "longitude"
        elif dim == "altitude":
            loop = self.altitudes
        elif dim == "latitude":
            loop = self.latitudes
        elif dim == "longitude":
            loop = self.longitudes
        else:
            warnings.warn(
                "Dimension '%s' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. Not plotting 2D." % dim)
            loop = []

        if isinstance(loop, (float, int)):
            loop = [loop]

        for location in loop:
            func(location=location, dim=dim, *args, **kwargs)

    def map_2D(self, array, location="equator", dim="latitude", ax=None, figsize=(5, 3.5), *args, **kwargs):
        """Generic 2D map plot for a specific dimension & location. Selects the data to send to :func:`plot_2Dmap`."""

        fig = plt.figure(figsize=figsize)
        vertical = self.r  # by default, altitude is used as a vertical measure

        if dim == "altitude":
            ax = fig.add_subplot(111)
            longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1] + 2 * np.pi))
            x, y = np.degrees(np.meshgrid(longitudes, self.grid.mid_latitudes))
            ax.set_xlabel('East Longitude')
            ax.set_ylabel('Latitude')
        elif dim == "latitude":
            if self.grid.n_longitudes > 1:  # we will do a normal plot in plot_2Dmap
                ax = fig.add_subplot(111, projection='polar')
            longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1] + 2 * np.pi))
            x, y = np.meshgrid(longitudes, self.r)
            if self.r.ndim > 1:
                vertical = np.log10(self.pressure[:, 0,
                                    0])  # in Emission mode, we don't compute the altitude so we use the pressure as a vertical measure, supposed to be 1D
                x, y = np.meshgrid(longitudes, vertical)
                ax.set_rlim(bottom=vertical.max(), top=vertical.min())
        elif dim == "longitude":
            if self.grid.n_latitudes > 1:  # we will do a normal plot in plot_2Dmap
                ax = fig.add_subplot(111, projection='polar')
            x, y = np.meshgrid(self.grid.mid_latitudes, self.r)
            if self.r.ndim > 1:
                vertical = np.log10(self.pressure[:, 0,
                                    0])  # in Emission mode, we don't compute the altitude so we use the pressure as a vertical measure, supposed to be 1D
                x, y = np.meshgrid(self.grid.mid_latitudes, vertical)
                ax.set_rlim(bottom=vertical.max(), top=vertical.min())

        newax = self.plot_2Dmap(ax=ax, location=location, dim=dim, x=x, y=y, z=array, *args, **kwargs)

        if newax:
            ax = newax

        if dim == "longitude":
            if self.grid.mid_latitudes[0] != self.grid.mid_latitudes[-1]:
                ax.set_xlim(self.grid.mid_latitudes[0], self.grid.mid_latitudes[-1])
        elif dim == "latitude":
            try:
                ax.set_theta_zero_location("W")
                angles = [45 * theta for theta in range(0, 8)]
                ax.set_xticks(np.deg2rad(angles))
                ax.set_xticklabels([f'{theta}°' for theta in angles], fontsize=8)
            except:  # in case of 1x1 maps
                plt.tight_layout(pad=2)
        else:
            plt.tight_layout(pad=2)

        if dim != "altitude" and not newax:
            ax.grid(linewidth=.1)
            if self.r.ndim == 1:
                ax.set_rmin(0)

                ax.set_yticks([self.r.min(), self.r.max()])
                ax.set_yticklabels(
                    [f'{x:,.1f} Mm' for x in [self.z_levels[0], self.z_levels[-1]]], fontsize=6)
                ax.set_rgrids([self.r.min(), self.r.max()])
            else:
                p_levels = np.array([-4, 0, 2, 4.])
                p_levels = np.insert(p_levels, np.searchsorted(p_levels, vertical.max()), vertical.max())
                p_levels = np.insert(p_levels, np.searchsorted(p_levels, vertical.min()), vertical.min())
                p_levels = p_levels[np.where((p_levels >= vertical.min()) & (p_levels <= vertical.max()))][
                           ::-1]
                ax.set_rgrids(p_levels)
                ax.set_yticklabels(["{:,.1g}".format(x) + ' Pa' for x in np.power(10, p_levels)], fontsize=6)
            ax.set_rlabel_position(80)
            ax.tick_params(pad=0)

        return ax

    def t_map(self, location="equator", dim="latitude", ax=None, cmap="gnuplot2", *args, **kwargs):
        """Temperature 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""

        ax = self.map_2D(self.temperature, location=location, dim=dim, ax=ax, cmap=cmap, *args, **kwargs)
        index = get_index(self.grid, location, dim)
        dim_display = dim

        if self.vertical_in_pressure:
            dim_display = "pressure"

        ax.set_title("Temperature (K) at %s %s" % (dim_display, self.get_value_dim(index, dim)))

        self.save_plot("t_map_%s_%s" % (dim, index))

    def t_maps(self, dim="latitude", *args, **kwargs):
        """Temperature 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You can select altitudes, latitudes and longitudes using arguments (see :func:`plot_2D`) or by setting them beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"`,
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"` (default),
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """

        self.plot_2D(self.t_map, dim, *args, **kwargs)

    def x_map(self, gas=None, location="equator", dim="latitude", cmap="PuBuGn", ax=None, *args, **kwargs):
        """VMR 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""
        if gas not in self.gas_mix_ratio:
            self.error(f"Gas {gas} not in mix ratio.")
            return

        if isinstance(self.gas_mix_ratio[gas], str):
            total_vmr = sum([x for x in self.gas_mix_ratio.values() if not isinstance(x, str)])
            vmr = 1 - total_vmr * np.ones(self.shape)
        else:
            vmr = self.gas_mix_ratio[gas] * np.ones(self.shape)

        vmin = max(np.min(vmr), 1e-16)

        if vmin > 1e-16:
            vmin = None

        ax = self.map_2D(vmr, location=location, dim=dim, ax=ax, cmap=cmap, log=True, vmin=vmin, *args,
                         **kwargs)

        index = get_index(self.grid, location, dim)
        dim_display = dim

        if self.vertical_in_pressure:
            dim_display = "pressure"

        ax.set_title("[%s] at %s %s" % (gas, dim_display, self.get_value_dim(index, dim)))
        # self.zp_legend(ax, fig)

        os.makedirs(os.path.join(self.out_folder, gas), exist_ok=True)

        self.save_plot(os.path.join(gas, f"{gas}_map_{dim}_{index}"))

    def x_maps(self, gases=None, dim="latitude", *args, **kwargs):
        """Gas Volume Mixing ratio 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You should set beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"` (default),
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"`,
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """

        if gases is None:
            gases = self.gas_mix_ratio

        if isinstance(gases, str):
            gases = [gases]

        for gas in gases:
            self.plot_2D(self.x_map, gas=gas, dim=dim, *args, **kwargs)

    def a_map(self, aerosol=None, location="equator", dim="latitude", cmap="BuPu", ax=None, *args, **kwargs):
        """Aerosols MMRs 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""

        mmr = self.aerosols[aerosol]["mmr"] * np.ones(self.shape)
        vmin = max(np.min(mmr), 1e-16)

        if vmin > 1e-16:
            vmin = None

        ax = self.map_2D(mmr, location=location, dim=dim, ax=ax, cmap=cmap, log=True, vmin=vmin, *args,
                         **kwargs)

        index = get_index(self.grid, location, dim)
        dim_display = dim

        if self.vertical_in_pressure:
            dim_display = "pressure"

        ax.set_title("Aerosol MMR: log(%s) at %s %s" % (aerosol, dim_display, self.get_value_dim(index, dim)))
        # self.zp_legend(ax, fig)

        os.makedirs(os.path.join(self.out_folder, aerosol), exist_ok=True)

        self.save_plot(os.path.join(aerosol, "a_map"), "%s_%s" % (dim, index))

    def a_maps(self, aerosols=None, dim="latitude", *args, **kwargs):
        """Aerosols Mass Mixing ratio 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You should set beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"` (default),
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"`,
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """

        if aerosols is None:
            aerosols = self.aerosols

        if isinstance(aerosols, str):
            aerosols = [aerosols]

        for aerosol in aerosols:
            self.plot_2D(self.a_map, aerosol=aerosol, dim=dim, *args, **kwargs)

    def plot_xprofile(self, *args, **kwargs):
        return self.plot_x(*args, **kwargs)
    
    def plot_x(self, latitude=None, longitude=None, ax=None, title=None, figsize=(5, 3.5), *args, **kwargs):
        """Plot VMRs (gas mix profiles) of one vertical column."""
        fig, ax, save = self.figure(ax, figsize)
        
        if 'label' in kwargs:
            del kwargs['label'] # will be molecule names

        gas_legends = {}
        mol_idx = 0
        min_mix = 1
        max_mix = 0

        for mol_name, mix in self.gas_mix_ratio.items():
            if mix == 'background':
                others = list(self.gas_mix_ratio.values())
                others.remove('background')
                mix = 1 - np.sum(others)

            if isinstance(mix, (np.ndarray)):
                max_mix = max(max_mix, mix.max())
                min_mix = min(min_mix, mix.min())
            elif not isinstance(mix, (str)):
                max_mix = max(max_mix, mix)
                min_mix = min(min_mix, mix)

            color = self.x_colors[mol_name]

            self.plot_column(ax, mix, self.pressure, latitude=latitude, longitude=longitude, color=color, label=mol_name, *args, **kwargs)

            gas_legends[mol_name] = mpl.lines.Line2D([0], [0], color=color, label=mol_name)
            mol_idx += 1

        plt.yscale('log')
        plt.xscale('log')
        min_mix = max(min_mix, 1e-12)
        plt.xlim(min_mix, 1)

        if save:
            self.x_legend(ax=ax, fig=fig, title=title)
            self.save_plot(self.save_column('mixratio'))

        return gas_legends, min_mix, max_mix

    def x_legend(self, ax, fig, *args, **kwargs):
        if isinstance(ax, (np.ndarray)):
            self.legend2D(ax)
            ax0 = ax.flatten()[0]
            ax1 = ax.flatten()[-1]
        else:
            ax0 = ax
            ax1 = ax

        ax0.invert_yaxis()
        self.set_title(ax0, *args, **kwargs)

        plt.xlabel('Mixing ratio')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()

        h, labels = ax1.get_legend_handles_labels()

        fig.subplots_adjust(left=0.2, right=0.82, wspace=0.25, hspace=0.35)
        fig.legend(h, labels, loc='center right', bbox_to_anchor=(1, 0.5), ncol=1, prop={'size': 11},
                   frameon=False)

    def plot_xprofiles(self, *args, **kwargs):
        """Plot VMRs (gas mix profiles) of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""

        return self.plot_columns(self.plot_xprofile, name="mixratio", legend=self.x_legend, *args, **kwargs)

    def plot_tp(self, latitude=None, longitude=None, ax=None, title=None, figsize=(5, 3.5), *args, **kwargs):
        """Plot TP profile of one vertical column."""

        fig, ax, save = self.figure(ax, figsize)
        self.plot_column(ax, self.temperature, self.pressure, latitude=latitude, longitude=longitude, *args, **kwargs)
        plt.yscale('log')

        if save:
            self.tp_legend(ax=ax, title=title)
            self.save_plot(self.save_column("tp"))

    def tp_legend(self, ax, fig=None, *args, **kwargs):
        if isinstance(ax, (np.ndarray)):
            self.legend2D(ax)
            ax = ax.flatten()[0]

        ax.invert_yaxis()
        self.set_title(ax, *args, **kwargs)

        plt.xlabel('Temperature (K)')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()

        self.legend(ax)

    def plot_tps(self, *args, **kwargs):
        """Plot TP profiles of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""

        self.plot_columns(self.plot_tp, name="tp", legend=self.tp_legend, *args, **kwargs)

    def plot_zp(self, latitude=None, longitude=None, ax=None, title=None, figsize=(5, 3.5), *args, **kwargs):
        """Plot ZP profile of one vertical column."""
        fig, ax, save = self.figure(ax, figsize)

        self.plot_column(ax, self.pressure, self.z, latitude=latitude, longitude=longitude, *args, **kwargs)
        ax.set_xscale('log')

        if save:
            self.zp_legend(ax=ax, title=title)
            self.save_plot(self.save_column("zp"))

    def zp_legend(self, ax, fig=None, *args, **kwargs):
        if isinstance(ax, (np.ndarray)):
            self.legend2D(ax)
            ax = ax.flatten()[0]

        ax.invert_xaxis()
        self.set_title(ax, *args, **kwargs)

        plt.ylabel('Altitude ($10^6$m)')
        plt.xlabel('Pressure (Pa)')
        plt.tight_layout()

        self.legend(ax)

    def plot_zps(self, *args, **kwargs):
        """Plot ZP profiles of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""

        self.plot_columns(self.plot_zp, name="zp", legend=self.zp_legend, *args, **kwargs)

    def plot_spectrum(self, mode=None, noise=True, ax=None, save=False, time=None, phase=None, resolution=None, xlabel=None, ylabel=None, dashes=[], linewidth=.5, x_axis="wls", figsize=(5.3, 3.5), legend=True, xlog=True, ylog=False, color=None, label=None, title=None, time_units = None, *args, **kwargs):
        """Plot a spectrum.

        Args:
            mode (str) : transmission/emission/lightcurve/phasecurve/None. None takes the value of the spectrum in the main model (transmission by default), which can be noised. Defaults to None.
            noise (bool) : Plot noised spectrum. If it is set to a value, it overwrites the current noise using a normal distribution.
            t (ndarray, optional): List of times to plot (in curve modes only) in seconds (or astropy).
            resolution (int, optional): Number of points to bin to. Defaults to None.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            save = True
        
        suffix = None
        
        phase, time, label_prefix, time_units = self.init_time(phase, time, time_units)
            
        times = None
        phases = None
        try:
            if phase is not None or time is not None:
                phases = np.degrees(self.getattr(mode, "phases"))
                try:
                    if time is not None:
                        times = self.getattr(mode, "times")
                except Exception as e:
                    self.error(f"Did not compute times from phases. Maybe set self.model.orbit.period? Full error:\n{e}")
        except AttributeError:
            self.error(f"Mode {mode} has no 'phases' attribute. Maybe another mode?")
            return 1
        if phase is True and phases is not None:
            phase = phases
        elif phase is None:
            phase = [None]
            # INFO: Dirty fix to plot spectrum
            self.ph_index = 0
            phases = [np.NaN]
        if isinstance(phase, (float,int,str)):
            phase = [float(phase)]

        for ph in phase:
            try:
                spectrum = self.flux(mode, phase=ph, resolution=resolution, noise=noise, ax=ax, color=color)
                # computes also self.ph_index
                assert spectrum is not None
                assert not isinstance(spectrum, np.ndarray) # can be used for 2D plots, not spectrum
            except:
                self.error(f"plot_spectrum(): Mode '{mode}' has no 'spectrum' to plot (phase = {ph}). Maybe try another mode (lightcurve,emission,...).")
                # TODO: iterate over mode to try to find a good one if mode is None
                return 1

            # 'ph_index' is set in self.flux()
            if times is not None:
                time, units = time_fmt(times[self.ph_index], time_units)
                suffix = f"{time:.2f} {units}"
            else:
                suffix = f"{phases[self.ph_index]:.1f}°"
                
            if len(phase) > 1:
                p_label = f"{label} @ {suffix}"
                if label is None:
                    p_label = f"{label_prefix} = {suffix}"
            else:
                p_label = label
                if label is None:
                    p_label = self.label
                    
            ax.plot(getattr(spectrum, x_axis), spectrum.value, label=p_label, color=color, dashes=dashes, linewidth=linewidth, *args, **kwargs)

        if xlog:
            ax.set_xscale('log')
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        # ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%.1f'))
        if ylog:
            ax.set_yscale("log")
        if xlabel is None:
            xlabel=label_from_dim(x_axis)
        ax.set_xlabel(xlabel)
        if ylabel is None:
            ylabel = self.spectrum_label(mode)
        ax.set_ylabel(ylabel)
        
        if title is None:
            title = self.title
        if len(phase) < 2:
            p_title = title
            if title and suffix:
                p_title = f"{title} @ {suffix}"
            ax.set_title(p_title)
        if save:
            if legend:
                ax.legend()
            plt.tight_layout()
            output_name = "spectrum"
            if mode:
                output_name += "_" + mode
            self.save_plot(output_name)

    def transmission_spectrum(self, *args, **kwargs):
        """Calls :func:`plot_spectrum` with :attr:`mode` = 'transmission'."""

        return self.plot_spectrum(mode="transmission", *args, **kwargs)

    def emission_spectrum(self, *args, **kwargs):
        """Calls :func:`plot_spectrum` with :attr:`mode` = 'transmission'."""

        return self.plot_spectrum(mode="emission", *args, **kwargs)

    def transmittance_map(self, wl=None, wn=None, phase=None, mode="transmission", zmax=None, r_factor=None, ax=None, title="Transmittance at ", cmap="gnuplot", overlay=True, star_out=True, figsize=None, save_name="transmittances/transmittance", pcolormesh=False, core_color="black", *args, **kwargs):
        """Plot a map of the transmittance, as seen by the observer.

        Args:
            wl (float, optional): Select wavelength (or inferior). Defaults to None.
            wn (float, optional): Select wavenumber. Defaults to None.
            phase (float, optional): Select phase (in lightcurve mode). Defaults to None.
            mode (str, optional): transmission/lightcurve. Defaults to "transmission".
            zmax (float, optional): Truncate plot at altitude :attr:`zmax`, scaled using :attr:`h_unit`. Defaults to max altitude.
            r_factor (float, optional): Scale planet core radius (Rp). Can be used to enlarge (artificially) the atmosphere. Defaults to 1.
            cmap (str, optional): Colormap. Defaults to "gnuplot".
            overlay (bool, optional): Activates ticks and grid. Defaults to True.
            star_out (bool, optional): Hide part of the transmittance that is out of the star. Defaults to True.
            save_name (str, optional): Change name base of output file. Defaults to "transmittance".
            pcolormesh (bool, optional): Activates use of pcolormesh. Otherwise use contourf. Defaults to False.
        """
        if phase is True:
            try:
                mode="lightcurve"
                phase = np.degrees(self.mode(mode).phases)
            except:
                phase = 0
        if isinstance(phase, (np.ndarray, list)):
            for ph in np.float_(phase):
                self.transmittance_map(wl=wl, wn=wn, phase=ph, mode=mode, zmax=zmax, r_factor=r_factor, ax=ax, title=title, cmap=cmap, overlay=overlay, star_out=star_out, figsize=figsize, save_name=f"{save_name}_{ph:.3f}", pcolormesh=pcolormesh, *args, **kwargs)
            return
        if phase is not None:
            phase = np.radians(float(phase))
            mode = "lightcurve" # force lightcurve mode

        ws, wl, wn, w_units = self.init_spectral(wl, wn, default_wl=1, mode=mode)
        if zmax is None:
            zmax = self.zmax
        if r_factor is not None:
            self.r_factor = r_factor

        if hasattr(wl, '__len__'):
            if len(wl) > 1:
                fig = plt.figure(figsize=figsize)
                # iterate over wavelengths
                ncols = int((len(wl)+1)/2)
                nrows = int((len(wl)+1)/ncols)
                axes = []
                for i, wavelength in enumerate(wl):
                    ax = fig.add_subplot(nrows, ncols, i+1, polar=True)
                    axes.append(ax)
                    cs = self.transmittance_map(wl=float(wavelength), phase=phase, mode=mode, zmax=zmax, r_factor=r_factor, ax=ax, title="", cmap=cmap, overlay=overlay, star_out=star_out, figsize=figsize, save_name=save_name,  pcolormesh=pcolormesh, *args, **kwargs)
                fig.subplots_adjust(right=1)
                clipped_colorbar(cs, format='%.3f', ax=axes)
                self.save_plot(save_name)
                return cs
            wl = wl[0]

        save = False
        if ax is None:
            save = True

        try:
            tr = self.transmittance(phase, wl)
            assert tr is not None
        except Exception as e:
            self.warning(f"No transmittance to plot ('{mode}' mode). If you need it, set store_transmittance(s) to True (see parameters for each module). The exact error is:\n{e}")
            return
        try:
            if mode == "lightcurve" and phase is not None and star_out:
                # we need to re-calculate intersection of transmittance and star since we did NOT store it for every phase (too costly)
                self.mode(mode).transmittance_surfaces = False # for plots, cells are either ENTIRELY in front the star, or are not
                tr, dist = np.subtract(1, self.mode(mode).star_rays_opacity(phase, np.subtract(1, tr)))
        except Exception as e:
            self.warning("Failed to compute star 'shadow' over transmittance. Skipping and plotting transmittance as is.")


        r = self.rays(mode).r[::-1]/self.h_unit
        z = r  - self.Rp
        r = z + self.R # scaling: R = Rp * r_factor
        z_idx = np.where(z < zmax)
        z = z[z_idx]
        r = r[z_idx]
        tr = tr[::-1][z_idx]
        try:
            assert self.rays(mode).angles_limits[0]
        except:
            # rays were not properly written in h5 so we compute them again
            self.rays(mode).n_radial = tr.shape[0]
            self.rays(mode).n_angular = tr.shape[1]
            self.rays(mode).build(self.model)
        th = self.rays(mode).angles

        if ax is None:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot(111, projection='polar')
        repeats = int(np.ceil(180/len(th)))
        tr = np.repeat(tr, repeats, axis=1) # smoothing things
        th_0 = self.rays(mode).angles_limits[0]
        th = np.linspace(th_0, th_0+2*np.pi, tr.shape[1])
        x, y = np.meshgrid(th, r)


        if pcolormesh:
            cs = ax.pcolormesh(x, y, tr, cmap=cmap, vmin=0, vmax=1, *args, **kwargs)
        else:
            cs = ax.contourf(x, y, tr, cmap=cmap, levels=20, vmin=0, vmax=1, *args, **kwargs)

        if mode == "lightcurve" and phase is not None and star_out:
            try:
                Rs = self.model.star.radius/self.h_unit
                rS, aS = self.mode("lightcurve").star_projected_coordinates(phase)
                rS /= self.h_unit

                circle = pl.Circle((rS*np.sin(-aS), rS*np.cos(aS)), Rs, transform=(Affine2D().rotate(ax._theta_offset.get_matrix()[0, 2]) + ax.transProjectionAffine + ax.transAxes), color="black", alpha=0.3)
                ax.add_artist(circle)
            except:
                pass

        ax.set_theta_zero_location("N")
        ax.set_rmin(0)
        if np.isfinite(zmax):
            ax.set_rmax(self.R + zmax)
        ticks = [0, -1]
        if self.r_factor <1:
            ticks = [0, int(len(z)/2),-1]
        ax.set_rgrids(r[ticks])
        ax.set_yticklabels(["{:,.1f}".format(x) + ' Mm' for x in z[ticks[:-1]]]+["0"], fontsize=8)
        ax.grid(linewidth=1)
        if overlay:
            ax.set_xticklabels(["0°","45°","90°","135","180°","225°","270°","315°"], fontsize=9)
        else:
            ax.set_xticklabels([])
        ax.set_rlabel_position(0)
        
        core = pl.Circle((0, 0), self.R, transform=(Affine2D().rotate(ax._theta_offset.get_matrix()[0, 2]) + ax.transProjectionAffine + ax.transAxes), color=core_color, alpha=1)
        ax.add_artist(core)

        if overlay:
            ax.set_title(f"{title}{ws[self.w_index]:.2f} {units_from_dim(w_units)}", pad=15)
        plt.tight_layout(pad=1)
        if save:
            if overlay:
                fig.colorbar(cs, ticks=ticker.LinearLocator(11), format='%.1f', pad=.1)
            self.save_plot(save_name)
        return cs

    def transmittance_maps(self, wl=None, wn=None, save_name="transmittances/transmittance", *args, **kwargs):
        """Same parameters as :func:`transmittance_map` but create new files for each wl/wn."""
        if wl is not None:
            if isinstance(wl, (float, int) ):
                wl = [wl]
            for w in wl:
                self.transmittance_map(wl=w, save_name=f"{save_name}_{w:.3f}", *args, **kwargs)
        elif wn is not None:
            for w in wn:
                self.transmittance_map(wn=w, save_name=f"{save_name}_{w:.3f}", *args, **kwargs)
    
    def transmittance_animation(self, wl=None, wn=None, phase=None, filename=None, prefix="transmittances/transmittance", *args,
                                **kwargs):
        """Transforms maps generated by :func:`transmittance_map` to a GIF animation.
        """
        try:
            from wand.exceptions import WandError
            from wand.image import Image
        except ImportError as e:
            self.error(f"Wand or MagickWand not installed. Cannot GIFify. Full error:\n{e}")
            return

        if phase is None or phase is True:
            try:
                phase = np.degrees(self.mode("lightcurve").phases)
            except AttributeError:
                self.debug("transmittance_animation: 'lightcurve' mode has not been computed.")
                return

        if isinstance(phase, (float, int, str)):
            phase = [phase]
            
        suffix=self.suffix
        if wl is not None:
            prefix=f"{prefix}_{wl:.3f}"
            suffix=f"{suffix}_{wl:.3f}"
        if wn is not None:
            prefix=f"{prefix}_{wn:.3f}"
            suffix=f"{suffix}_{wn:.3f}"
    
        gif_output = Image()
        for i in phase:
            try:

                frame = Image(filename=f"{self.out_folder}/{prefix}_{i:.3f}_{self.suffix}.pdf")
                gif_output.sequence.append(frame)
            except:
                pass

        for i, frame in enumerate(gif_output.sequence):
            frame.delay = 20

        try:
            gif_output.type = 'optimize'
        except WandError as e:
            self.critical("No transmittance images found. Cannot generate GIF.")
            return

        if filename is None:
            filename = "%s/transmittances_%s.gif" % (self.out_folder, suffix)

        gif_output.save(filename=filename)
        print("Saved %s" % filename)

    def emission_map(self, wl=None, wn=None, mode="emission",
                     ax=None, title="Emission at ", cmap="gnuplot",
                     overlay=True, figsize=(5, 3.5),
                     *args, **kwargs):
        """Plot emission at a specific wavelength :attr:`wl` (or closest inferior wavelength, in micrometer) or wavenumber.
        """
        ws, wl, wn, w_units = self.init_spectral(wl, wn, default_wl=1, mode=mode)

        if hasattr(wn, '__len__'):
            if len(wn) > 1:
                fig = plt.figure(figsize=figsize)
                # iterate over wavelengths
                nrows = int((len(wn) + 1) / 2)
                ncols = int((len(wn) + 1) / nrows)
                axes = []
                try:
                    i = self.find_spectral(wl, wn)
                    # i = nmin(self.wns.searchsorted(wn), len(self.wns) - 1)
                    vmin = self.mode(mode).raw_flux[..., i].min()
                    vmax = self.mode(mode).raw_flux[..., i].max()
                except:
                    self.warning(
                        "No raw emission flux to plot. If you need it, set 'store_raw_flux' to True.")
                    return
                for i, w in enumerate(wn):
                    ax = fig.add_subplot(nrows, ncols, i + 1)
                    axes.append(ax)
                    cs = self.emission_map(wn=float(w), ax=ax, title="", cmap=cmap, vmax=vmax, vmin=vmin,
                                           *args, **kwargs)
                fig.subplots_adjust(right=1)
                cbar = clipped_colorbar(cs, format='%.3f', ax=axes)
                cbar.ax.tick_params(labelsize=7)
                self.save_plot("emission")
                return
            wn = wn[0]

        save = False
        if ax is None:
            save = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        ax.set_xlabel('East Longitude')
        ax.set_ylabel('Latitude')

        try:
            w_index = self.find_spectral(wl, wn)
            flux = self.mode(mode).raw_flux[..., w_index]
            flux = np.concatenate([flux, flux[:, 0:1]], axis=1)
        except:
            self.warning("No raw emission flux to plot. If you need it, set 'store_raw_flux' to True.")
            return

        longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1] + 2 * np.pi))
        x, y = np.degrees(np.meshgrid(longitudes, self.grid.mid_latitudes))
        locator = ticker.LogLocator(base=1.01, subs=(1.0,), numticks=100)
        locator = ticker.LinearLocator(100)
        cs = ax.contourf(x, y, flux, locator=locator, *args, **kwargs)

        if overlay:
            ax.set_title(f"{title}{ws[w_index]:.3f} {units_from_dim(w_units)}", pad=15)
        plt.tight_layout(pad=1)
        if save:
            fig.colorbar(cs, format=ticker.LogFormatter(1.01, labelOnlyBase=False), pad=.1)
            self.save_plot("emission")
        return cs

    def plot_emission(self, *args, **kwargs):
        print("This function will not be supported in future releases. Please use emission_map() instead.")


class CurvePlot(BasePlot):
    """Plots for (light/phase)curves."""

    def plot_curve(self, mode="phasecurve", wl=None, wn=None, ax=None, 
                   label=None, title="Phasecurve",
                   x_axis: Literal["times","phases"]="times", 
                   xlabel=None, x_units=None, ylabel='Normalized flux',
                   legend=True, figsize=(5, 3.5), *args, **kwargs):
        """Plot a curve from a `mode` (phasecurve/lightcurve). Use either `wl` or `wn`, not both.

        Args:
            mode (str, optional): phasecurve of lightcurve. Defaults to "phasecurve".
            wl (float, optional): Wavelength of the curve (can be a list). Defaults to 15.
            wn (float, optional): Wavenumber of the curve (can be a list).
        """

        fig, ax, save = self.figure(ax, figsize)
        ws, wl, wn, w_units = self.init_spectral(wl, wn, mode=mode)
        x = self.get_spectral(w_units=w_units, mode=mode)[0]  # wls or wns
        suffix = ""
        if isinstance(wn, (float, int)):
            wn = [wn]

        try:
            x, xlabel_ = self.x_axis_curve(x_axis=x_axis, x_units=x_units, mode=mode)
            if xlabel is None: xlabel = xlabel_
        except Exception as e:
            self.info(f"plot_curve(): no {mode} mode to plot. Full error:\n{e}")
            return 1

        for w in wn:
            curve = self.curve(mode, wn=w)
            if self.substellar_longitude is not None:
                curve = curve[::-1] # why?

            # self.w_index comes from curve(), which calls find_spectral()
            suffix = f"{ws[self.w_index]:.1f} {units_from_dim(w_units)}"
            p_label = label
            if len(wn) > 1:
                p_label = f"{suffix}"
                if label:
                    p_label = f"{label} @ {suffix}"

            ax.plot(x, curve, label=p_label, *args, **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if legend and label is not None:
            ax.legend()

        if len(wn) < 2:
            p_title = f"{suffix}"
            if title and suffix:
                p_title = f"{title} @ {suffix}"
            ax.set_title(f"{p_title}")

        plt.tight_layout(pad=1)

        if save:
            self.save_plot(mode)

    def plot_phasecurve(self, *args, **kwargs):
        """See parameters of :func:`plot_curve`."""
        return self.plot_curve(mode="phasecurve", title="Phasecurve", *args, **kwargs)

    def plot_lightcurve(self, wl=1, *args, **kwargs):
        """See parameters of :func:`plot_curve`."""
        return self.plot_curve(mode="lightcurve", title="Lightcurve", wl=wl, *args, **kwargs)

    def plot_2d_flux(self, mode="phasecurve", ax=None, title='Normalized flux',
        figsize=(5, 3.5), x=None, y=None, flux=None, x_axis="wls", xlog=True,
        xlabel=None, ylabel='Phase angle (degrees)',
        cmap='viridis', colorbar_kwargs=dict(format='%.3f'), savename=None,
        *args, **kwargs):
        """2D phase curves (imshow), with the X axis the spectral dimension and the Y axis phases.

        Args:
            x_axis (str) : Choose X axis as "wls" or "wns", for wavelengths or wavenumbers, respectively.
            figsize (tuple, optional): Size of the figure. Defaults to (5,3.5).
            cmap (str, optional): Colormap to use in the imshow(). Defaults to "gnuplot".
        """

        fig, ax, save = self.figure(ax, figsize)

        if flux is None:
            try:
                flux = self.curve(mode)
            except:
                self.info("plot_curves(): no %s to plot." % mode)
                return 1
        if x is None:
            x = self.get_spectral(w_units=x_axis, mode=mode)[0]  # wls or wns
        if y is None:
            y = np.degrees(self.mode(mode).phases)

        if flux.max()==1:
            # plot a normalized flux
            levels=np.linspace(flux.min(), flux.max(), 8)
        else:
            # plot a difference
            l = [-200,-100,-50,-20,-5,0,5,20,50,100,200,700] # in ppm
            if flux.max()<1:
                l = np.array(l)/1e6 # not in ppm
            levels=np.array([flux.min(),*l,flux.max()])
            levels = levels[np.where((levels>=flux.min()) & (levels<=flux.max()))]
        colors = [mpl.cm.get_cmap(cmap)(i/len(levels)) for i in range(len(levels))]

        cmap = mpl.cm.get_cmap(cmap)
        norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        cs = ax.pcolormesh(x, y, flux, cmap=None, norm=norm, zorder=-9)
        ax.set_rasterization_zorder(-1)
        if xlabel is None:
            xlabel = label_from_dim(x_axis)
        if xlog:
            ax.set_xscale('log')
        else:
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        plt.tight_layout(pad=1)

        if save:
            fig.colorbar(cs, ticks=levels, spacing="uniform", **colorbar_kwargs)
            plt.tight_layout(pad=1)
            if savename is None:
                savename = mode + "s"
            self.save_plot(savename)
        return cs

    def plot_2d_phasecurve(self, *args, **kwargs):
        return self.plot_2d_flux(mode="phasecurve", *args, **kwargs)

    def plot_2d_lightcurve(self, *args, **kwargs):
        return self.plot_2d_flux(mode="lightcurve", *args, **kwargs)


class Plot(LoadPlot, ModelPlot, CurvePlot):
    """Plot class. Can plot a Model() or a HDF5 file generated by Pytmosph3R."""

    def __init__(self, model: Union[Model, str] = None,
                 title: Optional[str] = None, label: Optional[str] = None,
                 suffix=None, out_folder: str = '.', cmap: str = 'Paired',
                 r_factor=1., h_unit=1e6, zmax=np.inf, pmin=None, substellar_longitude=None,
                 vertical_in_pressure=None,
                 interactive=None, *args, **kwargs):
        """Parameters for the Plots:

        Args:
            model (string or :class:`~pytmosph3r.model.model.Model`) : HDF5 filename from which to read the model (if string), or Model after its computation.

            label (str) : Most useful when comparing multiple plots.

            suffix (str) : Suffix to append to plot filenames.

            out_folder (str) : Directory where we will generate the plots.

            r_factor (float) : Factor with which the planet radius will be scaled. (Below 1, the radius is smaller, so the atmosphere looks larger). Defaults to 1.

            zmax (float) : Maximum height to plot (can be used to crop the atmosphere), scaled via :attr:`h_units`. Defaults to infinity.

            h_unit (float) : Units of the heightscale. Defaults to 1E6 (= Mm).

            interactive (bool) : Activate/deactivate showing plots. Plot.interactive can also be changed for all Plot objects.
        """
        super().__init__(self.__class__.__name__, *args, **kwargs)

        self.h_unit = h_unit
        """Height unit scaling. By default 1e6, i.e., Mm."""

        self.zmax = zmax
        """Max altitude (in Mm) to plot."""

        self.r_factor = r_factor
        """Radius factor (for visual purposes). By default 1."""

        self._p_min = pmin
        """Min (top) pressure to plot."""

        self.vertical_in_pressure = vertical_in_pressure
        """Use pressure as vertical axis ."""

        self.substellar_longitude = substellar_longitude
        """Longitude of the substellar point (in degrees)."""
        if substellar_longitude is not None:
            self.substellar_longitude = float(substellar_longitude)

        self.f = None

        if isinstance(model, str):
            if os.path.splitext(model)[-1] != ".h5":
                try:
                    new_path = os.path.join(model, "output_pytmosph3r.h5")
                    if os.path.isfile(new_path):
                        model = new_path
                    else:
                        raise NameError
                except:
                    self.warning("Input file (%s) extension unrecognized. Not .h5?" % model)
            # self.f = h5py.File(model,'r')
            self.f = HDF5Input(model)
            self.filename = model
        else:
            self._model = model

        if interactive in (False, True):
            # user can set Plot.interactive to change all plots behavior, hence the 'None' by default.
            self.interactive = interactive

        if not self.interactive:
            mpl.use('Agg')
        self.title = title
        self.cmap = mpl.cm.get_cmap(cmap)
        self.suffix = suffix
        if self.suffix is None:
            self.suffix = "pytmosph3r"
        self.out_folder = out_folder
        self.ph_index = None

        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)

        if label is None:
            if isinstance(model, str):
                label = path_leaf(model)
            elif model is not None and 'filename' in model.__dict__ and model.filename:
                label = path_leaf(model.filename)
            else:
                label = "Pytmosph3R"
        self.label = label
        self.p_id = label

    def inputs(self):
        return ["pytmosph3r_h5", "title", "label", "suffix", "out_folder" "cmap", "r_factor", "h_unit",
                "zmax", "pmin", "substellar_longitude", "interactive", "model"]

    @property
    def idx_latitude(self):
        return get_latitude_index(self.latitude, self.n_latitudes)

    @property
    def idx_longitude(self):
        return get_longitude_index(self.longitude, self.n_longitudes)

