import datetime
from abc import ABC

import h5py
from packaging import version

from pytmosph3r.__version__ import __version__
from pytmosph3r.log import Logger
from pytmosph3r.util.util import retrieve_name
from .io import Input, Output


class HDF5Input(Input):
    def __init__(self, filename):
        Logger.__init__(self, name=self.__class__.__name__)
        Input.__init__(self, filename=filename)

        self.variable = h5py.Dataset

    @property
    def attrs(self):
        return self.f.attrs

    def _openFile(self):
        self.f = h5py.File(self.filename, mode='r')

    def getclass(self, path):
        return self.f[path].attrs["class"]

    def get(self, path):
        if self.f is None:
            self._openFile()
        value = self.f[path][...]
        if value.ndim == 0:
            try:
                return float(value)
            except:
                if version.parse(h5py.version.version) >= version.parse("3"):
                    try:
                        return self.f[path].asstr()[()]
                    except:
                        return str(value)
                return str(value)
        if version.parse(h5py.version.version) >= version.parse("3"):
            try:
                return self.f[path].asstr()[()]
            except:
                return value
        return value


class HDF5Output(Output, HDF5Input):
    def __init__(self, filename, append=False):
        Logger.__init__(self, 'HDF5Output')
        Output.__init__(self, filename, append)

        self.group_func = h5py.Group.create_group
        self.group_class = HDF5Group

    def get(self, path):
        raise NotImplementedError

    def getclass(self, path):
        raise NotImplementedError

    def _openFile(self):
        mode = 'w'

        if self._append:
            mode = 'a'

        self.f = h5py.File(self.filename, mode=mode)

        self.f.attrs['file_name'] = self.filename
        self.f.attrs['file_time'] = datetime.datetime.now().isoformat()
        self.f.attrs['creator'] = self.__class__.__name__
        self.f.attrs['HDF5_Version'] = h5py.version.hdf5_version
        self.f.attrs['h5py_version'] = h5py.version.version
        self.f.attrs['program_name'] = 'Pytmosph3R'
        self.f.attrs['program_version'] = __version__

    def write_string_array(self, string_array, string_name=None, metadata=None):
        if string_name is None:
            key = retrieve_name(string_array, up=2)  # 2 because of wrapper

        asciiList = [n.encode("ascii", "ignore") for n in string_array]

        return self.f.create_dataset(str(string_name), (len(asciiList)), 'S64', asciiList)


class HDF5Group(HDF5Output, ABC):
    def __init__(self, f):
        super().__init__('HDF5Group')
        self.f = f


def write_hdf5(h5_output, model, group_name="Model", items=None):
    """Write :attr:`model` into group `group_name` in HDF5 `h5_output`. The output file is separated into a group "Model" with the inputs, and a group "Output" with the outputs.

    Args:
        h5_output (string): Name of HDF5 output file.

        model (:class:`~pytmosph3r.model.model.Model`):  Model to write.

        group_name (str, optional): Either "Model", "Output", or "All". Decides which data to write to :attr:`group_name`: "Model" writes the input model only, "Output" writes the output data, and "All" writes everything. Defaults to "Model".

        items (list): items to write into group.
    """

    if h5_output is None:
        return

    append = False
    all = True  # try to write everything, except when we just want the input Model
    to_write = 'outputs'

    if group_name in ("Model", "Input"):
        to_write = 'inputs'

    if group_name == "Output":
        append = True

    if group_name == "All":
        group_name = "Output"

    if group_name in ("Model", "Input") or items is not None:
        all = False

    if group_name not in ("Model", "Input", "Output", "All"):
        Logger("HDF5Output").warning(
            "Does not know group %s. Will consider it as outputs, but beware that may break some features." % group_name)
        append = True

    with HDF5Output(h5_output, append=append) as o:
        group = o.create_group(group_name)

        if all:
            try:  # try to write model if not already written
                model_group = o.create_group("Model")
                model_group.write_obj(model, to_write='inputs')
            except ValueError:
                pass  # model already written

            group.write_obj(model, to_write="outputs")
        else:
            group.write_obj(model, to_write=to_write, items=items)
