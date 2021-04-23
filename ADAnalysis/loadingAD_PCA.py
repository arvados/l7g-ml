# usr/bin/python

import numpy as np
import sqlite3
import pandas as pd
import os
import sys
import re
import csv
import glob
import scipy.sparse

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
allfiledir = sys.argv[2]
namesfile = sys.argv[3]
phenotype = sys.argv[4]

# Load y Data as Dataframe (Data and IDs) 
dataAD = adutils.yloadAD(ydatasource)

# Placeholder for Locations of Tiles
header_list = ["number","names","outputname"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

# Clean Names to get HUID
names = adutils.cleanNamesAD(names)

# Load Tile Data
filesearch = allfiledir + "/*.npy"
filelist = glob.glob(filesearch)

idxoffset = 0

allXPCA = np.empty([len(names),0])
allidx = np.empty([0,])
allpathdataPCA = np.empty([0,])

for file in filelist:
    Xtrain = np.load(file)
    [m,n] = Xtrain.shape

    # Placeholder for Locations of Tiles
    pathdata = np.zeros(n)

    # Low Quality Represented by -1 
    # Skipped Tiles Respresented by 0 
    Xtrain += 1 
    idxN1 = Xtrain <= 0
    Xtrain[idxN1] = 0

    # Create Vector of Original Index of Tile Position
    idxn = Xtrain.shape[1]/2
    idxrange = np.arange(idxn)
    idxOP = np.empty(Xtrain.shape[1])
    idxOP[0::2] = idxoffset + idxrange
    idxOP[1::2] = idxoffset + idxrange
    array_length = len(idxOP)
    last_element = idxOP[array_length - 1]
    idxoffset = last_element

    print("Quality Cutoff 99% for PCA")
    # Quality Cutoff 99% for PCA
    [XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,1)
    allXPCA = np.hstack((allXPCA,XtrainPCA))
    allidx = np.hstack((idxOPPCA,allidx))
    allpathdataPCA = np.hstack((allpathdataPCA,pathdataPCA))

print("Calculating PCA")
# Calculate Top 20 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(allXPCA,allpathdataPCA,allidx)
tiledPCA = tileutils.pcaComponents(allXPCA,varvalsPCA,20)

del allXPCA
del varvalsPCA

# Save Final Outputs
np.save("tiledPCA.npy", tiledPCA)
df.to_csv("labels.csv",index=False,header=False)
