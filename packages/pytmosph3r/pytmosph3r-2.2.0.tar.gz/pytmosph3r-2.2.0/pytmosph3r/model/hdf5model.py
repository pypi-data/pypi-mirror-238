from .model import FileModel
from ..interface.hdf5 import HDF5Input


class HDF5Model(FileModel):
    """Model reading from HDF5. Same parameters as :class:`~pytmosph3r.model.model.Model`, with the addition of a :attr:`filename`."""
    
    def read_data(self, *args, **kwargs):
        """This method is automated (see :func:`~pytmosph3r.interface.io.Input.read`).
        """
        self.info(f"Reading model from {self.filename}")
        model = {}

        with HDF5Input(self.filename) as f:
            model = f.read("Model")
        self.__dict__.update(model.__dict__)
