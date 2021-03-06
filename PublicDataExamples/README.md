<h1>Public Tiled Data Analysis Examples</h1>   

<h2>Tiled Public Data</h2>

Explaination of Data Formats:
* In this repo: TileDataFormat.md 
* https://github.com/arvados/l7g-ml/blob/master/PublicDataExamples/TileDataFormat.md

Genomes with reference GrCh37: 
* Link for Download: https://su92l-4zz18-eheqmei0wm6k9e9.collections.su92l.arvadosapi.com/t=35g3tu8lo4hcgp1b11bjwaw22hw5ufks2oumv71v1gciw52aso/_/
* Includes: Harvard PGP (CGI), Simons Diversity, and 1K Genomes (old CGI)

Genomes with reference GrCh38:
* Link for Download: https://su92l-4zz18-7ld2fd87dgi8gr1.collections.su92l.arvadosapi.com/t=5nplveba410soklxc5ndausxw31gjemx3bcgddot06ch6l3amx/_/
* Includes: Subset of 1K Genomes for testing, UK PGP 

Full Set of 1K Genomes with reference GrCh38:
* Link for Download (set1): https://su92l-4zz18-ex19fny5l1vmdw9.collections.su92l.arvadosapi.com/t=clwmbdk8vlt93zw304s413wfg928fgryzivlz2ga6g14f91rf/_/
* Link for Download (set2): https://su92l-4zz18-k1txafpxx1f3c6a.collections.su92l.arvadosapi.com/t=242pijuhbgiiu8rxbfuxrjfroolnqhwtfrxs6gam8w1elux51u/_/
* Includes:  Newly recalled 1000 Genomes using GrCh38 (broken into 2 sets for memory considerations)

Genomes with reference hg19:
* Link for Download: https://su92l-4zz18-16ntyiehb807lrt.collections.su92l.arvadosapi.com/t=5387c6s20nzxs0rlu3xxcfco1gky8bi0qeyxv7fccq2zdr3aag/_/
* Includes: Harvard PGP, PGP Canada 

Tile Library:
* Full Tile Library for all public genomes that were tiled, recommend only downloading when necessary and/or getting access to cluster and running on collection directly (~115 GB)
* https://su92l-4zz18-4g601pj0w917v3s.collections.su92l.arvadosapi.com/t=3cgpa03bn3wo9sjiz5e9o5nd2scz4daor4q2zodrt5ytgdzc8r/_/ 

PGP Database:
* sqlite database of PGP data, can use for getting phenotype informations
* Location: https://collections.su92l.arvadosapi.com/c=9070d59896b003686089a25e79aba3b5-3558/_/html/index.html?disposition=inline

Ancestry File for 1000 Genomes Samples:
* tsv indicating ancestries and other information about 1000 Genomes samples
* Location: https://www.internationalgenome.org/data-portal/sample  (click Download List) 

References (Assembly Files):
* Assembly files are tiling specific files that map each tile location on a reference. 
* hg38: https://su92l-4zz18-x6f2kzfo8ok5rir.collections.su92l.arvadosapi.com/t=4kqpr8b9avkremkw3sz667x3wi1uta9sm6krnq6rjzu1ck5jc/_/
* GrCh37: https://su92l-4zz18-fpzdhvygctybb98.collections.su92l.arvadosapi.com/t=2wfv3ygsn8icpfpt02oclwbelxtdd8n9y0o551y6mxtanvpnm5/_/

<h2>Analysis Examples</h2>

Note these examples do require a reasonably large amount of memory.  I have verified they can run on a linux machine with 128 GiB of RAM. They may require ~1 hr to run depending on your system.

* Run models using docker container created using dockerfile found here: l7g-ml/GLM/Dockerfile  
* Run annotation using docker container created using dockerfile found here: /l7g-ml/Dockerfiles/get_hgvs

* Using python libaries for working with Tiled Data located in https://github.com/arvados/l7g-ml/blob/master/tileml/tileutils.py and https://github.com/arvados/l7g-ml/blob/master/pgpml/pgputils.py 

<h3>Classification Example</h3>

* Uses Harvard PGP Data

* <h4>Step 1: Processing/Filtering Data for Model</h4> </li>

* Will create filtered 1-hot encoded X data and corresponding y data you can use for your modeling work (for a given Blood Type) where in the X matrix each tile variant is represented by 2 columns: if the tile variant is present in 1 (1st column) or 2 (2nd column) phases at that tile location.</li>

* python loadingPGPBloodType_zygosity.py pgpdatabase.db tiledata.npy pathdata.npy allnames.txt A
* python loadingPGPBloodType_zygosity.py PGPDATABASE TILEDGENOMES TILEINFO SAMPLENAMES BLOODTYPE

* <h4>Step 2: Running Modeling</h4> 
* Will create a GLM model using Adaptive Lasso Regularization X and y data (X data is sparse matrix so given as values and row and column coordinates). Output will be non-zero coefficents and tile location information for "chosen tiles" that correspond to those non-zero coefficents for minimum and std of given metric and related plots
* Rscript ../GLM/src/glmnetAdaptive.r X.npy Xr.npy Xc.npy y.npy pathdataOH.npy oldpath.npy varvals.npy A class
* Rscript ../GLM/src/glmnetAdaptive.r filteredtiles_nonzerovals filteredtiles_rows filteredtiles_columns classdata tileinfo oldtileinfo tilevariantvalues bloodtypeforclassification metricforglm

* <h4>Step 3: Annotating Tile Variants</h4>
* In the output files from Step2, you will get a path and step and variant for tiles with non-zero coefficents. You can use the following to look up these to get the corresponding HGVS annotation.  You must convert tile and step to the hex representation since that is how they are stored in the tile library. If a step and path is marked as NA, it means that it is a PCA component and not a tile. Note: For this you will need to use a different docker container.  The dockerfile located here: /l7g-ml/Dockerfiles/get_hgvs .  It will install everything including placing the needed python code in the usr/bin. Tile ID is give by path.00.step.variant+span.  Span is usually 1. The output of Step 2 is tile variant +2, so subtract 2 before entering into the tile searcher. We add 2 so that all tile variants are over 0.  

* python ./usr/bin/tilesearcher.py 01c4.00.0389.000+1 hg38.fa.gz tilelibdirectory /assembly.00.hg38.fw.gz

Ouput may look like the following:
NC_000009.12:g.133273813C>T   -> HGVS annotation for https://www.ncbi.nlm.nih.gov/snp/rs505922

If Output is empty (NC_000009.12:g.=) - it means there is no variant present.  It may indicate variant is on the most common tile and lack of that variant is what it is using.  You can check it by checking the 0th tile variant to see if a variant is present

* python ./usr/bin/tilesearcher.py TILEID REF TILELIB ASSEMBLY

<h3>PCA Example</h3>

* This example was build to do the PCA of the 1000 Genomes Data
* Will caclulate top 3 PCA components and plot them colored by geographic ancestry
* python tiledPCA-1K.py all-GrCh38_1k_set1 all-info-GrCh38_1K_set2 names-GrCh38_1K_set2 igsr_samples.tsv
* python tiledPCA-1K.py tileddata tileinfo samplenames geographicalancestryinfo
