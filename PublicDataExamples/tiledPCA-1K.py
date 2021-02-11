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

a = '../../tileml'
b = '../../pgpml'
sys.path.insert(0, a)
sys.path.insert(0, b)

import tileutils as tileutils
import pgputils as pgputils

allfile = sys.argv[1]
infofile = sys.argv[2]
namesfile = sys.argv[3]
ancestryfile = sys.argv[4]

# Load Tile Data
Xtrain = np.load(allfile)
#Xtrain = Xtrain[:200,:]
Xtrain += 2  
# This will do this in-place and avoid making a copy
# Shift to 0 being Low Quality and 1 being Skipped Tiles by Adding 2

[m,n] = Xtrain.shape
pathdata = np.load(infofile)

# Create Vector of Original Index of Tile Position
idxOP = np.arange(Xtrain.shape[1])

# Quality Cutoff 100% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = tileutils.qualCutOff(Xtrain,pathdata,idxOP,1)

del Xtrain

# Removing Locations With Over 20 Tile Variants
idxMax = np.nanmax(XtrainPCA,axis=0) <= 20
XtrainPCA = XtrainPCA[:,idxMax]
pathdataPCA = pathdataPCA[idxMax]
idxOPPCA = idxOPPCA[idxMax]

# Calculate Top 3 PCA Components
[__, __, varvalsPCA]= tileutils.findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = tileutils.pcaComponents(XtrainPCA,varvalsPCA,3)
np.save("tiledPCA.npy", tiledPCA)

names = np.load(namesfile)
myfuncdecode = lambda x: x.decode("utf-8")
names = np.vectorize(myfuncdecode)(names)
names = names.tolist()

cleannames = pgputils.pgpCleanNames(names)
pcaNames = pd.DataFrame(np.column_stack([cleannames, names]),columns=['ID','Filename'])

# Setting Up Colors Based On Geographic Ancestries
ancestry1k = pd.read_csv('igsr_samples.tsv',sep='\t')
ancestry1k = ancestry1k.rename(columns={'Sample name': 'Sample', 'Population code': 'Population'})
ancestryMap = ancestry1k[['Sample','Population']]
ancestryMap['DataSource'] = '1K'
ancestryMap['ID'] = ancestry1k.Sample
ancestryMap['Region'] = ancestry1k.Population
ancestries = ancestryMap[['ID','Region','DataSource']]

z = pcaNames.merge(ancestries, how='left', on='ID')

z['Color'] = 'black'
idxAmerica1k = z['Region'].isin(['PUR', 'CLM','MXL','PEL'])
idxEurope1k = z['Region'].isin(['TSI','IBS','CEU','GBR','FIN'])
idxAfrica1k = z['Region'].isin(['LWK','MSL','GWD','YRI','ESN','ACB','ASW'])
idxEastAsia1k = z['Region'].isin(['KHV','CDX','CHS','CHB','JPT'])
idxSouthAsia1k = z['Region'].isin(['STU','ITU','BEB','GIH','PJL'])
z.Color[idxAmerica1k] = 'firebrick'
z.Color[idxEurope1k] = 'green'
z.Color[idxAfrica1k] = 'coral'
z.Color[idxEastAsia1k] = 'royalblue'
z.Color[idxSouthAsia1k] = 'blueviolet'

plt.figure
plt.scatter(tiledPCA[:,0],tiledPCA[:,1],c=z.Color,marker ="o",s=60,alpha = 0.8)

xlabel="PCA Component 1"
ylabel="PCA Component 2"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.savefig("test1KPCA.png",format='png')
