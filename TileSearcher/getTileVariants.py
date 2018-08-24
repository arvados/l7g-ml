#!/usr/bin/env python
# Created by Kevin Fang, 2018 at Curoverse.
# Searches for tile name, base pairs, and variants

from __future__ import print_function
import subprocess, sys, numpy as np
from subprocess import CalledProcessError, Popen, PIPE, STDOUT
import clustalo, parseInput
from application import TileApplication, Tile
from copy import deepcopy

# initialize new application
app = TileApplication()

# set up command line arguments
parseInput.setup_parsing(app)

# parse command line arguments
parseInput.parse_input(app)

# ensure that the system has the commands it needs to search
app.test_command_availability()

# set up information needed for tile search
coefPaths = np.load(app.data['tile_info'])
tile_path = np.trunc(coefPaths / (16 ** 5))
tile_step = np.trunc((coefPaths - tile_path * 16 ** 5) / 2)
tile_phase = np.trunc((coefPaths - tile_path * 16 ** 5 - 2 * tile_step))
vhex = np.vectorize(hex)
vectorized_path = vhex(tile_path.astype('int'))
vectorized_step = vhex(tile_step.astype('int'))
vectorized_phase = vhex(tile_phase.astype('int'))

# search for tile information from assembly files
def tile_search(index):
	vec_path = str(vectorized_path[int(index)])
	vec_path = vec_path[2:].zfill(4)

	try:
		proc = subprocess.check_output("cat " + app.data['assembly_fwi'] + " | grep :" + vec_path, shell=True)
		return proc
	except CalledProcessError as e:
		raise Exception("Assembly index file not found.", str(e))

# fill a tile object with appropriate path, step, and phase info
def fill_tile_info(tile_item):
	index = tile_item.index
	tile = tile_search(index)
	path = vectorized_path[index]
	step = vectorized_step[index]
	phase = vectorized_phase[index]

	# remove 'x' from hexadecimal number.
	filled_tile = Tile(index)
	filled_tile.path = path[2:].zfill(4)
	filled_tile.step = step[2:].zfill(4)
	filled_tile.phase = phase
	filled_tile.tile_str = tile.rstrip()

	return filled_tile

# fill a tile object with variant information from assembly files
def fill_variants_info(tile_item):
	filled_tile = deepcopy(tile_item)
	filename = "{}/{}.sglf.gz".format(app.data['keep'], tile_item.path)
	try:
		filled_tile.variants = subprocess.check_output('zgrep {}.00.{} {}'.format(tile_item.path, tile_item.step, filename), shell=True)
		return filled_tile
	except CalledProcessError as e:
		raise Exception("Collection not found: {}".format(filename))

# fill a tile object with clustal omega output
def fill_clustalo_entries(tile_item):
	filled_tile = deepcopy(tile_item)

	# split a single long variant string into a list of variants, separated by newline
	variants = tile_item.variants.split('\n')[:-1]

        if len(variants) == 1:
            filled_tile.clustalo_output = ([[variants[0]]], "")
            return filled_tile
	# convert list to fasta for clustalo
	fasta = clustalo.convert_list_to_fasta(variants) # clustalo output goes (entries, diffs) - calculates both
	filled_tile.clustalo_output = clustalo.get_clustalo(fasta)
	return filled_tile

# fill a tile object with the differences found by clustal omega (counts asterisks)
def fill_clustalo_diffs(tile_item):
	filled_tile = deepcopy(tile_item)
	clustal_entries = filled_tile.clustalo_output[1]

	# counts spaces in the string of asterisks
	diffs = []
	for j, string in enumerate(clustal_entries):
		spaces = [i + 60 * j + 1 for i, ltr in enumerate(string) if ltr == " "]
		diffs.extend(spaces)

	# save to tile
	filled_tile.clustalo_entries = filled_tile.clustalo_output[0]
	filled_tile.clustalo_diffs = diffs
	return filled_tile

