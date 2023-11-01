import math as m
from typing import Optional, Tuple

import numba
import numpy as np
from ai import cs
from .math import roots, nround


@numba.njit(cache=True)
def cos_central_angle(lat0, lon0, lat1, lon1):
    """Returns cosine of central angle between two points (lat0, lon0) and (lat1, lon1)."""
    return (np.sin(lat0)*np.sin(lat1)
                    + np.cos(lat1) * np.cos(lat0)
                    * np.cos(lon0 - lon1))

@numba.njit(cache=True)
def intersection_circles(d, r1, r2):
    """Computes the intersection area of two circles or radii :attr:`r1` and :attr:`r2`,
    of which the centers are separated by a distance :attr:`d`."""
    if (d < r1 + r2):
        a = r1**2
        b = r2**2
        if (d <= np.abs(r2 - r1)):
            return np.pi * min(a, b)
        x = (a - b + d**2) / (2 * d)
        x2 = d-x
        return a * np.arccos(x / r1) + b * np.arccos(x2 / r2) - x * np.sqrt(a-x**2) - x2*np.sqrt(b-x2**2)
    return 0

@numba.njit(cache=True)
def integrate_circles_intersections(d, r1, r2, func, coeffs):
    """Integrate `func(x)` for x 
    
    Extracted from batman (Kreidberg 2015)

    Args:
        func (numba function): Function to calculate over x
        d (float): distance between two circle centers.
        r1 (float): radius of 1st circle
        r2 (float): radius of 2nd circle
    """
    step_factor = 1 # TODO what value?
    d = d/r1; r2 = r2/r1
    x0 = max(d - r2, 0.)
    x1 = min(d + r2, 1.0)
    if x0 >= 1.: return 0 #flux = 0 if the planet is not transiting
    elif x1 - x0 < 1.e-7: return 0 # pathological case	
    x = x0
    dx = step_factor*np.arccos(x)
    A_p = 0 # previous Area size
    delta = 0 # integral
    while x < x1:
        A_x = intersection_circles(d, x, r2)
        func_value = func(x - dx/2., coeffs) # limb darkening coeff
        delta += (A_x - A_p)*func_value
        dx = step_factor*np.arccos(x)
        x = x + dx
        A_p = A_x
    dx = x1 - x + dx
    x = x1
    A_x = intersection_circles(d, x, r2)
    func_value = func(x - dx/2., coeffs)
    delta += (A_x - A_p)*func_value
    return delta

@numba.njit(cache=True)
def dist(r1, a1, r2, a2):
    """Distance between two points."""
    return np.sqrt(r1**2 + r2**2 -2*r1*r2*np.cos(a1-a2))

@numba.njit(cache=True)
def angle_from_sides(r1, r2, r3):
    """Angle between r1 and r2 in a triangle. r3 is the opposite side."""
    a = nround((r3**2 - r1**2 - r2**2) / (-2*r1*r2), 6)
    return np.arccos(a)

@numba.njit(cache=True)
def circular_segment(rS, aS, Rs, r1, a1, r2, a2):
    """Computes the intersection area of a line (r1, a1) - (r2, a2),
    with a circle of radius Rs of which the center is (rS, aS)."""
    if rS == 0:
        a = a2-a1
    else:
        a1S = angle_from_sides(Rs, rS, r1)
        a2S = angle_from_sides(Rs, rS, r2)
        a0 = aS%(2*np.pi)
        a00 = (aS+np.pi)%(2*np.pi)
        if a1 < 0:
            a0 = (aS-a1)%(2*np.pi)+a1
        # a = angle between (r1, a1) - (rS, aS) - (r2, a2)
        if (a1 < a0 and a0 < a2) or (a1 < a00 and a00 < a2):
            a = a1S + a2S # aS between a1 and a2
        else:
            # a1 and a2 on the same side
            a = a1S - a2S
    a = min(a%(2*np.pi), 2*np.pi-a%(2*np.pi))
    return np.abs(Rs**2 * (a - np.sin(a)) / 2)

@numba.njit(cache=True)
def triangle_surface(r1, a1, r2, a2, r3, a3):
    """"Surface of a triangle using the coordinates of each vertex."""
    a = dist(r3, a3, r1, a1)
    b = dist(r3, a3, r2, a2)
    c = dist(r2, a2, r1, a1)
    s = (a+b+c)/2
    return np.sqrt(s*(s-a)*(s-b)*(s-c))

