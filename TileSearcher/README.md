# Tile Searcher
A Python script that prints tile information given tile libraries, `getTileVariants.py`.

To get up and running, set the Arvados API keys and run `./setup.sh` and then you can call `getTileVariants.py`

This repository also contains a browser frontend written in React.js and a with a REST API backend in node.js that calls the Python script for easier use, as well as a simple Android client in `clients/TileInfoApp/` to query the API.

To start the web server, install npm and run `cd clients && npm i && npm start`. This will install all the Arvados dependencies, as well as start the backend and frontend and open it in a local browser

The Android client is very barebones (and the JSON requests are currently broken) but to run it, import the project into Android Studio and build it.
