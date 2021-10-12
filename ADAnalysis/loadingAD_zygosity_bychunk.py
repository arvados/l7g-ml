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

a = './tileml'
b = './adml'
sys.path.insert(0, a)
sys.path.insert(0, b)

from tileml import tileutils as tileutils
from adml import adutils as adutils

ydatasource = sys.argv[1]
allfile = sys.argv[2]
namesfile = sys.argv[3]
phenotype = sys.argv[4]
annotationsfile = sys.argv[5]

# Load y Data as Dataframe (Data and IDs) 
dataAD = adutils.yloadAD(ydatasource)

# Load Tile Data
Xtrain = np.load(allfile)

# Low Quality Represented by -1 
# Skipped Tiles Respresented by 0 
Xtrain += 1 
idxN1  = Xtrain <= 0
Xtrain[idxN1] = 0

# Determine Shape of Tiled Matrix Chunk
[m,n] = Xtrain.shape

# Placeholder Locations of Tiles
pathdata = np.zeros(n)

header_list = ["number","names","outputname"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

# Clean Names to get HUID
names = adutils.cleanNamesAD(names)

# Match tiled genomes with y values by HUID
[y,pheno] = adutils.syncTilesAD(dataAD,names)

# Get tile tag offset
# Read first line of annotation file and subtract to get offset values

dflabels = ["tag","col","tilevar","annotation"] 
annotations = pd.read_csv(annotationsfile, nrows=1,header=0,names=dflabels)
offset = annotations.tag.values - annotations.col.values
offset = offset[0]

# Create Vector of Original Index of Tile Position
idxn = Xtrain.shape[1]/2
idxrange = np.arange(idxn)
idxrange = idxrange 
idxOP = np.empty(Xtrain.shape[1])
idxOP[0::2] = idxrange
idxOP[1::2] = idxrange

# Reshaping Matrix to Combine Phases  
[m,n] = Xtrain.shape
Xtrain = np.concatenate((Xtrain[:,0:n:2], Xtrain[:,1:n:2]),axis=0)
idxOP = idxOP[0:n:2]
pathdata = idxOP[0:n:2] + offset

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= tileutils.findTileVars(Xtrain,pathdata,idxOP)

# Calculate OH Representation, Filtered using Pearson Chi2
# (tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff):
[Xtrain, pathdataOH, varvals, idxOPOH, zygosity] = tileutils.chiZygosity(Xtrain,pathdataOH,idxOPOH,varvals,y,4,.05,zygosityreturn=True)

# Removing NaN values from y
idxNN = np.logical_not(np.isnan(y))
y = y[idxNN]

# Combine Filtered OH Encoded Tiled Genomes and PCA Components
[Xr,Xc] = Xtrain.nonzero()
print(Xr.shape)
Xtrain = Xtrain.data
print(Xtrain.shape)
print(y.shape)
print(pathdataOH.shape)

# Get "chunk" number from file name
chunk = re.search('\.(\d\d\d\d)\.',annotationsfile)
chunk = chunk.group(1)

# Output names
yfile = 'y' + chunk + '.npy'
pathdatafile = 'pathdataOH' + chunk + '.npy'
oldpathfile = 'oldpath' + chunk + '.npy'
varvalsfile  = 'varvals' + chunk + '.npy'
Xfile = 'X' + chunk + '.npy'
Xrfile = 'Xr' + chunk + '.npy'
Xcfile = 'Xc' + chunk + '.npy'
zygosityfile = 'zygosity' + chunk + '.npy'

# Save Final Outputs
np.save(yfile, y)
np.save(pathdatafile, pathdataOH)
np.save(oldpathfile, idxOPOH)
np.save(varvalsfile, varvals)
np.save(Xfile, Xtrain)
np.save(Xrfile, Xr)
np.save(Xcfile, Xc)
np.save(zygosityfile,zygosity)