@numba.njit(cache=True)
def compute_surface_sector(r, a, a_r, r_a, rS, aS, Rs, n_angular):
    """Surface area of a sector delimited by (r, a) with the intersections points of with the radius r (angles a_r), and the intersections points with the angles a of the sector (radii r_a). There are two solutions (max) for each.

    Args:
        r (float): Radius of sector
        a (float, float): Delimiting angles of sector
        a_r (tuple): Intersections with r (2 solutions max)
        r_a (tuple): Intersections with a (2 angles, and 2 solutions max for each)
        rS (float): projected distance to star center
        aS (float): projected angle to star center
        Rs (float): star radius
        n_angular (float): Number of angles (simpler calculations if equal to 1)
    """

    if rS > r+Rs:
        return 0. # too far or no intersections

    if n_angular == 1:
        return intersection_circles(rS, r, Rs)
    # TODO check n_angular == 2

    Aa0_rr0  = 0  # triangle a_r[0], a_r[1], r_a[0][1]
    Aa0_rr1  = 0  # triangle a_r[1], r_a[0][1], r_a[0][0]
    Aa01_rr1 = 0 # triangle a_r[1], r_a[0][1], r_a[1][0]
    Ar1_r1   = 0   # triangle a_r[1], r_a[0][1], r_a[1][0]
    Ar       = 0   # circular segment (r, a_r[0,1])
    Aa0      = 0  # circular segment (Rs, a_r[0], r_a[0])
    Aa1      = 0  # circular segment (Rs, a_r[1], r_a[1])
    Aa01     = 0 # circular segment (Rs, r_a[0], r_a[1])

    # Check where we are intersecting the sector
    i_r = np.where(((a_r <= a[1]) & (a_r >= a[0]) | (a_r-2*np.pi <= a[1]) & (a_r-2*np.pi >= a[0]) ))
    i_a = np.where((r_a < r) & (r_a >= 0))
    i_a_above = np.where((r_a > r))

    if len(i_r[0]) == 0:
        # no intersect with r

        if len(i_a[0]) == 0:
            if (r_a[:,0]<0).all() and (r_a[:,1]>r).all():
                # the whole sector is covering the star
                assert r**2 * ((a[1]-a[0])/2) < intersection_circles(rS, Rs, r)
                return r**2 * ((a[1]-a[0])/2)
            # if ((r_a[0]<0)|(r_a[0]>r)|np.isnan(r_a[0])).all() and ((r_a[1]<0)|(r_a[1]>r)|np.isnan(r_a[1])).all():
            return 0 # whole sector out of star
            # assert (r_a > r).any(), "Report as a bug"
        elif i_a[0][0] == i_a[0][1]: # intersect with only one angle a_i
            r_i = r_a[i_a[0][0]]
            a_i = a[i_a[0][0]]
            assert (r_i < r).all(), "Report as a bug"
            # assert circular_segment(rS, aS, Rs, r_i[0], a_i, r_i[1], a_i) < intersection_circles(rS, Rs, r)

            res = circular_segment(rS, aS, Rs, r_i[0], a_i, r_i[1], a_i)
            return res
        elif i_a[0][0] != i_a[0][1]:
            # intersect with both angles a_i from "below"
            r_i = [r_a[i_a[0][0], i_a[1][0]], r_a[i_a[0][1], i_a[1][1]]]
            r_a[i_a[0][0]]
            a_i = a[i_a[0]]
            Aa01 = circular_segment(rS, aS, Rs, r_i[0], a_i[0], r_i[1], a_i[1])
            if (r_a < 0).any():
                A0 = triangle_surface(0, 0, r_i[0], a_i[0], r_i[1], a_i[1]) # we assume the star is bigger than the planet, hence 0,0
                return A0 + Aa01
            else:
                # intersect with both angles a_i from "above"
                Ar = circular_segment(0, 0, r, r, a[0], r, a[1])
                Aa0_r = triangle_surface(r, a[1], r, a[0], r_a[0][0], a[0])
                Aa1_r = triangle_surface(r, a[1], r_a[1][0], a[1], r_a[0][0], a[0])
                return Ar + Aa0_r + Aa1_r + Aa01
    elif len(np.unique(i_a[0])) == 1 and (r_a[i_a[0][0]] > 0).all():
        # intersect one angle a_i and r, from the "outside"
        A0 = triangle_surface(r, a[i_a[0][0]], r, a_r[i_r[0][0]], r_a[i_a[0][0], i_a[1][0]], a[i_a[0][0]])
        Ar   = circular_segment(0, 0, r, r, a_r[i_r[0][0]], r, a[i_a[0][0]])
        Aa0r = circular_segment(rS, aS, Rs, r, a_r[i_r[0][0]], r_a[i_a[0][0], i_a[1][0]], a[i_a[0][0]])
        return A0 + Ar + Aa0r
    elif len(i_r[0]) == 2 and len(i_a[0]) == 0:
        if (r_a>r).all():
            # intersect r from above
            return intersection_circles(rS, Rs, r)
        # intersect r from below
        Ar   = circular_segment(rS, aS, Rs, r, a_r[0], r, a_r[1])
        Aa0  = circular_segment(0, 0, r, r, min(a_r), r, min(a))
        Aa1  = circular_segment(0, 0, r, r, max(a_r), r, max(a))
        Ar0  = triangle_surface(0, 0, r, a_r[0], r, a_r[1])
        Aa0r = triangle_surface(0, 0, r, min(a_r), r, min(a))
        Aa1r = triangle_surface(0, 0, r, max(a_r), r, max(a))
        return Ar + Aa0+ Aa1+ Ar0+ Aa0r+ Aa1r
    elif len(i_r)==1 and len(np.unique(i_a[0])) == 1:
        # intersect one angle a_i and r, from the "inside"
        A0 = triangle_surface(0, 0, r, a_r[i_r[0][0]], r_a[i_a[0][0], i_a[1][0]], a[i_a[0][0]])
        Ar1 = triangle_surface(0, 0, r, a_r[i_r[0][0]], r, a[1-i_a[0][0]])
        Ar   = circular_segment(0, 0, r, r, a_r[i_r[0][0]], r, a[1-i_a[0][0]])
        Aa0r = circular_segment(rS, aS, Rs, r, a_r[i_r[0][0]], r_a[i_a[0][0], i_a[1][0]], a[i_a[0][0]])
        return A0 + Ar1 + Ar + Aa0r
    else:
        # TODO track if there are some bugs left
        a_r=[a_r[0],a_r[1]]
        if len(i_r) == 1 and len(i_a_above[0]):
            # restrict angle to sector
            a_r[1-i_r[0][0]] = a[i_a_above[0][0]]
            if i_a_above[0][0] != 1-i_r[0][0]:
                # restricted angle set to side with radius outside sector
                # (there should be only one)
                a_r = [a_r[1],a_r[0]]

        # restrict radii to sector
        r_a=[[r_a[0][0],r_a[0][1]], [r_a[1][0],r_a[1][1]]]
        r_a[0][0] = max(r_a[0][0], 0)
        r_a[1][0] = max(r_a[1][0], 0)
        r_a[0][1] = min(r_a[0][1], r)
        r_a[1][1] = min(r_a[1][1], r)

        Aa0_rr0  = triangle_surface(r, a_r[1], r, a_r[0],  r_a[0][1], a[0])
        Aa0_rr1  = triangle_surface(r, a_r[1], r_a[0][0], a[0], r_a[0][1], a[0])
        Aa01_rr1 = triangle_surface(r, a_r[1], r_a[0][0], a[0], r_a[1][1], a[1])
        Ar1_r1   = triangle_surface(r_a[1][0], a[1], r_a[0][0], a[0], r_a[1][1], a[1])

        A0   = Aa0_rr0 + Aa0_rr1 + Aa01_rr1 + Ar1_r1 # central area
        Ar   = circular_segment(0, 0, r, r, a_r[0], r, a_r[1])
        Aa0  = circular_segment(rS, aS, Rs, r, a_r[0], r_a[0][1], a[0])
        Aa1  = circular_segment(rS, aS, Rs, r, a_r[1], r_a[1][1], a[1])
        Aa01 = circular_segment(rS, aS, Rs, r_a[0][0], a[0], r_a[1][0], a[1])
        return A0 + Ar + Aa0 + Aa1 + Aa01


