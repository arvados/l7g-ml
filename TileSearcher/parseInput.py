import argparse
import application
import yaml
global parser

CONFIG_FILENAME = 'config.yml'


def setup_parsing(app):
    # set up argument parsing

    app.parser = argparse.ArgumentParser(
        description="From an index of a tile, return the Tile Name, Variants, and/or Base Pair Locations")
    app.parser.add_argument(
        '-i',
        '--indices',
        type=int,
        nargs="+",
        help="Indices of tiles (use quotations for multiple, e.g. '352 562 3543523 4562'",
        required=True)


def read_config(app):
    with open(CONFIG_FILENAME, 'r') as stream:
        data_args = yaml.load(stream)
    app.set_functionality_from_config(data_args)
    app.verify_config(data_args)
    app.set_config_data_args(data_args)


def parse_input(app):
    # parse arguments
    args = app.parser.parse_args()
    # quit if no arguments were specified
    # set functionality and data locations based on parsed arguments
    read_config(app)

    app.set_tile_indices(args)

    return app
