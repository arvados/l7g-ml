# Tile Variant Searcher & RSID Lookup
### Kevin Fang, Curoverse Research, 2017-19
Python scripts that extract information from tiles.

Contains a script (`getTileVariants.py`) that retrieves tile step, path, phase, and variants from assembly files that and can also perform Clustal Omega alignments on the variants.

Contains another script (`getRsids.py`) to retrieve RSIDs for specific variants. 

#### Setup instructions to get running in Docker  
1. Make sure Docker is installed on your machine  
2. Clone and open this repository in the command line (`git clone https://github.com/kevin-fang/tile-searcher && cd tile-searcher`)  
3. Run `docker pull kfangcurii/tile-tools`  
4. Set up your Arvados API Tokens (skip this if you're running on an Arvados shell node)
5. Run `./setup.sh` to mount keep
6. Search for tiles using the following command: `./runInDocker.sh "<command line arguments here>"`, using command line arguments normally. For example, `./runInDocker.sh "./getTileVariants.py -i 1234 56789"` or `./runInDocker.sh "./getRsids.py -i 1234 -v 1"`.

#### Notes:
- If the docker build is not named `kfangcurii/tile-tools`, then change the docker image name in the shell script. Alternatively, build it yourself from the Dockerfile included in the `docker/` directory and change the docker name in the shell script
- Modify `config.yml` to reflect where the data is located. A sample configuration file is provided that represents the full tile set. 
- For `getTileVariants.py`, you can choose which config arguments to include depending on search requirements. Instructions are included in `config.yml` file.
- However, `getRsids.py` uses every feature of `getTileVariants.py`, so it _requires_ that the all the files requirements are specified in `config.yml`.

## Tile Variant Searching

The script `getTileVariants.py` is used to retrieve tile information, including step, path, phase, and variants from assembly files. Also contains a multiple sequence aligner to compare with all the variants (using Clustal Omega alignment).

Note that to run the ClustalO alignment at the end to check for variant differences, you must have the [Clustal Omega](http://www.clustal.org/omega/) package installed and have `clustalo` added to your path.

Deprecated: ability to use command line arguments (too cluttered). Instead, call `python getTileVariants.py -i 1234 67890` after setting `config.yml`.

## RSID Searching

The script `getRsids.py` is used to retrieve a list of possible RSIDs for SNPs/INDELS located in a variant of a genome. It compares a variant with the most common tile, and uses Mutalyzer 2 to locate the variations. 

A sample call to check for possible RSIDs on the first variant of tile 1234 would look like `./getRsids.py -i 1234 -v 1`.

## Tile Searching as a function

If you would like to use the output of the tile searching script in Python, you do not need to manually parse the output. `getTileVariants.py` is available as a function, callable from python. See the example below:  
```python
# import modules for tile variant searching
import getTileVariants, application

# search for index 1234, while suppressing processing output
tile_info = getTileVariants.tile_iteration(1234, suppress_output=True)

info_dict = tile_info.to_dict()

'''
info_dict looks like this:
{
    "chrom": "9",
    "path": "01c4",
    "position_end": "136140011",
    "position_start": "136139786",
    "step": "0369"
}
'''
```

There is more tile information available in the `tile_info` object that is returned. See below:   
```python
class Tile:
    def __init__(self, index):
        ...

        # tile path, step, and phase 
        self.path = None
        self.phase = None
        self.step = None

        # string representation of tile
        self.tile_str = None

        # tile variants
        self.variants = None

        # raw output from clustalo
        self.clustalo_output = None

        # calculated diffs from clustalo
        self.clustalo_diffs = None
        
        # raw text output from base pair location searching
        self.bp_output = None       

        # mapping from tile indexes to chromosomal locations
        self.diffs_map = None
```

## RSID Searching as a function

To use the RSID Searching from inside python, simply import it as a module. 

```python
# import module
import getRsids
# search for RSIDs for tile with index 1234, 1st variant.
# returns a dictionary with tile (variant) sequence, common sequence, variant, mutations, and index
info_dict = getRsids.rsid_search(1234, 1)

'''
info_dict looks like this:
{  
   "tile_sequence":"0000.00.0269.001+1,478d344b887e4dd7ed5d4af3c9cd8a76,atgccgctgcggggcacgttggtcctttccgcactcggggtccccggcggcctcacgcgtccgtgcagcggaggcttcctgagccccctggagagcctggcctgggcccgggtgtggagaccctcccgggctttcaatccgggcaggaggcagatggcagacaaaaaaaaaacataagagaaccgaattaggtgggtggcctgggtggacaaaagccttcttgacgccgggtggtcccaaaggcttctg",
   "variant":1,
   "mutations":{  
      "936633_936644delinsaaaaaaaaaaca":[  
         ("rs1017325702", "936636", "G", "C"),
         ("rs887210492",  "936643", "C", "A")
      ]
   },
   "common_sequence":"0000.00.0269.000+1,86945238e5aa7ad4ff4b407a3c442c46,atgccgctgcggggcacgttggtcctttccgcactcggggtccccggcggcctcacgcgtccgtgcagcggaggcttcctgagccccctggagagcctggcctgggcccgggtgtggagaccctcccgggctttcaatccgggcaggaggcagatggcagactcagcagtcacgtaagagaaccgaattaggtgggtggcctgggtggacaaaagccttcttgacgccgggtggtcccaaaggcttctg",
   "index":1234
}
'''
```

