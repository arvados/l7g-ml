#usr/bin/python
import os
os.environ.get('DISPLAY','')
import matplotlib as mpl
mpl.use('Agg')      # This line must come before importing pyplot
import matplotlib.pyplot as plt
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

allfile = "/home/sarah/keep/by_id/su92l-4zz18-cpw0i3z7wery77o/matrix.npy" 
#allfile = sys.argv[1]

# Load Tile Data
Xtrain = np.load(allfile)

# Low Quality Represented by 0 
# Skipped Tiles Respresented by -1 

Xtrain = Xtrain + 1

idxN1 = Xtrain == 0 
idxN2 = Xtrain == 1

Xtrain[idxN1] = 1
Xtrain[idxN2] = 0

[m,n] = Xtrain.shape

# Placeholder for Locations of Tiles
pathdata = np.zeros(n) 
idxOP = np.arange(Xtrain.shape[1])

# Quality Cutoff 100% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,1)

# Removing Locations With Over 20 Tile Variants
idxMax = np.nanmax(XtrainPCA,axis=0) <= 20
XtrainPCA = XtrainPCA[:,idxMax]
pathdataPCA = pathdataPCA[idxMax]
idxOPPCA = idxOPPCA[idxMax]

# This is just a hack for now to test memory (taking ~1/2 the data)
XtrainPCA = XtrainPCA[:,:5000000]
pathdataPCA = pathdataPCA[:5000000]
idxOPPCA = idxOPPCA[:5000000]

# Calculate Top 3 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = tileutils.pcaComponents(XtrainPCA,varvalsPCA,3)

plt.figure
plt.scatter(tiledPCA[:,0],tiledPCA[:,1])
plt.savefig("testPCA.png",format='png')
