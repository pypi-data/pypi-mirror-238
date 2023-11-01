from typing import Optional, List, Tuple, Union

import numpy as np
from pytmosph3r.log.logger import Logger


class Grid(Logger):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    @property
    def shape(self) -> Tuple:
        raise NotImplementedError

    @property
    def ndim(self):
        return len(self.shape)

    def walk(self, dims=None):
        """Return iterator over multiple dimensions.

        Args: dims (:obj:`array`): List of dimensions to iterate over. By default, iterates over all
        dimensions (defined in the attribute `shape` of the current object.)
        """

        from itertools import product
        if dims is None:
            dims = range(len(self.shape))
        return product(*[range(self.shape[i]) for i in dims])


class Grid3D(Grid):
    """ Simple 3D grid based on a 2D longitude/latitude grid and an (abstract) vertical axis. You can
    overwrite the latitudes and longitudes of your grid points with the :attr:`mid_latitudes` and
    :attr:`mid_longitudes` parameters. Note that :attr:`latitudes` and :attr:`longitudes` are derived from
    these and return the boundaries of each cell of the grid.

    Args:
        n_vertical (int) : Number of vertical points in the grid.
        n_latitudes (int) : Number of latitudinal points in the grid.
        n_longitudes (int) : Number of longitudinal points in the grid.
    """

    def __init__(self, n_vertical: Optional[int] = None, n_latitudes: Optional[int] = None,
                 n_longitudes: Optional[int] = None,
                 mid_latitudes: Optional[np.ndarray] = None, mid_longitudes: Optional[np.ndarray] = None):

        super().__init__()

        self.n_vertical: Optional[int] = int(n_vertical) if n_vertical else None
        self.n_latitudes: Optional[int] = int(n_latitudes) if n_latitudes else None
        self.n_longitudes: Optional[int] = int(n_longitudes) if n_longitudes else None

        self._to_east: Optional[bool] = None  # going towards the east by default
        self._to_north: Optional[bool] = None  # going towards the south by default

        self._mid_latitudes = mid_latitudes
        self._mid_longitudes = mid_longitudes

        self._regular_latitudes = True
        """Assume latitudes are regularly spaced (poles are half-long)."""

        self._latitudes: Optional[np.ndarray] = None
        self._longitudes: Optional[np.ndarray] = None

        self._positive_latitudes: Optional[np.ndarray] = None

        self._latitude_angle: Optional[float] = None  # BUG: Should be an array
        self._longitude_angle: Optional[float] = None  # BUG: Should be an array

        self._half_longitudes: Optional[np.ndarray] = None
        self._all_longitudes: Optional[np.ndarray] = None

    @property
    def regular_latitudes(self):
        try:
            return self._regular_latitudes
        except:
            return True # assume regularly spaced by default, for speed
    @regular_latitudes.setter
    def regular_latitudes(self, value):
        self._regular_latitudes = value

    @property
    def to_east(self) -> bool:
        """True if longitude is in increasing order."""

        if self._to_east is None:
            self._to_east = (np.diff(self.mid_longitudes) > 0).all()

        return self._to_east

    @property
    def to_north(self) -> bool:
        """True if latitude is in increasing order."""

        if self._to_north is None:
            self._to_north = (np.diff(self.mid_latitudes) > 0).all()

        return self._to_north

    @property
    def shape(self) -> Tuple[int, int, int]:
        """Shape of arrays in this grid."""

        return self.n_vertical, self.n_latitudes, self.n_longitudes

    def index_colatitude(self, colatitude) -> int:
        """Returns index corresponding to an angle with the pole 0 (by convention, north)."""

        if colatitude < 0:
            return self.index_colatitude(-colatitude)
        elif colatitude < self.lat_angle / 2:
            return 0
        elif colatitude > self.lat_angle * (self.n_latitudes - 3 / 2):
            return self.n_latitudes - 1
        else:
            return int(colatitude / self.lat_angle + 1 / 2)

    def index_latitude(self, latitude) -> int:
        """Gives the index of the latitude interval containing a `latitude` (given in `radians`)."""
        if not self.regular_latitudes:
            # slower search but necessary for irregular grids
            return max(self.latitudes.searchsorted(latitude, "right")-1, 0)

        return self.index_colatitude(latitude + np.pi / 2)

    def latitude(self, i):
        """Boundary angles in `rad` of latitude box with index `i`."""

        if i == self.n_latitudes:
            return [self.latitudes[i], None]
        else:
            return [self.latitudes[i], self.latitudes[i + 1]]

    @property
    def latitudes(self) -> np.ndarray:
        """Latitudinal boundaries (deduced from :attr:`mid_latitudes`)."""

        if self._latitudes is None:
            self._latitudes = self.mid_latitudes[:-1] + np.diff(self.mid_latitudes) / 2
            if self.to_north:  # going up
                self._latitudes = np.insert(self._latitudes, 0, -np.pi / 2)
                self._latitudes = np.append(self._latitudes, np.pi / 2)
            else:  # going down
                self._latitudes = np.insert(self._latitudes, 0, np.pi / 2)
                self._latitudes = np.append(self._latitudes, -np.pi / 2)

        return self._latitudes

    @latitudes.setter
    def latitudes(self, value: np.ndarray):
        self._latitudes = value

        # let's check if latitudes are regularly spaced (for faster search)
        diff = np.diff(self._latitudes[1:-1]) # ignore poles
        self.regular_latitudes = np.all(np.isclose(diff, diff[0]))

    @property
    def positive_latitudes(self) -> np.ndarray:
        """Positive latitudinal boundaries (deduced from :attr:`mid_latitudes`)."""

        if self._positive_latitudes is None:
            self._positive_latitudes = self.latitudes[np.where(self.latitudes >= 0)]

        return self._positive_latitudes

    @property
    def mid_latitudes(self) -> np.ndarray:
        """Latitudes in the \"middle\" of each latitude box."""

        if self._mid_latitudes is None:
            if self.n_latitudes > 1:
                self._mid_latitudes = np.asarray(
                    [i * self.lat_angle - np.pi / 2 for i in range(0, self.n_latitudes)])
            else:
                self._mid_latitudes = np.asarray([0])  # equator if only one latitude

        return self._mid_latitudes

    @mid_latitudes.setter
    def mid_latitudes(self, value):
        """Overwrite latitudes in the middle of each box."""

        self._mid_latitudes = np.asarray(value)

        # force recomputations of other variables that depend on mid_latitudes
        self._to_north = None
        self._positive_latitudes = None
        self._latitudes = None

    @property
    def lat_angle(self):
        """Angle between two latitudes."""

        if self.n_latitudes > 1:
            self._latitude_angle = np.pi / (self.n_latitudes - 1)  # poles cover only half an angle
        else:
            self._latitude_angle = np.pi

        return self._latitude_angle

    def index_longitude(self, longitude) -> int:
        """Gives the index of the longitude interval containing a `longitude` (given in `radians`)."""

        if self.to_east:
            if longitude < self.all_longitudes[0]:
                return self.index_longitude(longitude + 2 * np.pi)
            elif longitude > self.all_longitudes[-1]:
                return self.index_longitude(longitude - 2 * np.pi)
            else:
                return int((longitude - self.all_longitudes[0]) / self.lon_angle) % self.n_longitudes
        else:
            if longitude < self.all_longitudes[-1]:
                return self.index_longitude(longitude + 2 * np.pi)
            elif longitude > self.all_longitudes[0]:
                return self.index_longitude(longitude - 2 * np.pi)
            else:
                return (self.n_longitudes - int((longitude - self.all_longitudes[0]) / self.lon_angle)) \
                       % self.n_longitudes

    def longitude(self, i):
        """Boundary angles in `rad` of longitude box with index `i`."""

        return [self.all_longitudes[i], self.all_longitudes[i + 1]]

    @property
    def longitudes(self) -> np.ndarray:
        """Longitudinal boundaries (unique). Deduced from :attr:`mid_longitudes`."""

        if self._longitudes is None:
            if self.to_east:  # going up
                last = self.mid_longitudes[0] + 2 * np.pi
            else:  # going down
                last = self.mid_longitudes[0] - 2 * np.pi
            self._longitudes = self.mid_longitudes - np.diff(
                np.concatenate([self.mid_longitudes, [last]])) / 2

        return self._longitudes

    @longitudes.setter
    def longitudes(self, value: np.ndarray):
        self._longitudes = value

    @property
    def half_longitudes(self):
        """Half-list of longitudinal boundaries to avoid duplication. Deduced from :attr:`all_longitudes`."""

        if self._half_longitudes is None:
            self._half_longitudes = self.all_longitudes[:int(self.n_longitudes / 2)]

        return self._half_longitudes

    @property
    def all_longitudes(self) -> np.ndarray:
        """Longitudinal boundaries (first longitude duplicated to make a full circle).
         Deduced from :attr:`longitudes`."""

        if self._all_longitudes is None:
            if self.to_east:  # going up
                self._all_longitudes = np.concatenate([self.longitudes, [self.longitudes[0] + 2 * np.pi]])
            else:  # going down
                self._all_longitudes = np.concatenate([self.longitudes, [self.longitudes[0] - 2 * np.pi]])

        return self._all_longitudes

    @all_longitudes.setter
    def all_longitudes(self, value: np.ndarray):
        """Overwrite longitudinal boundaries."""

        self._all_longitudes = value

    @property
    def mid_longitudes(self) -> np.ndarray:
        """List of longitudes (in the \"middle\" of each longitude box). By default, start at -Pi."""

        if self._mid_longitudes is None:
            self._mid_longitudes = np.asarray([self.lon_angle * i for i in range(self.n_longitudes)]) - np.pi

        return self._mid_longitudes

    @mid_longitudes.setter
    def mid_longitudes(self, value):
        """Overwrite longitudes in the middle of each box."""
        self._mid_longitudes = np.asarray(value)

        # force recomputations of other variables that depend on mid_longitudes
        self._to_east = None
        self._all_longitudes = None
        self._half_longitudes = None
        self._longitudes = None

    @property
    def night_longitudes(self) -> List:
        """List of longitudinal indices on the `night` side.
        The night side is here defined as the first quarter of longitudinal indices and the last one.
        """

        return list(range(int(self.n_longitudes / 4))) + \
               list(range(int(self.n_longitudes * 3 / 4),
                          self.n_longitudes))  # BUG: Check what is returned, parenthesis hazard

    @property
    def day_longitudes(self) -> List:
        """List of longitudinal indices on the `day` side.
        The day side is here defined as the second and third quarters of longitudinal indices.
        """

        return list(range(int(self.n_longitudes / 4), int(self.n_longitudes * 3 / 4)))

    @property
    def lon_angle(self):
        """Angle between two longitudes."""

        if self._longitude_angle is None:
            self._longitude_angle = 2 * np.pi / self.n_longitudes

        return self._longitude_angle

    def make_3D(self, obj: Union[np.ndarray, dict], axis: Optional[List[int]] = None) -> np.ndarray:
        """This function will try to transform :attr:`obj` from whatever dimension it is (or a dict of arrays with whatever dimensions) into a 3D array (or a dict with 3D arrays) of the same shape as the grid.

        Args:
            obj (ndarray | dict): 1, 2 or 3 dimensional array (or dict with such arrays).

            axis (Optional[List[int]]): Allow to choose the value of axis. Use [0] to set a 1D pressure
        or temperature array seen as an atmospheric column to a 3D one.

        Returns:
            (ndarray | dict): 3D array (or dict with 3D arrays).
        """
        if isinstance(obj, dict):
            for k,v in obj.items():
                obj[k] = self.make_3D(v)
            return obj
        
        if not hasattr(obj, "shape") or obj.shape == self.shape:
            return obj

        # if axis is None:
        #     axis = [0]

        indices = np.arange(len(self.shape))
        if axis is None:
            axis = indices[np.isin(self.shape, obj.shape)]

        new_axis = tuple([i for i, s in enumerate(self.shape) if i not in axis])

        return np.ones(self.shape) * np.expand_dims(obj, axis=new_axis)

    def horizontal_walk(self, *args):
        """Iterator over horizontal grid (latitude, longitude)."""

        return self.walk([1, 2])

    def horizontal_run(self, function, *args, **kwargs):
        """Run a function over horizontal grid (latitude, longitude)."""

        results = np.empty(self.shape, dtype=object)
        dtype = object
        for lat, lon in self.walk([1, 2]):
            tmp = function(lat, lon, *args, **kwargs)
            try:
                dtype = tmp.dtype
            except:
                pass
            results[:, lat, lon] = tmp

        return np.asarray(results, dtype=dtype)

    def outputs(self):
        return self.inputs() + ['mid_latitudes', 'mid_longitudes']
