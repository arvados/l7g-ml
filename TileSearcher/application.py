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

        # information that will be filled laterj
        self.path = None
        self.phase = None
        self.step = None
        self.tile_str = None
        self.variants = None
        self.clustalo_output = None
        self.clustalo_diffs = None
        self.bp_output = None
        self.diffs_map = None

    def to_dict(self):
        info_dict = {}
        info_dict['step'] = self.step
        info_dict['path'] = self.path
        info_dict['chrom'] = self.tile_str.split(":")[1].replace("chr", "")
        tile_location = self.bp_output.split('\n')
        info_dict['position_start'] = tile_location[0].split('\t')[1].strip()
        info_dict['position_end'] = tile_location[1].split('\t')[1].strip()
        return info_dict

    def __str__(self):
        return "Tile {} information:\n{}\nPath: {}\nStep: {}\nPhase: {}".format(
            self.index, self.tile_str, self.path, self.step, self.phase)


class TileApplication:
    # initialize False defaultdicts for functionality and data
    def __init__(self):
        self.functionality = defaultdict(lambda: False)
        self.data = defaultdict(lambda: False)
        self.tiles = []

    def verify_args(self, args):
        # verify that the arguments needed are given
        if args.location is None and args.assembly_fwi is None:
            raise Exception(
                "Cannot get tile location without --assembly-fwi argument.")
        if args.variant_diffs is None and args.sglf is None:
            raise Exception(
                "Cannot get variant diffs without --sglf argument.")
        if args.diff_indices is None and args.sglf is None:
            raise Exception("Cannot get diff indices without --sglf argument.")
        if args.base_pair_locations and args.assembly_gz is None:
            raise Exception(
                "Cannot get base pair locations without --assembly-gz argument.")

    def verify_config(self, config_args):
        if "diff_indices" in config_args['features'] and not config_args['sglf']:
            raise Exception(
                "Cannot get diff indices without sglf in configuration file.")
        if "location" in config_args['features'] and not config_args['assembly_fwi']:
            raise Exception(
                "Cannot get location without assembly_fwi in configuration file.")
        if "base_pair_locations" in config_args['features'] and not config_args['assembly_gz']:
            raise Exception(
                "Cannot get base pair locations without assembly_gz in configuration file.")
        if "variant_diffs" in config_args['features'] and not config_args['assembly_gz']:
            raise Exception(
                "Cannot get variant diffs without sglf in configuration file.")

    def set_config_data_args(self, config_args):
        self.data['tile_info'] = config_args['tile_info']
        self.data['assembly_gz'] = config_args['assembly_gz']
        self.data['assembly_fwi'] = config_args['assembly_fwi']
        self.data['sglf'] = config_args['sglf']

    def set_functionality_from_config(self, config_args):

        # parse functionality from input and save to dictionary
        self.functionality['location'] = 'location' in config_args['features']
        self.functionality['variant_diffs'] = 'variant_diffs' in config_args['features']
        self.functionality['diff_indices'] = 'diff_indices' in config_args['features']
        self.functionality['base_pair_locations'] = 'base_pair_locations' in config_args['features']

    def set_functionality(self, args):
        # parse functionality from input and save to dictionary
        if args.location is None:
            self.functionality['location'] = True
        if args.variant_diffs is None:
            self.functionality['variant_diffs'] = True
        if args.diff_indices is None:
            self.functionality['diff_indices'] = True
        if args.base_pair_locations is None:
            self.functionality['base_pair_locations'] = True

    def set_tile_indices(self, args):
        for idx in args.indices:
            self.tiles.append(Tile(idx))

    def set_data_args(self, args):
        # save data to dictionary in application
        self.data['tile_info'] = args.tile_info
        self.data['assembly_gz'] = args.assembly_gz
        self.data['assembly_fwi'] = args.assembly_fwi
        self.data['sglf'] = args.sglf

    def get_functionality(self):
        # create a string that displays what the application will calculate
        base_str = ""
        if self.functionality['base_pair_locations']:
            base_str += "Finding Tile Location, "
        if self.functionality['print_variant_diffs']:
            base_str += "Printing Variant Differences (ClustalW), "
        if self.functionality['diff_indices']:
            base_str += "Finding Indices of Variant Differences, "
        if self.functionality['base_pair_locations']:
            base_str += "Retrieving Base Pair Locations"

        return base_str

    def test_command_availability(self):
        # tests the following commands based on input: bgzip, zgrep, clustalo,
        # cat
        if self.functionality['base_pair_locations']:
            test_command(
                ['bgzip', '-help'], "bgzip is not installed or is not available in the PATH.")
        if self.functionality['location']:
            test_command(['cat', '--help'],
                         "cat is not available on this system.")
        if self.functionality['location'] or self.functionality['variant_diffs'] or self.functionality['diff_indices']:
            test_command(
                ['zgrep', '--help'], "zgrep is not installed or is not available in the PATH")
        if self.functionality['variant_diffs'] or self.functionality['diff_indices']:
            test_command(['clustalo', '--help'],
                         "clustalo is not installed or is not avaialble in the PATH.")
