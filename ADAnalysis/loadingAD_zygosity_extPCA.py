# usr/bin/python

import numpy as np
import sqlite3
import pandas as pd
import os
import sys
import re
import csv
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

#a = '../tileml'
#b = '../adml'
a = './tileml'
b = './adml'
sys.path.insert(0, a)
sys.path.insert(0, b)

from tileml import tileutils as tileutils
from adml import adutils as adutils
#import tileutils as tileutils
#import adutils as adutils

ydatasource = sys.argv[1]
allfile = sys.argv[2]
namesfile = sys.argv[3]
phenotype = sys.argv[4]
PCAfile = sys.argv[5]
PCAnamesfile = sys.argv[6]

# Load y Data as Dataframe (Data and IDs) 
dataAD = adutils.yloadAD(ydatasource)
#print(dataAD)
#quit()

# Load Tile Data
Xtrain = np.load(allfile)

# Load External PCA Data
tiledPCA = np.load(PCAfile)

# Low Quality Represented by -1 
# Skipped Tiles Respresented by 0 
Xtrain += 1 
idxN1  = Xtrain <= 0
Xtrain[idxN1] = 0

# Pathdata not available
[m,n] = Xtrain.shape

# Placeholder for Locations of Tiles
pathdata = np.zeros(n)

header_list = ["number","names","outputname"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

dfPCA = pd.read_csv(PCAnamesfile, names=header_list)
PCAnames = dfPCA["names"].tolist()

# Clean Names to get HUID
names = adutils.cleanNamesAD(names)
PCAnames = adutils.cleanNamesAD(PCAnames)

print(names)
print(PCAnames)

# Match tiled genomes with y values by HUID
[y,pheno,tiledPCA] = adutils.syncTilesADwPCA(dataAD,names,PCAnames,tiledPCA)

# Match tile genomes with external PCA values

# Create Vector of Original Index of Tile Position
idxn = Xtrain.shape[1]/2
idxrange = np.arange(idxn)
idxOP = np.empty(Xtrain.shape[1])
idxOP[0::2] = idxrange
idxOP[1::2] = idxrange

print("Reshaping Matrix")
# Reshaping Matrix to Combine Phases  
[m,n] = Xtrain.shape
Xtrain = np.concatenate((Xtrain[:,0:n:2], Xtrain[:,1:n:2]),axis=0)
pathdata = pathdata[0:n:2]
idxOP = idxOP[0:n:2]

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= tileutils.findTileVars(Xtrain,pathdata,idxOP)

# Calculate OH Representation, Filtered using Pearson Chi2
# (tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff):
[Xtrain, pathdataOH, varvals, idxOPOH, zygosity] = tileutils.chiZygosity(Xtrain,pathdataOH,idxOPOH,varvals,y,10,.05,zygosityreturn=True)

# Removing NaN values from y
idxNN = np.logical_not(np.isnan(y))
y = y[idxNN]
pheno = pheno[idxNN]
tiledPCA = tiledPCA[idxNN,:]

# Combine Filtered OH Encoded Tiled Genomes and PCA Components
tiledPCA = csr_matrix(tiledPCA)
print(tiledPCA.shape)
Xtrain = hstack([Xtrain,tiledPCA],format='csr')
Xtrain = hstack([Xtrain,pheno],format='csr')
print(Xtrain.shape)
[Xr,Xc] = Xtrain.nonzero()
print(Xr.shape)
Xtrain = Xtrain.data
print(Xtrain.shape)

# Save Final Outputs
np.save('y.npy', y)
np.save('pathdataOH.npy', pathdataOH)
np.save('oldpath.npy', idxOPOH)
np.save('varvals.npy', varvals)
np.save("X.npy", Xtrain)
np.save("Xr.npy", Xr)
np.save("Xc.npy", Xc)
np.save("zygosity.npy",zygosity)
