from subprocess import call, Popen, PIPE, STDOUT
import os
from collections import defaultdict

# test whether a command is available to the comptuer
def test_command(command, error_msg):
		try:
			call(command, stdout=PIPE, stderr=PIPE)
		except OSError as e:
			if e.errno == os.errno.ENOENT:
				raise Exception(error_msg)

class Tile:
	def __init__(self, index):
		self.index = index
		self.path = None
		self.phase = None
		self.step = None
		self.tile_str = None

	def __str__(self):
		return "Tile {} information:\n{}\nPath: {}\nStep: {}\nPhase: {}".format(self.index, self.tile_str, self.path, self.step, self.phase)

class TileApplication:
	# initialize False defaultdicts for functionality and data
	def __init__(self):
		self.functionality = defaultdict(lambda: False)
		self.data = defaultdict(lambda: False)
		self.tiles = []

	def set_functionality(self, args):
		# parse functionality from input and save to dictionary
		for idx in args.indices:
			self.tiles.append(Tile(idx))
		if args.get_location == None:
			if args.assembly_fwi == None:
				raise Exception("Cannot get tile location without --assembly-fwi argument.")
			self.functionality['get_location'] = True
		if args.print_variant_diffs == None:
			if args.keep == None:
				raise Exception("Cannot get variant diffs without --keep argument.")
			self.functionality['print_variant_diffs'] = True
		if args.get_diff_indices == None:
			if args.keep == None:
				raise Exception("Cannot get diff indices without --keep argument.")
			self.functionality['get_diff_indices'] = True	
		if args.get_base_pair_locations == None:
			if args.assembly_gz == None:
				raise Exception("Cannot get base pair locations without --assembly-gz argument.")
			self.functionality['get_base_pair_locations'] = True

	def save_data_args(self, args):
		# save data to dictionary in application
		self.data['hiq_info'] = args.hiq_info
		self.data['assembly_gz'] = args.assembly_gz
		self.data['assembly_fwi'] = args.assembly_fwi
		self.data['keep'] = args.keep

	def get_functionality(self):
		# create a string that displays what the application will calculate
		base_str = ""
		if self.functionality['get_base_pair_locations']: 
			base_str += "Finding Tile Location, "
		if self.functionality['print_variant_diffs']:
			base_str += "Printing Variant Differences (ClustalW), "
		if self.functionality['get_diff_indices']:
			base_str += "Finding Indices of Variant Differences, "
		if self.functionality['get_base_pair_locations']:
			base_str += "Retrieving Base Pair Locations"
		
		return base_str

	def test_command_availability(self):
		# tests the following commands based on input: bgzip, zgrep, clustalo, cat
		if self.functionality['get_base_pair_locations']:
			test_command(['bgzip', '-help'], "bgzip is not installed or is not available in the PATH.")
		if self.functionality['get_location']:
			test_command(['cat', '--help'], "cat is not available on this system.")
		if self.functionality['get_location'] or self.functionality['print_variant_diffs'] or self.functionality['get_diff_indices']:
			test_command(['zgrep', '--help'], "zgrep is not installed or is not available in the PATH")
		if self.functionality['print_variant_diffs'] or self.functionality['get_diff_indices']:
			test_command(['clustalo', '--help'], "clustalo is not installed or is not avaialble in the PATH.")