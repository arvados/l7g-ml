#!/usr/bin/env python
# Created by Kevin Fang, 2017 at Curoverse.
# Searches for tile name, base pairs, and variants

import subprocess, argparse
import numpy as np
from subprocess import CalledProcessError, Popen, PIPE, STDOUT
import sys
import clustalo

class color:
    RED = '\033[91m'
    END = '\033[0m'

# set up argument parsing
parser = argparse.ArgumentParser(description="From an index of a tile, return the tile name, variants, and/or Base Pair Locations")
parser.add_argument('-i', '--index', type=int, help="An index of the tile", required=True)
parser.add_argument('--hiq-info', type=str, help="Location of tile names (for PGP, it is called hiq-pgp-info)", required=True)
parser.add_argument('-l', '--get-location', type=int, nargs='?', default=False, help="Whether to get tile location (requires cat, grep, and assembly.00.hg19.fw.fwi)")
parser.add_argument('-v', '--get-variants', type=int, nargs='?', default=False, help="Whether to get tile variants (a/t/c/g) (requires zgrep and the keep collection with *.sglf.gz)")
parser.add_argument('-pvd', '--print-variant-diffs', type=int, nargs='?', default=False, help="Whether to print the tile variants (a/t/c/g) diffs. Takes longer than -v, still requires zgrep and keep collection.")
parser.add_argument('-vdi', '--get-variant-diff-indices', type=int, nargs='?', default=False, help="Whether to print the tile variants with diff indices. Takes longer than -v, still requires zgrep and keep colleciton.")
parser.add_argument('-b', '--get-base-pairs', type=int, nargs='?', default=False, help="Whether to get base pair locations (requires bgzip and assembly.00.hg19.fw.gz)")
parser.add_argument('--assembly-gz', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.gz")
parser.add_argument('--keep', type=str, nargs='?', default=None, help="Location of keep collection with *.sglf.gz")
parser.add_argument('--assembly-fwi', type=str, nargs='?', default=None, help="Location of assembly.00.hg19.fw.fwi")
args = parser.parse_args()

if args.get_location == args.get_variants == args.print_variant_diffs == args.get_variant_diff_indices == args.get_base_pairs == False: 
    print "Nothing to find. Exiting..."
    sys.exit(0) 

print "Finding:"
# set None values to true for easier if statements and print if any arguments are missing
if args.get_location == None: 
    if args.assembly_fwi == None:
        print "Cannot get tile location without --assembly-fwi argument. Exiting..."
        sys.exit(1)
    args.get_location = True
    print "Tile location"
if args.get_variants == None: 
    if args.keep == None:
        print "Cannot get variants without --keep argument. Exiting..."
        sys.exit(1)
    args.get_variants = True
    print "Tile variants"
if args.print_variant_diffs == None:
    if args.keep == None:
        print "Cannot get variant diffs without --keep argument. Exiting..."
        sys.exit(1)
    args.print_variant_diffs = True
    print "Annotated Tile Variant Diffs"
if args.get_variant_diff_indices == None:
    if args.keep == None:
        print "Cannot get variant diffs without --keep argument. Exiting..."
        sys.exit(1)
    args.get_variant_diff_indices = True
    print "Tile Variant Diff Indices"
if args.get_base_pairs == None: 
    if args.assembly_gz == None:
        print "Cannot get base pair location without --assembly-gz argument. Exiting..."
        sys.exit(1)
    args.get_base_pairs = True
    print "Base pair location"
print "For index", args.index, '\n'

# set up information needed for tile search
coefPaths = np.load(args.hiq_info)
tile_path = np.trunc(coefPaths / (16 ** 5))
tile_step = np.trunc((coefPaths - tile_path * 16 ** 5) / 2)
tile_phase = np.trunc((coefPaths - tile_path * 16 ** 5 - 2 * tile_step))
vhex = np.vectorize(hex)
vectorizedPath = vhex(tile_path.astype('int'))
vectorizedStep = vhex(tile_step.astype('int'))
vectorizedPhase = vhex(tile_phase.astype('int'))

# search for a tile
def tileSearch(arg):
    vecpath = str(vectorizedPath[int(arg)])
    vecpath = vecpath[2:].zfill(4)
    try:
        #proc = Popen(['cat', args.assembly_fwi, "|", "grep", ":", vecpath], stdout=PIPE, stderr=STDOUT)
        #print proc.communicate()
        proc = subprocess.check_output("cat " + args.assembly_fwi + " | grep :" + vecpath, shell=True)
        return proc
    except CalledProcessError as e:
        return "Assembly index file not found or `cat` command not available. Continuing..."

# get the location of a tile
def getTileLocation(arg,raw_tile_data):
    split_raw = raw_tile_data.split('\t')
    begin = int(split_raw[2])
    sequence = int(split_raw[1])
  # hexVal = split_raw[0].split(':')[2]
    vecstep = str(vectorizedStep[int(arg)])
    vecstep = vecstep[2:].zfill(4)
    
    cmdToRun = "bgzip -c -b %d -s %d -d %s | grep -B1 \"%s\s\"" % (begin, sequence, args.assembly_gz, vecstep)
    try:
        subprocess.call("bgzip -r " + args.assembly_gz, shell=True)
        output = subprocess.check_output(cmdToRun, shell=True)
        return output
    except CalledProcessError as e:
        return "bgzip not installed or assembly file (assembly.00.hg19.fw.gz) not found. Continuing...."

# get the tile path, step, and phase and print out if needed
tilePath = vectorizedPath[args.index]
tileStep = vectorizedStep[args.index]
tilePhase = vectorizedPhase[args.index]
if (args.get_location):
    print "Tile information:"
    tile = tileSearch(args.index)
    print "Tile Path:", tilePath
    print "Tile Step:", tileStep 
    print "Tile Phase:", tilePhase 
    print tile.rstrip() + '\n'

# print out base pairs if needed
if (args.get_base_pairs):
    print "Base pair location:"
    tile = tileSearch(args.index)
    print getTileLocation(args.index,tile).rstrip() + '\n'

# format tilePath by removing 0x value and padding with spaces so length = 4 
tilePath = tilePath[2:].zfill(4)
tileStep = tileStep[2:].zfill(4)

# get tile variants using zgrep command on keep collection
if (args.get_variants):
    try:
        #proc = Popen(['zgrep', "{}.00.{} {}/{}.sglf.gz".format(tilePath, tileStep, args.keep, tilePath)], stdout=PIPE, stderr=STDOUT)
        #variants = proc.communicate()
        variants = subprocess.check_output("zgrep %s.00.%s %s/%s.sglf.gz" % (tilePath, tileStep, args.keep, tilePath), shell=True)
    except CalledProcessError:
        print "Collection not found or `zgrep` command not available. Finishing..."
        sys.exit()
    print "Variant Information:"
    print variants

def getDifferentIndices(variants):
    fasta = clustalo.convert_list_to_fasta(variants)
    return clustalo.get_diff_indices(fasta)

if args.get_variant_diff_indices:
    try:
        #proc = Popen(['zgrep', "{}.00.{} {}/{}.sglf.gz".format(tilePath, tileStep, args.keep, tilePath)], stdout=PIPE, stderr=STDOUT)
        #variants = proc.communicate()
        variants = subprocess.check_output("zgrep %s.00.%s %s/%s.sglf.gz" % (tilePath, tileStep, args.keep, tilePath), shell=True)

    except CalledProcessError:
        print "Collection not found or `zgrep` command not available. Finishing..."
        sys.exit()

    # split commandline output into each variant
    variants = variants.split('\n')[:-1]

    differentIndices = getDifferentIndices(variants) 
    # split tile hash and name from the actual sequence for clustalo
    for i, variant in enumerate(variants):
       splits = variant.split(',')
       variants[i] = ["".join([splits[0], splits[1]]), splits[2]]
    # add 1, as counting differences are offset by 1
    print "Index of variant differences:", differentIndices 

def print_red_diffs(variants):

    # split tile hash and name from the actual sequence for clustalo
    for i, variant in enumerate(variants):
       splits = variant.split(',')
       variants[i] = ["".join([splits[0], splits[1]]), splits[2]]

    for variant in variants:
        # print out tile name and hash value
        print ",".join(variant[:-1]) + ",",
        
        diffStatus = False
        # write to stdout (so there won't be spaces after each letter) in color.RED if there are differences and normal color if there aren't 
        for i, letter in enumerate(variant[1]):
            if i + 1 in differentIndices and not diffStatus:
                sys.stdout.write(letter)
                sys.stdout.write(color.RED)
                diffStatus = True
            elif i + 1 in differentIndices and diffStatus:
                sys.stdout.write(letter)
            elif i + 1 not in differentIndices and diffStatus:
                sys.stdout.write(letter)
                sys.stdout.write(color.END)
                diffStatus = False
            elif i + 1 not in differentIndices and not diffStatus:
                sys.stdout.write(letter)
        print color.END

def print_clustalo_diffs(variants):
    fasta = clustalo.convert_list_to_fasta(variants)
    for item in clustalo.get_clustalo(fasta)[0]:
        print "\n".join(item)
    #print "".join(clustalo.get_clustalo(fasta)[0])

# print variants using different color to mark differences using zgrep and difference checking
if args.print_variant_diffs:
    try:
        variants = subprocess.check_output("zgrep %s.00.%s %s/%s.sglf.gz" % (tilePath, tileStep, args.keep, tilePath), shell=True) 
    except CalledProcessError:
        print "Collection not found or `zgrep` command not available. Finishing..."
    
    print "Annotated Variant Diffs (" + color.RED + "red" + color.END + " denotes a different base pair):"
    # split commandline output into each variant
    variants = variants.split('\n')[:-1]

    differentIndices = getDifferentIndices(variants) 

    print_clustalo_diffs(variants)