from pytmosph3r.interface import HDF5Output
from pytmosph3r.model import DiagfiModel


def nc_to_h5():
    """Utility tool to convert a diagfi.nc to HDF5 file.
    """
    import argparse
    parser = argparse.ArgumentParser(description='diagfi-to-hdf5-converter')
    parser.add_argument("-i", "--input", dest="input", type=str, required=True, help="Input diagfi filename")
    parser.add_argument("-o", "--output", dest="output", type=str, required=True, help="Output HDF5 filename")
    args = parser.parse_args()

    diagfi_data = DiagfiModel(args.input)
    diagfi_data.read_data()
    with HDF5Output(args.output) as o:
        group = o.create_group("Model")
        group.write_obj(diagfi_data)


if __name__ == "__main__":
    nc_to_h5()
