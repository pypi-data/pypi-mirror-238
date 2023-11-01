from pytmosph3r.interface import HDF5Input, ncOutput


def h5_to_nc():
    """Convert a HDF5 file to NETCDF4.
    """
    import argparse
    parser = argparse.ArgumentParser(description='diagfi-to-hdf5-converter')
    parser.add_argument("-i", "--input", dest="input", type=str, required=True, help="Input H5 filename")
    parser.add_argument("-o", "--output", dest="output", type=str, required=True, help="Output NC filename")
    args = parser.parse_args()

    with HDF5Input(args.input) as h:
        model = h.read("Model")
        output = h.read("Output")

        with ncOutput(args.output) as nc:
            nc.write_model(model, output)


if __name__ == "__main__":
    h5_to_nc()
