# Download to Arvados

## Info

Bash script can be depricated by updating the CWL step to use command line args

### How to run

Run on Arvados node:

   ``` bash
   arvados-cwl-runner --api=containers --disable-reuse --no-wait --project-uuid [project uuid] download-wf.cwl yml/[your specified yml]
   ```

## Extras

### Extras are experimental and have not been tested.  

for paired fastq's:

   ``` bash
   cwl-runner --local downloadPaired.cwl --bashScript downloadPaired.sh --urlFile 2-paired.txt
   ```

   ``` bash
   cwl-runner --debug downloadPaired.cwl --bashScript downloadPaired.sh --urlFile 2-paired.txt
   ```

for md5sum'ing:

   ``` bash
   cwl-runner --local md5sum.cwl md5sum.yml
   ```
