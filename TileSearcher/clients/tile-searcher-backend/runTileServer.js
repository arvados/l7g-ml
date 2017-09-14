#!/usr/bin/env nodejs
var express = require("express")
var app = express()
var cors = require("cors")
var PythonShell = require("python-shell")

app.use(cors())
app.get('/tile', (req, res) => {
	console.log("url: " + req.url)
	index = req.query.index
	json = req.query.json
	get_base_locs = req.query.get_base_locs
	get_variants = req.query.get_variants
	get_name = req.query.get_name
	get_diff_indices = req.query.get_diff_indices
	get_all = req.query.all

	if (get_all) {
		get_base_locs = 'true'
		get_variants = 'true'
		get_name = 'true'
		get_diff_indices = 'true'
	}
	console.log("Finding tile for index: " + index + ", json status: " + json)
	if (json == 'true') {
		json = true
		res.setHeader('Content-Type', 'text/json')
	} else {
		json = false
		res.setHeader('Content-Type', 'text/html')
	}
	var options = {
		mode: 'text',
		scriptPath: '../../',
		args: ['--hiq-info=../../tiling-files/hiq-pgp-info', '--index=' + index, '--assembly-fwi=../../tiling-files/assembly.00.hg19.fw.fwi', '--assembly-gz=../../tiling-files/assembly.00.hg19.fw.gz', '--keep=../../keep/by_id/su92l-4zz18-fkbdz2w6b25ayj3']
	}
	if (get_base_locs == 'true') {
		options.args.push('-b')
	}
	if (get_variants == 'true') {
		options.args.push('-v')
	}
	if (get_name == 'true') {
		options.args.push('-l')
	}
	if (get_diff_indices == 'true') {
		options.args.push('-vdi')
	}

	var results = ""
	var shell = new PythonShell('getTileVariants.py', options)
	shell.on('message', (message) => {
		if (json) {
			results = results + message + '\n'
		} else {
			results = results + message + '<br/>'
		}
	})
	shell.on('error', (err) => {
		res.write("An error occured. Please send the following information to the server host:\n" + err)
		console.log(err)
	})
	shell.on('close', () => {
		resultsObj = new Object()
		resultsObj.index = index 
		resultsObj.search = []
		if (results.includes("Tile location")) {
			resultsObj.search.push("Tile Location")
		}
		if (results.includes("Base pair location")) {
			resultsObj.search.push("Base Pair Location")
		}
		if (results.includes("Variant Information")) {
			resultsObj.search.push("Variant Information")
		}
		if (results.includes("Tile Variant Diff Indices")) {
			resultsObj.search.push("Tile Variant Diff Indices")
		}

		resultsArr = results.split('\n')
		for (var i = 0; i < resultsArr.length; i++) {
			if (resultsArr[i].includes("Tile Path")) {
				resultsObj.tile_path = resultsArr[i].substring(11)
			} else if (resultsArr[i].includes("Tile Step")) {
				resultsObj.tile_step = resultsArr[i].substring(11)
			} else if (resultsArr[i].includes("Tile Phase")) {
				resultsObj.tile_phase = resultsArr[i].substring(12)
			} else if (resultsArr[i].includes("Base pair location")) {
				resultsObj.base_pair_start = resultsArr[i + 1]
				resultsObj.base_pair_end = resultsArr[i + 2]
			} else if (resultsArr[i].includes("hg19")) {
				resultsObj.name = resultsArr[i].replace(/\t/g, ' ') 
			} else if (resultsArr[i].includes("Variant Diff Indices")) {
				resultsObj.different_indices = resultsArr[i].substring(22)
			} else if (resultsArr[i].includes("Variant Information")) {
				resultsObj.variants = []
				i += 1
				while (resultsArr[i].includes('.00.')) {
					resultsObj.variants.push(resultsArr[i])
					i += 1
				}
			}
		}


		if (json) {
			var resultsJson = JSON.stringify(resultsObj).replace(/\\t/g, '');
			res.write(resultsJson)
			console.log("Finished searching")
		} else {
			res.write(results)
			console.log("Finished searching")
		}
		res.end();
	})
})

const port = 8080
app.listen(port);

console.log("Listening on port: " + port)
