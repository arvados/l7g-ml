
# Download SGDP to Arvados

## Info

Simons Genome Diversity Project data is primarily hosted on Seven Bridges Cancer Cloud, and because of how the download URLs are constructed, they posed a number of problems with accessing and downloading.

To mediate the downloading, constructing a pipeline that includes `wget -O [filename] [url in single-quotes] && md5sum -b [filename] > [filename].md5sum` required additional scripting to form arrays for scattering over pairs of filenames and URLs.

### How to run

Supply a txt file in `src` containing URLs and run `src/get_arrays.py`

Additional flags and help for `get_arrays.py`:

   ``` bash
   usage: get_arrays [-h] [-s] [-p] [-m] [-f] [URL_LIST]

   Get arrays of URLs and filenames from listing of URLs.

   positional arguments:
      URL_LIST            Input URL list file via stdin

   optional arguments:
      -h, --help          show this help message and exit
      -s, --singletest    Generates a yml for a single step for CWL testing
      -p, --printsamples  Prints the first 5 items in the constructed arrays
      -m, --minitest      Generates a yml containing the first 5 items in arrays
      -f, --filenames     creates a txt of all filenames in a single file
   ```

Run on Arvados node:

   ``` bash
   arvados-cwl-runner --api=containers --no-wait --project-uuid su92l-some-projectuuid download-wf.cwl yml/manifest.yml
   ```

## Extras  

To validate if bgzipped files test OK (via `gzip -tv`) navigate to `sgdp/gz-verify`:

   ``` bash
   arvados-cwl-runner --api=containers --no-wait --project-uuid su92l-some-projectuuid gz-validate-wf.cwl yml/sgdp.yml
   ```

This workflow generates a `*.vfy` extension, simply for ease of locating these files.

Run `src/getstatus.py` to generate a directory listing and status.

(note: `bgzip` does not have a test function, and many bgzipped files will also contain a message`gzip: ./file.gz: extra field of 6 bytes ignored`, so `getstatus.py` ignores these lines)

For a cleaner format of validation, run `src/gzanalyze.py` after running `getstatus.py` along with the `filenames.txt` that can be created with `sgdp/src/get_arrays.py`

