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

<h2>Analysis Examples</h2>

Note these examples do require a reasonably large amount of memory.  I have verified they can run on a linux machine with 128 GiB of RAM. They may require ~1 hr to run depending on your system.

* Run using docker container created using dockerfile found here: l7g-ml/GLM/Dockerfile  

* Using python libaries for working with Tiled Data located in https://github.com/arvados/l7g-ml/blob/master/tileml/tileutils.py and https://github.com/arvados/l7g-ml/blob/master/pgpml/pgputils.py 

<h3>Classification Example</h3>

* Uses Harvard PGP Data

* Step 1: Processing/Filtering Data for Model</li>

* Will create filtered 1-hot encoded X data and corresponding y data you can use for your modeling work (for a given Blood Type) where in the X matrix each tile variant is represented by 2 columns: if the tile variant is present in 1 (1st column) or 2 (2nd column) phases at that tile location.</li>

* python loadingPGPBloodType_zygosity.py pgpdatabase.db tiledata.npy pathdata.npy allnames.txt A
* python loadingPGPBloodType_zygosity.py databaseforPGP tiledgenomes tileinfo samplenames bloodtypeforclassification

* Step 2: Running Modeling 
* Will create a GLM model using Adaptive Lasso Regularization X and y data (X data is sparse matrix so given as values and row and column coordinates). Output will be non-zero coefficents and tile location information for "choosen tiles" that correspond to those non-zero coefficents for minimum and std of given metric and related plots
* Rscript ../GLM/src/ X.npy Xr.npy Xc.npy y.npy pathdataOH.npy oldpath.npy varvals.npy A class
* Rscript filteredtiles_nonzerovals filteredtiles_rows filteredtiles_columns classdata tileinfo oldtileinfo tilevariantvalues bloodtypeforclassification metricforglm

<h3>PCA Example</h3>

* This example was build to do the PCA of the 1000 Genomes Data
* Will caclulate top 3 PCA components and plot them colored by geographic ancestry
* python tiledPCA-1K.py all-GrCh38_1k_set1 all-info-GrCh38_1K_set2 names-GrCh38_1K_set2 igsr_samples.tsv
* python tiledPCA-1K.py tileddata tileinfo samplenames geographicalancestryinfo
