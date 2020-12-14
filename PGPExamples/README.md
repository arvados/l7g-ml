Examples on how to do machine learning with tiled data using public data from PGP (Personal Genome Project)

Run using docker container created using dockerfile found here: l7g-ml/GLM/Dockerfile  
Tiled PGP Data Available Here:
Database of PGP Phenotype Data Available Here:


Example Calls Below:
Will create filtered 1-hot encoded X data and corresponding y data you can use for your modeling work (for a given Blood Type) where in the X matrix each tile variant is represented by 2 columns: if the tile variant is present in 1 (1st column) or 2 (2nd column) phases at that tile location. 

python loadingPGPBloodType_zygosity.py pgpdatabase.db tiledata.npy pathdata.npy allnames.txt A

