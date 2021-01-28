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
print(np.amax(Xtrain))
print(np.amax(Xtrain,axis=0))

# Low Quality Represented by -1 
# Skipped Tiles Respresented by 0 
Xtrain += Xtrain  
idxN1  = Xtrain <= 0
Xtrain[idxN1] = 0

print(np.amax(Xtrain))
print(np.amax(Xtrain,axis=0))

#pathdata = np.load(infofile)
# Pathdata not available
[m,n] = Xtrain.shape

# Placeholder for Locations of Tiles
pathdata = np.zeros(n)

header_list = ["number","names","outputname"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

# Clean Names to get HUID
names = pgputils.pgpCleanNames(names)

# Match tiled genomes with y values by HUID
[Xtrain,y] = tileutils.syncTiles(dataBloodType,Xtrain,names)

# Create Vector of Original Index of Tile Position
idxOP = np.arange(Xtrain.shape[1])

# Remove XYM Chromosomes
#[Xtrain,pathdata,idxOP]  = tileutils.removeXYM(Xtrain,pathdata,idxOP)

# Quality Cutoff 99% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.99)

# Calculate Top 20 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = tileutils.pcaComponents(XtrainPCA,varvalsPCA,20)

# Reshaping Matrix to Combine Phases  
[m,n] = Xtrain.shape
test = np.equal(Xtrain[:,0:n:2],Xtrain[:,1:n:2])
print(test)
count = np.count_nonzero(test)
print(count)
Xtrain = np.concatenate((Xtrain[:,0:n:2], Xtrain[:,1:n:2]),axis=0)
pathdata = pathdata[0:n:2]
idxOP = idxOP[0:n:2]

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= tileutils.findTileVars(Xtrain,pathdata,idxOP)
print(Xtrain.shape)
print(varvals)
idxvar = varvals > 2
print(varvals[idxvar])

quit()

# Calculate OH Representation, Filtered using Pearson Chi2
print("inputs to zygosity")
print(Xtrain)
print(pathdataOH)
print(varvals)
print(idxOPOH)
print(y)
# (tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff):
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
