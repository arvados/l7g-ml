# Tile Searcher
A Python script that prints tile information given tile libraries, `getTileVariants.py`.

Note that to run the ClustalW alignment at the end to check for variant differences, you must have the [Clustal Omega](www.clustal.org/omega) package installed and have `clustalo` added to your path.

To get up and running, set the Arvados API keys and run `./setup.sh` and then you can call `getTileVariants.py` with the appropriate arguments. 

A sample call for tile variants 1234 and 67890 can look something like `python getTilesNew.py -i "1234 67890" --hiq-info ./tiling-files/hiq-pgp-info --get-location --assembly-fwi='./tiling-files/assembly.00.hg19.fw.fwi' --get-diff-indices --keep=./keep/by_id/su92l-4zz18-fkbdz2w6b25ayj3 --print-variant-diffs --get-base-pair-locations --assembly-gz='./tiling-files/assembly.00.hg19.fw.gz'
`. 

If you are using the PGP and wish to easily search for a tile location there, run `./sampleGetTile 1234 67890` to quickly locate tiles 1234 and 67890.

This repository also contains a browser frontend written in React.js and a with a REST API backend in node.js that calls the Python script for easier use, as well as a simple Android client in `clients/TileInfoApp/` to query the API.

To start the web server, install npm and run `cd clients && npm i && npm start`. This will install all the Arvados dependencies, as well as start the backend and frontend and open it in a local browser