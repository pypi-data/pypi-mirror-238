import datetime
import logging
import os

from pytmosph3r.__version__ import __version__ as version
from pytmosph3r.cli.parser import pytmosph3r_parser
from pytmosph3r.config import Config
from pytmosph3r.interface import write_netcdf, write_spectrum
from pytmosph3r.log import Logger, root_logger, setLogLevel

"""The entry point to Pytmosph3R"""


def main():
    """Reads a config file and runs Pytmosph3R"""

    root_logger.info('Welcome to Pytmosph3R %s' % version)
    root_logger.info("\n"
                     "         ,MMM8&&&.\n"  # noqa
                     "    _...MMMMM88&&&&..._\n"  # noqa
                     " .::'''MMMMM88&&&&&&'''::.\n"  # noqa
                     "::     MMMMM88&&&&&&     ::\n"  # noqa
                     "'::....MMMMM88&&&&&&....::'\n"  # noqa
                     "   `''''MMMMM88&&&&''''`\n"  # noqa
                     "         'MMM8&&&'\n")  # noqa

    parser = pytmosph3r_parser()

    args = parser.parse_args()
    if args.all:
        if args.verbose is None:
            args.verbose = 2
        if args.h5_output is None:
            args.h5_output = "output_pytmosph3r.h5"
        if args.nc_output is None:
            args.nc_output = "output_pytmosph3r.nc"
        if args.spectrum_dat_output is None:
            args.spectrum_dat_output = "spectrum_pytmosph3r.dat"
    elif args.verbose is None:
        args.verbose = 0

    start_time = datetime.datetime.now()
    root_logger.info('Pytmosph3R PROGRAM START AT %s', start_time)
    Logger.verbose = args.verbose

    if args.debug:
        import cProfile
        pr = cProfile.Profile()
        pr.enable()
        setLogLevel(logging.DEBUG)

        import ntpath
        def path_leaf(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)

        prefix = "%s_" % args.debug
        stats_file = prefix + path_leaf(args.input_file)
        stats_file = os.path.join(args.output_folder, stats_file)
        stats_file = os.path.splitext(stats_file)[0] + ".prof"

    if args.input_file.endswith(".cfg"):
        root_logger.warning("Configuration files won't be supported in the future. We encourage you to load and run Pytmosph3R directly via python files.")
        # Parse the input file
        config = Config()
        config.search_path(args.input_file)
        config.read(config.filename)

        # Setup global parameters
        config.setup_globals()
        # Generate a model from the input
        model = config.generate_model()

    os.makedirs(args.output_folder, exist_ok=True)
    h5_output = os.path.join(args.output_folder, args.h5_output)
    model.output_file = h5_output

    model.build()
    model.run()

    if args.spectrum_dat_output:
        spectrum_dat_output = os.path.join(args.output_folder, args.spectrum_dat_output)
        write_spectrum(spectrum_dat_output, model)

    if args.nc_output:
        nc_output = os.path.join(args.output_folder, args.nc_output)
        root_logger.info('Creating netCDF file at %s ...', nc_output)
        write_netcdf(nc_output, model, args.radius_scale)

    end_time = datetime.datetime.now()
    root_logger.info('Pytmosph3R PROGRAM END AT %s s', end_time)
    total_time = end_time - start_time
    root_logger.info('Pytmosph3R run in %.2f s', total_time.total_seconds())

    if args.debug:
        pr.disable()
        pr.create_stats()
        root_logger.info('Recording stats in %s', stats_file)
        pr.dump_stats(stats_file)
        root_logger.info('Stats - DONE')

    from pytmosph3r.plot import Plot
    plot = Plot(model=model, out_folder=args.output_folder)
    if args.plot:
        plot.interactive = True
    plot.plot_spectrum(legend=False)


if __name__ == "__main__":
    main()
