Examples on how to do machine learning with tiled data using public data from PGP (Personal Genome Project)

Run using docker container created using dockerfile found here: l7g-ml/GLM/Dockerfile  

Tiled PGP Data Available Here:
Brief Explaination of Tiled Data:
Database of PGP Phenotype Data Available Here:


Example Calls Below:

Processing/Filtering Data for Model --

Will create filtered 1-hot encoded X data and corresponding y data you can use for your modeling work (for a given Blood Type) where in the X matrix each tile variant is represented by 2 columns: if the tile variant is present in 1 (1st column) or 2 (2nd column) phases at that tile location. 

python loadingPGPBloodType_zygosity.py pgpdatabase.db tiledata.npy pathdata.npy allnames.txt A

Running Modeling ---

Will create a GLM model using Adaptive Lasso Regularization X and y data (X data is sparse matrix so given as values and row and column coordinates). Output will be non-zero coefficents and tile location information for "choosen tiles" that correspond to those non-zero coefficents for minimum and std of given metric and related plots 

Rscript ../GLM/src/ X.npy Xr.npy Xc.npy y.npy pathdataOH.npy oldpath.npy varvals.npy A class
