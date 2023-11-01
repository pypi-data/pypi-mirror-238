import argparse

from pytmosph3r.__version__ import __version__ as version


def pytmosph3r_parser():
    """Returns a parser, which can be included in the documentation.
    """
    parser = argparse.ArgumentParser(description='Pytmosph3R {}'.format(version))

    parser.add_argument("-i", "--input", dest='input_file', type=str,
                        required=True, help="Input config file to use")
    parser.add_argument("-p", "--plot", dest='plot', default=False,
                              help="Whether to plot after the run",
                              action='store_true')
    parser.add_argument("-g", "--debug-log", dest='debug', const="stats",
                        nargs='?',type=str, help="Debug profile filename (also activates debug messages).")
    parser.add_argument("-o", "--output-folder", dest='output_folder', default=".", type=str, help="Outputs folder.")
    parser.add_argument("-a","--all",dest="all", default=False, help="Write everything. Absolutely everything! HDF5 (max verbose), netCDF, .dat, ...",action='store_true')
    parser.add_argument("-h5", "--hdf5-output", dest='h5_output', default="output_pytmosph3r.h5", type=str, help="Output HDF5 filename.")
    parser.add_argument("-l", "--light", dest='light_output', action='store_true', help="Do not write HDF5 (for lighter output). You should probably also use the -S option then.")
    parser.add_argument("-v", "--verbose", dest='verbose', nargs='?', const=1, type=int, help="Verbose level in HDF5 file (larger but more complete information). Between 0,1,2.")
    parser.add_argument("-vv", "--very-verbose", dest='verbose', const=2, action='store_const', help="Very verbose output in HDF5 file (complete information). Be sure you want to fill your disk with data!")
    parser.add_argument("-nc", "--nc-output", dest='nc_output', nargs='?', const="output_pytmosph3r.nc", type=str, help="netCDF filename. Can be visualized with ncview, paraview, ...")
    parser.add_argument("-r", "--radius-scale", dest='radius_scale', default=0, type=float, help="Change the scale of the radius of the planet when saving .nc (for visual reasons).")
    parser.add_argument("-s", "--save-spectrum", nargs='?', const="pytmosph3r_spectrum.dat",
                        dest='spectrum_dat_output', type=str, help="Write spectrum into a light .dat file. For a faster execution of the program, run with this option and -l")
    return parser