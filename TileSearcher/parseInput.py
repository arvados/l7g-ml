import argparse
import application
global parser

def setup_parsing(app):
	# set up argument parsing
	
	app.parser = argparse.ArgumentParser(description="From an index of a tile, return the Tile Name, Variants, and/or Base Pair Locations")
	app.parser.add_argument('-i', '--indices', type=int, nargs="+", help="Indices of tiles (use quotations for multiple, e.g. '352 562 3543523 4562'", required=True)
	app.parser.add_argument('--hiq-info', type=str, help="Location of tile names (for PGP, it is called hiq-pgp-info). Always required.", required=True)
	app.parser.add_argument('--get-location', type=int, nargs='?', default=False, help="Whether to get tile location. REQUIREMENTS: cat, zgrep, and assembly-fwi")
	app.parser.add_argument('--print-variant-diffs', type=int, nargs='?', default=False, help="Print tile variants (a/t/c/g) diffs. REQUIREMENTS: zgrep, keep collection, ClustalW.")
	app.parser.add_argument('--get-diff-indices', type=int, nargs='?', default=False, help="Whether to print the tile variants with diff indices. REQUIREMENTS: zgrep, keep collection, ClustalW.")
	app.parser.add_argument('--get-base-pair-locations', type=int, nargs='?', default=False, help="Whether to get base pair locations. REQUIREMENTS: bgzip and assembly-gz)")
	app.parser.add_argument('--assembly-gz', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.gz")
	app.parser.add_argument('--keep', type=str, nargs='?', default=None, help="Location of keep collection with *.sglf.gz files")
	app.parser.add_argument('--assembly-fwi', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.fwi")

def parse_input(app):
	# parse arguments
	args = app.parser.parse_args()
	print(args.index)
	# quit if no arguments were specified
	if args.get_location == args.print_variant_diffs == args.get_diff_indices == args.get_base_pair_locations == False: 
		raise Exception("Nothing to find.")

	# set functionality and data locations based on parsed arguments
	app.set_functionality(args)
	app.save_data_args(args)
	return app