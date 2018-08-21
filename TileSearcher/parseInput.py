import argparse
import application
import yaml
global parser

def setup_parsing(app):
	# set up argument parsing
	
	app.parser = argparse.ArgumentParser(description="From an index of a tile, return the Tile Name, Variants, and/or Base Pair Locations")
	app.parser.add_argument('-i', '--indices', type=int, nargs="+", help="Indices of tiles (use quotations for multiple, e.g. '352 562 3543523 4562'", required=True)
	app.parser.add_argument('--tile-info', type=str, help="Location of tile names (for PGP, it is called hiq-pgp-info). Always required.")
	app.parser.add_argument('--location', type=int, nargs='?', default=False, help="Whether to get tile location. REQUIREMENTS: cat, zgrep, and assembly-fwi")
	app.parser.add_argument('--variant-diffs', type=int, nargs='?', default=False, help="Print tile variants (a/t/c/g) diffs (ClustalW output). REQUIREMENTS: zgrep, keep collection, ClustalW.")
	app.parser.add_argument('--diff-indices', type=int, nargs='?', default=False, help="Whether to print the tile variants with diff indices. REQUIREMENTS: zgrep, keep collection, ClustalW.")
	app.parser.add_argument('--base-pair-locations', type=int, nargs='?', default=False, help="Whether to get base pair locations. REQUIREMENTS: bgzip and assembly-gz)")
	app.parser.add_argument('--assembly-gz', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.gz")
	app.parser.add_argument('--keep', type=str, nargs='?', default=None, help="Location of keep collection with *.sglf.gz files")
	app.parser.add_argument('--assembly-fwi', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.fwi")
	app.parser.add_argument('--write-to-file', type=int, nargs='?', default=False, help="Whether to write to a file or print to stdout.")


def parse_input(app):
	# parse arguments
	args = app.parser.parse_args()
	# quit if no arguments were specified
	# set functionality and data locations based on parsed arguments

	if args.location == None or args.variant_diffs == None or args.diff_indices == None or args.base_pair_locations == None:
		#print([args.location, args.variant_diffs, args.diff_indices, args.base_pair_locations])
		app.set_functionality(args)
	else:
		print("Setting functionality from config...")
		with open('config.yml', 'r') as stream:
			data_args = yaml.load(stream)
		app.set_functionality_from_config(args, data_args)

	if args.write_to_file == None:
		app.write_to_file = True
		print("Writing to file...")
	else:
		app.write_to_file = False

	if not all([args.assembly_fwi, args.keep, args.assembly_gz]):
		# if no command line data arguments are specified, read from config
		print("No data command line arguments specified. Reading from config.yml...")
		with open('config.yml', 'r') as stream:
			data_args = yaml.load(stream)

		# verify that necessary data is provided
		app.verify_config(args, data_args)

		# set data and functionality
		app.set_config_data_args(data_args)
	else:	
		if args.location == args.variant_diffs == args.diff_indices == args.base_pair_locations == False: 
			raise Exception("Nothing to find.")

		# verify that the data needed is provided in command line arguments
		app.verify_args(args)

		# set data and functionality
		app.set_data_args(args)

	app.set_tile_indices(args)

	return app