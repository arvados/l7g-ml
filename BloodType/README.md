Using machine learning and the Arvados Lightning project, we are able to predict blood type using tiled PGP data.  

Our latest machine learning model 1-hot encodes the data, applies a Pearson chi^2 filter, and then performs classification using an SVM with an l1 regularization (found in folder chi2). 

This project is reliant on the following Python libraries: `scikit-learn`, `pandas`, `matplotlib`, `numpy`, `scipy`. In addition, the tile searches to find tiles of importance cannot be run on non-UNIX machines as it requires the system `grep` and `cat` commands.
 
