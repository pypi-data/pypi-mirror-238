import math as m
from typing import Tuple

import numpy as np
from ai import cs

from .grid import Grid
from pytmosph3r.log import Logger
from pytmosph3r.planetary_system import Observer
from pytmosph3r.util.util import timer


class RaysGrid(Grid):
    """Polar grid defining the number of rays on the terminator plane
        (plane going through the center of the planet and orthogonal to the rays).

    The grid has :py:attr:`n_radial` radial points located at the middle of the layers (see :py:attr:`z`),
        and :py:attr:`n_angular` angular points (see :py:attr:`angles`).
    """

    def __init__(self, n_radial=None, n_angular=None):
        self.n_radial = n_radial
        """Number of radial points in the grid. Equal to :attr:`~pytmosph3r.Model.n_layers` by default."""

        self.n_angular = n_angular
        """Number of angular points in the grid. Equal to 2* :attr:`~pytmosph3r.Model.n_latitudes` by default."""

        self.top_altitude = None
        """Top altitude to consider for the rays. Warning: does not represent the altitude of the highest ray, but the altitude of the maximum level of the grid. The rays are then passing through the middle of each layer."""

        self.dz = None
        """Distance between levels."""

        self.r = None
        """Impact parameters of the rays, i.e., their distance to the center of the planet. Note that they are passing through the middle of the layers of the grid."""

        self.angles = None
        """Azimuthal angles of the rays."""
        self.r_limits = None
        """Delimiting radii of each transmittance cell."""
        self.angles_limits = None
        """Delimiting angles of each transmittance cell."""

    @property
    def n_radial(self):
        return self._n_radial
    @n_radial.setter
    def n_radial(self, value):
        self._n_radial = int(value) if value else None
    @property
    def n_angular(self):
        return self._n_angular
    @n_angular.setter
    def n_angular(self, value):
        self._n_angular = int(value) if value else None

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the grid (:py:attr:`n_radial`,:py:attr:`n_angular`)."""
        return (self.n_radial, self.n_angular)

    def compute_radii(self):
        """Compute the altitudes (in `m`) over the grid by discretizing the space between the surface and :py:attr:`top_altitude` into :py:attr:`n_radial` intervals.
        The altitudes are then computed as the middle of these intervals.
        """

        z_levels = np.linspace(0, self.top_altitude, self.n_radial + 1)
        self.dz = np.diff(z_levels)
        self.r_limits = self.Rp + z_levels
        self.r = self.r_limits[:-1] + self.dz / 2.
        assert not np.isnan(self.r).any(), "NaN value in altitude"

    def compute_angles(self):
        """Compute the angles of the grid in `radians`."""

        self.angles = np.asarray([self.unit_angle * i for i in range(self.n_angular)])
        self.angles_limits = np.asarray([self.unit_angle * (i - 1 / 2) for i in range(self.n_angular + 1)])

    @property
    def unit_angle(self):
        """Angular length of one slice (in `radians`)."""

        return 2 * np.pi / self.n_angular


class Rays(Observer, RaysGrid):
    """Rays are orthogonal to the terminator plane (going through the center of the planet) of which the direction is defined by :class:`Observer`.
    The discretization of the plane is handled by :class:`RaysGrid`.
    """

    def __init__(self, n_radial=None, n_angular=None, observer=None, grid=None):
        Logger.__init__(self, self.__class__.__name__)
        RaysGrid.__init__(self, n_radial, n_angular)

        if grid is not None:
            if self.n_radial is None and "n_radial" in grid:
                self.n_radial = grid["n_radial"]
            if self.n_angular is None and "n_angular" in grid:
                self.n_angular = grid["n_angular"]
            self.warning(f"'grid' parameter is deprecated. Use directly 'n_radial' and 'n_anguar'. Using (n_radial = {n_radial}, n_angular = {n_angular}).")


        self.observer = observer
        """Position of the observer."""
        if isinstance(observer, dict):
            self.observer = Observer(**observer)

        self.rays_lengths = None
        """Lengths of each subsegment of each ray, ordered by their coordinates."""

        self.rays_indices = None
        """Control if rays lengths will be stored as a 1D array (or 2D, which is the default behavior)."""

    @property
    def latitude(self):
        return self.observer.latitude
    @property
    def longitude(self):
        return self.observer.longitude
    @property
    def units(self):
        return self.observer.units
    @property
    def orbit(self):
        return self.observer.orbit
    # properties above useless?
    @property
    def cartesian_system(self):
        return self.observer.cartesian_system

    def build(self, model):
        """Initialize the class with data from other modules for later computations.
        """
        self.model = model
        self.observer = model.observer
        self.atmosphere = model.atmosphere
        self.Rp = model.planet.radius
        self.Rs = model.star.radius
        self.atm_radii = self.Rp + model.atmosphere.altitude_levels

        self.top_altitude = model.atmosphere.max_altitude if 'max_altitude' in model.atmosphere.__dict__ and model.atmosphere.max_altitude is not None else model.atmosphere.altitude.max()

        assert not m.isnan(self.top_altitude), "Top altitude is NaN"

        self.n_radial = self.n_radial if self.n_radial else model.n_vertical
        self.n_angular = self.n_angular if self.n_angular else model.atmosphere.n_latitudes * 2
        self.n_radial = int(self.n_radial)
        self.n_angular = int(self.n_angular)

        self.compute_radii()
        self.compute_angles()

    def init_subrays(self):
        """Initialize the data for the computation of subrays."""

        if self.rays_indices is not None:
            self.rays_lengths = []
        else:
            self.rays_lengths = np.full(
                self.shape + (sum((2 * (self.atmosphere.shape[0]),) + self.atmosphere.shape[1:]), 4), -1.0)

        if Logger.verbose > 1:
            if "points" not in self.__dict__:
                self.points = np.empty((self.shape), dtype=object)
            if "mid_points" not in self.__dict__:
                self.mid_points = np.empty((self.shape), dtype=object)

        self.n_subrays = 0
        """Total number of sub-segments of rays (for which we compute the length)."""

        self.n_opacity_coords = 0  # not a property because it depends on the method (per angle or not)
        """Total number of cells crossed by rays (inferior or equal to :attr:`n_subrays`). Length of :attr:`opacity_coords`."""

        self.opacity_coords = {}
        """Dictionary of coordinates (length :attr:`n_opacity_coords`) of cells for which to compute opacity."""

    @timer
    def compute_sub_rays(self, bounds=None):
        """Subdivision of the rays into smaller segments ('subrays') based on the atmospheric grid.
        Each subray is associated to coordinates and their lengths are stored in :py:attr:`rays_lengths`.
        The function iterates over :py:attr:`RaysGrid.angles` and computes :py:func:`compute_sub_rays_angle` for each of these angles.

        Args:
            bounds (tuple): Must be ((r_s,r_e), (a_s,a_e)), where r_s and r_e are the radial start and end points, and a_s and a_e the angular ones.

        Returns:
            :py:obj:`dict`: Coordinates in the atmospheric grid with at least one subray, which will be given to the opacity module (``Exo_k``).
        """

        iterations = range(self.n_angular)

        if bounds is not None:
            iterations = range(bounds[1][0], bounds[1][1] + 1)
        else:
            self.info("Computing sub-rays...")

        self.init_subrays()

        for self.angle_idx in iterations:
            rbounds = (0, self.n_radial)
            if bounds is not None:
                if bounds[1][0] == bounds[1][1]:
                    rbounds = bounds[0]
                elif self.angle_idx == bounds[1][0]:
                    rbounds = [bounds[0][0], self.n_radial]
                elif self.angle_idx == bounds[1][1]:
                    rbounds = [0, bounds[0][1]]
            self.compute_sub_rays_angle(rbounds)

        if bounds is None:
            self.info("Computation of sub-rays - DONE")

        self.n_opacity_coords = len(self.opacity_coords)

        return self.opacity_coords

    def compute_sub_rays_angles(self, angles):
        """Subdivision of rays for multiple angles."""

        self.init_subrays()  # sets opacity_coords to {}
        angles = np.atleast_1d(angles)

        for self.angle_idx in angles:
            self.compute_sub_rays_angle()

        return self.opacity_coords

    def compute_sub_rays_angle(self, bounds=None):
        """Subdivision of the rays at the angle :py:attr:`angle_idx`. WARNING: the parameter to this function is NOT the angle, but the :attr:`bounds` of radial points to consider.
        See :py:func:`compute_sub_rays`. If :attr:`opacity_coords` is not initialized, it creates one.

        Args:
            bounds (tuple): Must be (r_s,r_e), where r_s and r_e are the radial start and end points.
        """

        atm_layer_idx = 0

        if not hasattr(self, 'opacity_coords'):
            self.opacity_coords = {}

        iterations = range(self.n_radial)

        if bounds is not None:
            iterations = range(*bounds)

        for self.layer_idx in iterations:
            ray_radius = self.r[self.layer_idx]
            atm_layer_idx = int(self.atm_radii.searchsorted(ray_radius,
                                                            side='right'))  # Note: if atm.n_vertical == rays.n_radial, atm_layer_idx = self.layer_idx
            self.n_up_levels = self.atmosphere.n_levels - atm_layer_idx  # nb of upper levels to check

            # compute indices for each intersection type
            self.lat_idx = 2 * self.n_up_levels
            self.long_idx = self.lat_idx + 2 * len(
                self.atmosphere.grid.positive_latitudes)  # we will iterate over the positive latitudes only, and duplicate the information
            self.max_points = self.long_idx + int(self.atmosphere.grid.n_longitudes / 2)

            # coord_system points of one ray with atmospheric grid
            points = np.full((self.max_points, 4), np.nan)  # (dist, alt, lat, lon)

            self.add_ray_origin(ray_radius, self.angles[self.angle_idx])

            self.levels_intersection(points, atm_layer_idx)
            self.latitudes_intersection(points)
            self.longitudes_intersection(points)
            points = self.filter_out(points)

            if Logger.verbose > 1:
                self.points[self.layer_idx, self.angle_idx] = points  # save for plotting later

            subrays_coords = self.subrays_length(points, ray_radius)
            self.opacity_coords.update(subrays_coords)  # merging coordinates for opacity

            subrays_coords = np.array([(i[0][0], i[0][1], i[0][2], i[1]) for i in
                                       list(subrays_coords.items())])  # don't need a dictionary now

            # store lengths for optical depth (tau)
            if self.rays_indices is not None:
                self.rays_indices.append((self.layer_idx, self.angle_idx))
                self.rays_lengths.append(subrays_coords)
            else:
                try:
                    self.rays_lengths[self.layer_idx, self.angle_idx][:len(subrays_coords)] = subrays_coords
                except:
                    pass  # subrays_coords is empty
            self.n_subrays += len(subrays_coords)

        return self.opacity_coords

    def levels_intersection(self, points, atm_layer_idx):
        """Computes the intersection of a ray (of coordinates (radius, angle)) with atmospheric levels (spheres). Returns a list of points [dist, r, lat, lon]."""

        radii = self.atm_radii[atm_layer_idx:]
        n_up_levels = len(radii)

        assert n_up_levels == self.atmosphere.n_levels - atm_layer_idx
        assert 2 * n_up_levels == self.lat_idx

        dist, latitudes, longitudes = self.cartesian_system.solve_radius(radii)

        points[:2 * n_up_levels] = np.stack([dist, np.tile(radii, 2), latitudes, longitudes],
                                            axis=1)  # doubled because of symmetry

    def latitudes_intersection(self, points):
        dist, radii, latitudes, longitudes = self.cartesian_system.solve_latitude(
            self.atmosphere.grid.positive_latitudes)
        points[self.lat_idx:self.long_idx] = np.stack([dist, radii, latitudes, longitudes],
                                                      axis=1)  # doubled because of symmetry

    def longitudes_intersection(self, points):
        dist, radii, latitudes, longitudes = self.cartesian_system.solve_longitude(
            self.atmosphere.grid.half_longitudes)
        points[self.long_idx:] = np.stack([dist, radii, latitudes, longitudes], axis=1)

    def filter_out(self, points):
        """Filter out spheres that are larger than atmosphere and sort"""

        atm_idx = np.where((points[:, 1] <= self.atm_radii[-1])
                           # & (points[:, 1] > 0)
                           & (~np.isnan(points[:, 0]))
                           & (~np.isnan(points[:, 1])) & (~np.isnan(points[:, 2])) & (~np.isnan(points[:, 3]))
                           )

        try:
            points = np.unique(points[atm_idx], axis=0)
        except:
            # atm_idx = [] probably makes np.unique() fail
            points = points[atm_idx]

        sorted_points = sorted(points, key=lambda x: x[0])  # sort using distance to origin point

        return np.asarray(sorted_points)

    def subrays_length(self, points, ray_radius):
        """Find coordinates of subrays and compute their length.
        Stored their coordinates into a dictionary: {(altitude, latitude, longitude): True} to allow merging
         the coordinates shared with other rays.
        """

        subrays_coords = {}

        if len(points) < 1:  # no points
            return subrays_coords

        dist = np.diff(points[:, 0])

        x, y, z = cs.sp2cart(points[:, 1], points[:, 2], points[:, 3])

        mid_points_x = x[:-1] + np.diff(x) / 2
        mid_points_y = y[:-1] + np.diff(y) / 2
        mid_points_z = z[:-1] + np.diff(z) / 2
        radii, latitudes, longitudes = cs.cart2sp(mid_points_x, mid_points_y, mid_points_z)
        altitudes = radii - self.Rp

        alti_idx = list(map(self.atmosphere.index_altitude, altitudes))
        lati_idx = list(map(self.atmosphere.grid.index_latitude, latitudes))
        # lati_idx = self.atmosphere.grid.index_latitudes(latitudes) # vectorized?
        long_idx = list(map(self.atmosphere.grid.index_longitude, longitudes))
        mid_points = np.stack([dist, radii, latitudes, longitudes], axis=1)

        if Logger.verbose > 1:
            self.mid_points[self.layer_idx, self.angle_idx] = mid_points

        for i in range(len(points) - 1):
            if m.isnan(dist[i]) or m.isnan(alti_idx[i]) or m.isnan(lati_idx[i]) or m.isnan(long_idx[i]):
                self.error("NaN in coordinates & distance of subrays.")
            if (alti_idx[i], lati_idx[i], long_idx[i]) not in subrays_coords:
                subrays_coords[(alti_idx[i], lati_idx[i], long_idx[i])] = dist[i]
            else:
                subrays_coords[(alti_idx[i], lati_idx[i], long_idx[i])] += dist[i]

        coords_sum = np.sum(list(subrays_coords.values()))
        dist_sum = np.sum(dist)

        assert np.isclose(coords_sum,
                          dist_sum), "Probably skipped a point in measuring distances, lengths of each subray coordinates does not match distances between intersection points (total of %s vs %s)" % (
            coords_sum, dist_sum)

        return subrays_coords

    def outputs(self):
        outputs = ["n_opacity_coords", "n_subrays", "r", "angles", "r_limits"
, "angles_limits"]

        if Logger.verbose > 1:
            outputs += ["points", "mid_points"]

        return outputs

def init_rays(obj):
    """Returns a :class:`Rays` class with either a dictionary or a Rays object."""
    if obj is not None:
        if isinstance(obj, Rays):
            return obj # already a class
        return Rays(**obj)