class PointCircle:
    """2D polar coordinates."""

    def __init__(self, radius: float, angle: float):
        self.radius: float = radius
        """Radius in meters."""

        self.angle: float = angle
        """Angle in radians."""

    @property
    def coords(self) -> Tuple[float, float]:
        return self.radius, self.angle


class PointSpherical:
    """3D spherical coordinates."""

    def __init__(self, radius: float, latitude: float, longitude: float):
        self.radius: float = radius
        """Radius, in meters."""

        self.latitude: float = latitude
        """Latitude in radian :math:`[ -\pi/2, +\pi/2]`"""

        self.longitude: float = longitude % (2 * np.pi)
        """Longitude in radian :math:`[0,2\pi[`"""

    @property
    def coords(self) -> Tuple[float, float, float]:
        return self.radius, self.latitude, self.longitude


class PointCartesian:
    """3D Cartesian coordinates."""

    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    @property
    def coords(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    @property
    def norm2(self)->float:
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    @property
    def norm(self)->float:
        return m.sqrt(self.norm2)

    def __sub__(self, other):
        return PointCartesian(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, other: float):
        return PointCartesian(other*self.x, other*self.y, other*self.z)

@numba.njit(cache=True)
def fast_solve_latitude(x, latitudes, z_ray, norm_ray, dir_latitude):
    for i in range(len(latitudes)):
        a = m.sin(latitudes[i])**2 - m.sin(dir_latitude)**2
        b = - 2 * m.sin(dir_latitude) * z_ray
        c = ((norm_ray * m.sin(latitudes[i]))**2 - z_ray**2)

        sol = roots(a,b,c)
        if len(sol) > 0:
            x[i] = sol[0]
        if len(sol) > 1:
            x[len(latitudes)+i] = sol[1]


class CoordinateSystem:
    """Computes the intersection of a ray going through :py:attr:`ray_origin` following the direction :py:attr:`direction`.

    Args:
        direction (:class:`PointCartesian`): Direction (x,y,z) of the ray.
        ray_origin (:class:`PointCartesian`): Cartesian coordinates (x,y,z) of the ray intersection point with the terminator.
    """

    def __init__(self, direction: PointCartesian, ray_origin: Optional[PointCartesian] = None):
        self.direction: PointCartesian = direction
        self.ray_origin: Optional[PointCartesian] = ray_origin

    def radius(self, x):
        return np.sqrt(self.ray_origin.norm2 + x**2 )

    def latitude(self, x):
        with np.errstate(invalid='ignore'):
            return -np.arcsin((self.ray_origin.z + x * self.direction.z) /
                    self.radius(x))

    def longitude(self, x):
        with np.errstate(all='ignore'):
            longitude = np.arctan((self.ray_origin.y + x * self.direction.y) /
                        (self.ray_origin.x + x * self.direction.x) )
            # tan(x) is defined only between -pi/2 and pi/2, so here is a fix for our definition
            longitude[self.ray_origin.x + x * self.direction.x < 0] += np.pi
            numerator_sign = np.sign(self.ray_origin.y + x * self.direction.y)[self.ray_origin.x + x * self.direction.x == 0]
            longitude[self.ray_origin.x + x * self.direction.x == 0] = numerator_sign * np.pi/2
        return longitude

    def solve_radius(self, radii):
        with np.errstate(invalid='ignore'):
            x = np.sqrt(radii**2 - self.ray_origin.norm2 )
        x = np.concatenate([-x, x]) # doubled because of symmetry before and after the ray origin point
        return x, self.latitude(x), self.longitude(x)

    def solve_longitude(self, longitudes):
        x = ((self.ray_origin.y - self.ray_origin.x * np.tan(longitudes)) /
             (self.direction.x * np.tan(longitudes) - self.direction.y))
        if m.isclose(self.ray_origin.y, 0, abs_tol=1e-12) and m.isclose(self.direction.y, 0, abs_tol=1e-12):
            # special case when formula above is independent from longitudes
            x = np.full(longitudes.shape, np.nan)
        return x, self.radius(x), self.latitude(x), self.longitude(x)


class CartesianCoordinateSystem(CoordinateSystem):
    """Same as :class:`CoordinateSystem`, but initialize the system with a direction and an ray origin given in spherical and polar coordinates, respectively.
    """

    def __init__(self, latitude:float, longitude:float):
        self.spherical_direction = PointSpherical(1, latitude, longitude)

        x, y, z = cs.sp2cart(1, latitude, longitude)
        system_direction = PointCartesian(float(x),float(y),float(z))
        super().__init__(system_direction)

    def solve_latitude(self, latitudes):
        x = np.full(2*len(latitudes), np.nan)
        fast_solve_latitude(x, latitudes, self.ray_origin.z, self.ray_origin.norm, self.spherical_direction.latitude) # numba call
        return x, self.radius(x), self.latitude(x), self.longitude(x)

    @property
    def y_coeff(self):
        #  y**2 + b * y + c
        dir_lat = self.spherical_direction.latitude
        dir_lon = self.spherical_direction.longitude
        b = 2 * m.sin(dir_lat) * m.tan(dir_lon) * m.cos(self._point.angle)
        c = m.cos(self._point.angle)**2 * ((m.sin(dir_lat)**2 / m.cos(dir_lon)**2) + m.cos(dir_lat)**2) -1
        return [1, b, c]

    def coordinates(self, radius, angle):
        """Returns coordinates in Cartesian coordinate `system` of point at (`radius`, `angle`) """
        self._point = PointCircle(radius, angle)
        z = radius * m.cos(self.spherical_direction.latitude) * m.cos(angle)
        if m.isclose(self.spherical_direction.longitude, np.pi/2) or m.isclose(self.spherical_direction.longitude, 3*np.pi/2):
            y = -self.direction.z*z/self.direction.y
        else:
            y_sol = roots(*self.y_coeff) # two solutions
            y_r = y_sol[0]
            if angle > np.pi: # cos(angle)**2 == cos(-angle)**2
                y_r = y_sol[1]
            y = y_r * self._point.radius * m.cos(self.spherical_direction.longitude)
        if m.isclose(self.direction.x, 0, abs_tol=1e-12):
            with np.errstate(all='ignore'):
                x = np.sqrt(radius**2 - y**2 - z**2)
                if (angle < np.pi and self.direction.y > 0) or (angle > np.pi and self.direction.y < 0):
                    x = -x
            if np.isnan(x):
                x = 0 # handle rounding error that makes sqrt negative
        else:
            x = (- (y * self.direction.y) - ( z * self.direction.z )) / self.direction.x
        return PointCartesian(x, y, z) #, PointCartesian(x, y[1], z)

    def add_ray_origin(self, radius, angle):
        self.ray_origin = self.coordinates(radius, angle)
        try:
            assert m.isclose(self.ray_origin.norm, radius)
        except:
            raise ArithmeticError("Radius (%s) doesn't match norm of ray origin point (%s). Check the formulas or report as a bug!"%(radius, self.ray_origin.norm))


class CircleIntersection:
    """Class to compute the intersection of the cells of the transmittance grid with the star disk.

    Args:
        star (:class:`~pytmosph3r.star.Star`) : Star (including coordinates and size)
        sma (float) : Distance (in :math:`m`) between the star and the planet.
        inclination (float) : Orbit inclination (in degrees).
        rays (:class:`~pytmosph3r.rays.Rays`) : Transmittance grid (including the number of radial and angular rays).
    """
    def __init__(self, star, orbit=None, rays=None):
        self.model = None
        self.star = star
        self._sma = None
        self._inclination = None
        self._orbit = None
        self.orbit = orbit
        self.rays = rays
        """Transmittance grid."""
        self.radial_inter = np.zeros((self.rays.n_radial, 2))
        """Intersections with each radius (2 solutions each, max)."""
        self.angular_inter = np.zeros((self.rays.n_angular, 2))
        """Intersections with each angle (2 solutions each, max)."""

    @property
    def orbit(self):
        if self._orbit is None and self.model is not None:
            self._orbit = self.model.orbit
        return self._orbit
    @orbit.setter
    def orbit(self, value):
        self._orbit = value
    @property
    def sma(self):
        """Distance between planet and star."""
        if self._sma is None and self.orbit is not None:
            self._sma = self.orbit.r()
        return self._sma
    @sma.setter
    def sma(self, value):
        self._sma = value
    @property
    def inclination(self):
        """Inclination of the orbit."""
        if self._inclination is None and self.orbit is not None:
            self._inclination = self.orbit.inclination
        return self._inclination
    @inclination.setter
    def inclination(self, value):
        self._inclination = value

    @property
    def rays(self):
        """Automatize fetching of rays from transmission / building if necessary."""
        if (self._rays is None and self.model and
            self.model.transmission and self.model.transmission.rays):
            self._rays = self.model.transmission.rays
        try:
            assert self._rays.r is not None
        except:
            try:
                self._rays.build(self.model)
            except:
                pass # we'll try later on, don't you worry
        return self._rays
    @rays.setter
    def rays(self, value):
        self._rays = value
    
    def dist(self, phase=None):
        """Computes distance of each cell of the transmittance to the star center.
        Does not recompute if phase is not provided (save computation time).

        Args:
            phase (float, optional): Phase in radians. Defaults to None.

        Returns:
            array: Distance of transmittance cells to star center
        """
        if phase is not None:
            rS, aS = self.orbit.star_coordinates_projected(phase)
            self._dist = dist(self.rays.r[:, None], self.rays.angles, rS, aS)
        return self._dist

    def intersections(self, phase, star=None, sma=None, rays=None):
        """Computes intersection surfaces between star and the grid of rays."""
        if star is not None:
            self.star = star
        if sma is not None:
            self.sma = sma
        if rays is not None:
            self.rays = rays
        """Returns surface intersection of each transmittance cell with the star disk."""
        self.rays.observer.position_from_phase(phase, orbit=self.orbit)
        self.rS, self.aS = self.orbit.star_coordinates_projected(phase)
        self.compute_intersections_points()
        return self.compute_intersections_surfaces()

    def compute_intersections_points(self):
        """Compute intersection points of the star with all radii and angles of the transmittance grid.
        """
        # Get intersections with radii
        r = self.rays.r_limits
        Rs = self.star.radius
        a_r = angle_from_sides(r, self.rS, Rs)
        self.radial_inter = np.stack([self.aS+a_r, self.aS-a_r]).T % (2*np.pi)

        # Get intersections with angles
        b = -2*self.rS*np.cos(self.rays.angles_limits - self.aS)
        c = self.rS**2 - Rs**2
        angular_inter = []
        for b_i in b:
            sol = roots(1, b_i, c)
            if len(sol) < 1:
                sol = [np.nan]
            if len(sol) < 2:
                sol[1] = sol[0]
            angular_inter += [sol]
        self.angular_inter = np.asarray(angular_inter)
        assert (np.isclose(dist(self.rays.r_limits[:,None], self.radial_inter, self.rS, self.aS), Rs)|np.isnan(self.radial_inter)).all(), f"Bug: Rs = {Rs}."
        return

    def compute_intersections_surfaces(self):
        Rs = self.star.radius
        dist_bounds = dist(self.rays.r_limits[:,None], self.rays.angles_limits, self.rS, self.aS)
        # coords = np.where(dist_bounds < Rs)
        # for now, calculate everything (we can try to be smart later)
        coords = np.where(dist_bounds >= 0)

        self.surfaces_sector = np.zeros((self.rays.n_radial+1, self.rays.n_angular))
        self.surfaces = np.zeros(self.rays.shape)

        for c in np.array(coords).T:
            # compute for all neighbors to that point
            if ((c[0] > self.rays.n_radial) or (c[1] > self.rays.n_angular-1)
                or (c[0] < 0) or (c[1] < 0) or self.surfaces_sector[tuple(c)]) :
                continue # outside of bounds or already computed (not zero)
            self.surfaces_sector[tuple(c)] = \
                compute_surface_sector(r = self.rays.r_limits[c[0]],
                                        a = self.rays.angles_limits[c[1] : c[1]+2],
                                        a_r = self.radial_inter[c[0]], # TODO check order
                                        r_a = np.asarray(self.angular_inter[c[1] : c[1]+2]),
                                        rS=self.rS, aS=self.aS,
                                        Rs = self.star.radius,
                                        n_angular=self.rays.n_angular)
            assert not np.isnan(self.surfaces_sector[tuple(c)])

        self.surfaces = np.diff(self.surfaces_sector, axis=0)
        # np.array([intersection_circles(self.rS, r, Rs) for r in self.rays.r_limits])
        # from ..plot.plotutils import plot_sector_star
        # plot_sector_star(self.rS, self.aS, Rs, self.rays.r_limits[-1], self.rays.angles_limits)
        return self.surfaces


