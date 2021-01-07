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

a = '../../tileml'
b = '../../pgpml'
sys.path.insert(0, a)
sys.path.insert(0, b)

import tileutils as tileutils
import pgputils as pgputils 

ydatasource = sys.argv[1]
allfile = sys.argv[2]
namesfile = sys.argv[3]
bloodtype = sys.argv[4]

# Load y Data as Dataframe (Data and IDs) 
dataBloodType = pgputils.yloadBlood(ydatasource,bloodtype)

# Load Tile Data
Xtrain = np.load(allfile)

# Low Quality Represented by -1 
# Skipped Tiles Respresented by 0 
idxNeg = Xtrain < 0
Xtrain[idxNeg] = -1
Xtrain = Xtrain + 1

#pathdata = np.load(infofile)
# Pathdata not available
[m,n] = Xtrain.shape

# Placeholder for Locations of Tiles
pathdata = np.zeros(n)

#names_file = open(namesfile, 'r') 
#names = []
#for line in names_file:
#    names.append(line[:-1])

header_list = ["number","names"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

# Clean Names to get HUID
names = pgputils.pgpCleanNames(names)

# Match tiled genomes with y values by HUID
[Xtrain,y] = tileutils.syncTiles(dataBloodType,Xtrain,names)

# Create Vector of Original Index of Tile Position
idxOP = np.arange(Xtrain.shape[1])

# Randomize Phases
Xtrain = tileutils.randomizePhase(Xtrain)

# Remove XYM Chromosomes
#[Xtrain,pathdata,idxOP]  = tileutils.removeXYM(Xtrain,pathdata,idxOP)

# Quality Cutoff 99% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.99)

# Calculate Top 20 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = tileutils.pcaComponents(XtrainPCA,varvalsPCA,20)

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= tileutils.findTileVars(Xtrain,pathdata,idxOP)
print(Xtrain.shape)

# Calculate OH Representation, Filtered using Pearson Chi2
[Xtrain, pathdataOH, varvals, idxOPOH] = tileutils.chiPhased(Xtrain,pathdataOH,idxOPOH,varvals,y,5,.02)

# Combine Filtered OH Encoded Tiled Genomes and PCA Components
tiledPCA = csr_matrix(tiledPCA)
Xtrain = hstack([Xtrain,tiledPCA],format='csr')

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
