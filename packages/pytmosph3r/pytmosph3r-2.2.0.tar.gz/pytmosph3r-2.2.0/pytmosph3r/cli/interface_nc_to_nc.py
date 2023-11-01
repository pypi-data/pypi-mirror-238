from pytmosph3r.atmosphere import InputAtmosphere
from pytmosph3r.interface import ncOutput
from pytmosph3r.model import DiagfiModel
from pytmosph3r.observations import Emission


def nc_to_nc():
    """Utility tool to rewrite a diagfi.nc.
    """
    import argparse
    import json

    parser = argparse.ArgumentParser(description='diagfi-to-diagfi-converter')
    parser.add_argument("-i", "--input", dest="input", type=str, required=True, help="Input diagfi filename")
    parser.add_argument("-r", "--radius-scale", dest='radius_scale', default=1, type=float,
                        help="Change the scale of the radius of the planet when saving .nc (for visual reasons).")
    parser.add_argument("-p", "--min-pressure", dest='min_pressure', type=float, default=1e-5,
                        help="Top pressure.")
    parser.add_argument("-o", "--output", dest="output", type=str, required=True,
                        help="Output netCDF filename")
    parser.add_argument('-gd', '--gas-dict', default="{}", type=json.loads,
                        help="Example: {\\\"H2O\\\":\\\"h2o_vap\\\"}")
    parser.add_argument('-g', '--gas-mix-ratio', default="{}", type=json.loads,
                        help="Example: {\\\"H2O\\\":5e-4}")
    args = parser.parse_args()

    # gas_dict = json.loads(args.gas_dict)
    gas_dict = args.gas_dict
    model = DiagfiModel(filename=args.input, gas_dict=gas_dict,
                        input_atmosphere=InputAtmosphere(gas_mix_ratio=args.gas_mix_ratio),
                        emission=Emission())
    model.read_data()
    model.input_atmosphere.build(model)
    model.atmosphere = model.input_atmosphere

    with ncOutput(args.output) as nc:
        nc.write_model(model, radius_scale=args.radius_scale)


if __name__ == "__main__":
    nc_to_nc()