# fill a tile object with base pair locations
def fill_bp_loc(tile_item):
	filled_tile = deepcopy(tile_item)
	# split the tile str into components for analysis
	split = filled_tile.tile_str.split('\t')
	begin = int(split[2])
	sequence = int(split[1])
	
	# read base pair locations from assembly files
	cmdToRun = "bgzip -c -b %d -s %d -d %s | grep -B1 \"%s\s\"" % (begin, sequence, app.data['assembly_gz'], filled_tile.step)

	try:
		# call bgzip to locate base pair locations
		subprocess.call("bgzip -r " + app.data['assembly_gz'], shell=True)
		output = subprocess.check_output(cmdToRun, shell=True)
		filled_tile.bp_output = output
		return filled_tile
	except CalledProcessError as e:
		raise Exception("assembly file not found.")

def fill_snp_locations(tile_item):
	filled_tile = deepcopy(tile_item)
	
def calc_var_diffs(tile_item):
	filled_tile = deepcopy(tile_item)
	return fill_clustalo_diffs(fill_clustalo_entries(fill_variants_info(filled_tile)))

from operator import itemgetter
from itertools import groupby
def group_continuous_diffs(clustalo_diffs):
	groups = []
	for _, j in groupby(enumerate(clustalo_diffs), lambda (k, x): k - x):
		groups.append(map(itemgetter(1), j))
	return groups

# out is a function that tells the program what to do with output - send to a file or print?
def tile_iteration(tile, out):
# get the location of tiles and store it because it will be important later
	tile = fill_tile_info(tile)
	if app.functionality['location']: # get tile location, path, step phase	
		out(str(tile).rstrip() + '\n')

	if app.functionality['base_pair_locations']: # get base pair location
		tile = fill_bp_loc(tile)
		out(tile.bp_output.rstrip() + '\n')

	if app.functionality['variant_diffs']: # get variant differences using ClustalW
		# fill the variant info for the file, in case needed later
		tile = calc_var_diffs(tile)
		tile.diffs_calculated = True

		for item in tile.clustalo_entries:
			out("\n".join(item))
			out('\n')
		
	if app.functionality['diff_indices']: # get the indices of the variant differences
		if not tile.diffs_calculated:
			tile = calc_var_diffs(tile)			
		#out("Index of variant differences: {}\n".format(tile.clustalo_diffs))
		
		# read base pair location from tile
		if not tile.bp_output:
			tile = fill_bp_loc(tile)

		import re
		base_pairs = re.split(r'\s+', tile.bp_output)	

		# group the diffs so it doesn't print out a huge list of ints
		grouped_diffs = group_continuous_diffs(tile.clustalo_diffs)		

		exact_locs = []
		output_diffs = []
		# find the base pair location
		convert = lambda x: x - 24 + int(base_pairs[1])
		for diff in grouped_diffs:
			if len(diff) == 1:
				exact_locs.append(convert(diff[0]))
				output_diffs.append(diff[0]) 
			else:
				exact_locs.append((convert(diff[0]), convert(diff[-1])))
				output_diffs.append((diff[0], diff[-1]))

		# print results
		index_pos_map = list(zip(output_diffs, exact_locs))

		out("Variant diffs:\n")
		if len(index_pos_map) == 0:
			out("Only one variant found.\n")
		for position, index in index_pos_map:
			if type(position) is int:
				out("Position on chromosome: {}, index of diff: {}\n".format(position, index))
			else:
				out("Position range on chromosome: {}-{}, index range: {}-{}\n".format(position[0], position[1], index[0], index[1]))

	print("Finished search for tile {}\n".format(tile.index))

# iterate through input array of tiles
for tile in app.tiles:
	if app.write_to_file:
		import os
		if not os.path.exists('output'):
			os.mkdir('output')
		with open("output/{}.txt".format(tile.index), 'w') as f:
			tile_iteration(tile, f.write)
	else:
		tile_iteration(tile, print)
