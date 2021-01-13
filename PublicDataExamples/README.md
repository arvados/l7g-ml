Examples on how to do machine learning with tiled data using public data (from PPGP, 1000 Genomes, etc)  

**Tiled Public Data**

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
* Includes:  Newly recalled 1000 Genomes using GrCh38 (broken into 2 sets for memory considerations)

Genomes with reference  hg19:
* Link for Download: https://su92l-4zz18-16ntyiehb807lrt.collections.su92l.arvadosapi.com/t=5387c6s20nzxs0rlu3xxcfco1gky8bi0qeyxv7fccq2zdr3aag/_/
* Includes: Harvard PGP, PGP Canada 

Tile Library:
* Full Tile Library for all public genomes that were tiled, recommend only downloading when necessary and/or getting access to cluster and running on collection directly
* https://su92l-4zz18-4lgzarfnuefpm4j.collections.su92l.arvadosapi.com/t=faw6d0cuxkymq23m94m4lz0lrbdoscq0giuc5td0owe7oae1v/_/ 

**Analysis Examples**

* Run using docker container created using dockerfile found here: l7g-ml/GLM/Dockerfile  

* Using python libaries for working with Tiled Data located in https://github.com/arvados/l7g-ml/blob/master/tileml/tileutils.py and https://github.com/arvados/l7g-ml/blob/master/pgpml/pgputils.py 
* Example Calls Below:

** Processing/Filtering Data for Model

Will create filtered 1-hot encoded X data and corresponding y data you can use for your modeling work (for a given Blood Type) where in the X matrix each tile variant is represented by 2 columns: if the tile variant is present in 1 (1st column) or 2 (2nd column) phases at that tile location. 

python loadingPGPBloodType_zygosity.py pgpdatabase.db tiledata.npy pathdata.npy allnames.txt A

** Running Modeling 

Will create a GLM model using Adaptive Lasso Regularization X and y data (X data is sparse matrix so given as values and row and column coordinates). Output will be non-zero coefficents and tile location information for "choosen tiles" that correspond to those non-zero coefficents for minimum and std of given metric and related plots 

Rscript ../GLM/src/ X.npy Xr.npy Xc.npy y.npy pathdataOH.npy oldpath.npy varvals.npy A class