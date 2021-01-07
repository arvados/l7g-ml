#/usr/bin/python

import numpy as np
import sqlite3
import pandas as pd
import os
import sys
import re
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

a = '/data-sdd/cwl_tiling/l7g-ml/tileml'
b = '/data-sdd/cwl_tiling/l7g-ml/pgpml'
sys.path.insert(0, a)
sys.path.insert(0, b)

import tileutils as tileutils
import pgputils as pgputils 

ydatasource = sys.argv[1]
allfile = sys.argv[2]
infofile = sys.argv[3]
namesfile = sys.argv[4]
bloodtype = sys.argv[5]

# Load y Data as Dataframe (Data and IDs) 
dataBloodType = pgputils.yloadBlood(ydatasource,bloodtype)

# Load Tile Data
Xtrain = np.load(allfile)
# Add +2 so low quality tiles are represented by 0
Xtrain += 2 
pathdata = np.load(infofile)
names_file = open(namesfile, 'r') 
names = []
for line in names_file:
    names.append(line[:-1])

# Clean Names to get HUID
names = pgputils.pgpCleanNames(names)

# Match tiled genomes with y values by HUID
[Xtrain,y] = tileutils.syncTiles(dataBloodType,Xtrain,names)

# Create Vector of Original Index of Tile Position
idxOP = np.arange(Xtrain.shape[1])

# Remove XYM Chromosomes
[Xtrain,pathdata,idxOP]  = tileutils.removeXYM(Xtrain,pathdata,idxOP)

# Quality Cutoff 99% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.99)

# Calculate Top 20 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = tileutils.pcaComponents(XtrainPCA,varvalsPCA,20)

# Reshaping Matrix to Combine Phases  
[m,n] = Xtrain.shape
Xtrain = np.concatenate((Xtrain[:,0:n:2], Xtrain[:,1:n:2]),axis=0)
pathdata = pathdata[0:n:2]
idxOP = idxOP[0:n:2]

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= tileutils.findTileVars(Xtrain,pathdata,idxOP)

# Calculate OH Representation, Filtered using Pearson Chi2
[Xtrain, pathdataOH, varvals, idxOPOH] = tileutils.chiZygosity(Xtrain,pathdataOH,idxOPOH,varvals,y,5,.02)

print(Xtrain.shape)
print(pathdataOH.shape)
print(varvals.shape)
print(idxOPOH.shape)

# Combine Filtered OH Encoded Tiled Genomes and PCA Components
tiledPCA = csr_matrix(tiledPCA)
print(tiledPCA.shape)
Xtrain = hstack([Xtrain,tiledPCA],format='csr')
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
