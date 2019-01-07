# Tile Searcher
### Kevin Fang, 2017-18
Python scripts that allow for information to be extracted from tiles.

Contains a script (`getTileVariants.py`) that retrieves tile information, including step, path, phase, and variants from assembly files that and can also perform Clustal Omega alignments on the variants.

Contains another script (`getRsids.py`) to retrieve RSIDs for specific variants. 

A Dockerfile is also provided for easy dependency installation. To call it, run `./runInDocker.sh "<normal command line arguments here>"`. For example, `./runInDocker.sh "./getTileVariants -i 1234"`. You may have to change the docker image name in the shell script, though.

Note that to run the ClustalW alignment at the end to check for variant differences, you must have the [Clustal Omega](http://www.clustal.org/omega/) package installed and have `clustalo` added to your path.

To get up and running, set the Arvados API keys and run `./setup.sh` and then you can call `getTileVariants.py` with the appropriate arguments. Note that `getRsids.py` _requires_ that the all the files requirements are specified in `config.yml`.

Alternatively, you can change the file `config.yml` to specify features that the searcher should use and point to the necessary data files. A sample configuration file is provided.

To write the tile data to an output folder, include the argument `--write-to-file` when calling `getTileVariants.py` and it will create a folder with output.

A sample call for tile variants 1234 and 67890 can look something like `python getTileVariants.py -i 1234 67890 --tile-info ./tiling-files/hiq-pgp-info --location --assembly-fwi='./tiling-files/assembly.00.hg19.fw.fwi' --diff-indices --keep=./keep/by_id/su92l-4zz18-fkbdz2w6b25ayj3 --variant-diffs --base-pair-locations --assembly-gz='./tiling-files/assembly.00.hg19.fw.gz'`. 

Alternatively, if `config.yml` set, just call `python getTileVariants.py -i 1234 67890`.

List of commandline arguments for `getTileVariants.py`:  
- `-i` or `--index` lets you provide a list of indices for the tile searcher to run on.  
- `--tile-info` points to the location of the tile names. For the Harvard Personal Genome Project, it is called `hiq-pgp-info`.  
- `--location` is included if the script should output the tile path, step, and phase.  
- `--variant-diffs` is included if the script should output the ClustalW alignment, showing the differences between the tile variants.  
- `--base-pair-locations` is included if the script should output base pair locations of the tile.  
- `--diff-indices` is included if the script should output the indices where variants are different.  
- `--write-to-file` is included if the script should write the output to a file instead. By default, it writes to a folder called `output`.

### Deprecated:

This repository also contains a browser frontend written in React.js and a with a REST API backend in node.js that calls the Python script for easier use, as well as a simple Android client in `clients/TileInfoApp/` to query the API.

To start the web server, install npm and run `cd clients && npm i && npm start`. This will install all the Arvados dependencies, as well as start the backend and frontend and open it in a local browser.
