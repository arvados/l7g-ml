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
import hashlib

a = '/data-sdd/cwl_tiling/l7g-ml/TileModules'
sys.path.insert(0, a)

from tileUtils import *

untapdb = sys.argv[1]
allfile = sys.argv[2]
infofile = sys.argv[3]
namesfile = sys.argv[4]
bloodtype = sys.argv[5]

print("==== Command Line Arguments Received... =====")

# Access PGP database and create dataframe

conn = sqlite3.connect(untapdb)
c = conn.cursor()
c.execute('SELECT * FROM demographics')
rows = c.fetchall()
colnames = []

for i in c.description:
    colnames.append(i[0])
data = pd.DataFrame(rows, columns=colnames)
conn.close()

dataBloodType = data[['human_id','blood_type']]
dataBloodType = dataBloodType.replace('', np.nan, inplace=False)
dataBloodType = dataBloodType.dropna(axis=0, inplace=False)

#Encodes blood type to integers
dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
dataBloodType['O'] = dataBloodType['blood_type'].str.contains('O',na=False).astype(int)
dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)

print("==== Loading Tiled Genome Files... ====")

Xtrain = np.load(allfile)
# Add +2 so low quality tiles are represented by 0
Xtrain += 2 
pathdata = np.load(infofile)
names_file = open(namesfile, 'r') 
names = []
for line in names_file:
    names.append(line[:-1])

# Removing strings not related participant ID
names1 = [i.split('/')[-1] for i in names]
names2 = [i.replace('filtered_','') for i in names1]
names3 = [i.replace('.haplotypeCalls.er.raw','') for i in names2]
names4 = [i.replace('_cg_data_ASM','') for i in names3]
names5 = [i.replace('data_','') for i in names4]
names6 = [i.replace('.cgf','') for i in names5]
names7 = [i.split('_var')[0] for i in names6]
names8 = [i.split('_GS')[0] for i in names7]
names9 = [i.split('_lcl')[0] for i in names8]
names10 = [i.split('_blood')[0] for i in names9]
names11 = [i.split('_buffy')[0] for i in names10]
names12 = [i.split('_noHLA')[0] for i in names11]
names13 = [re.sub('_(S1|sorted).genome','',i) for i in names12]
names14 = [re.sub('_.+-portable', '',i) for i in names13]
names = names14

# Simple lambda function to return if the input is a string
isstr = lambda val: isinstance(val, str)

dataBloodType.human_id = dataBloodType.human_id.str.lower()
results = []
for name in names:
    results.append(name.lower())

df_names = pd.DataFrame(results,columns={'Sample'})
df_names['Number'] = df_names.index

df2 = df_names.merge(dataBloodType,left_on = 'Sample', right_on='human_id', how='inner')
del dataBloodType
df2['blood_type'].value_counts()
del df_names
idx = df2['Number'].values

Xtrain = Xtrain[idx,:] 
y = df2[bloodtype].values 

# Create Vector of Original Index of Tile Position
idxOP = np.arange(Xtrain.shape[1])

# Randomize Phases
Xtrain = randomizePhase(Xtrain)

# Removing XYM Chromosomes
[Xtrain,pathdata,idxOP]  = removeXYM(Xtrain,pathdata,idxOP)

# Quality Cutoff 99% for PCA
[XtrainPCA, pathdataPCA, idxOPPCA] = qualCutOff(Xtrain,pathdata,idxOP,0.99)

# Calculate Top 20 PCA Components
[__, __, varvalsPCA]= findTileVars(XtrainPCA,pathdataPCA,idxOPPCA)
tiledPCA = pcaComponents(XtrainPCA,varvalsPCA,20)

# Quality Cutoff 90% for Filter and Further ML
[Xtrain, pathdata, idxOP] = qualCutOff(Xtrain,pathdata,idxOP,0.90)
[pathdataOH, idxOPOH, varvals]= findTileVars(Xtrain,pathdata,idxOP)

# Calculate OH Representation, Filtered using Pearson Chi2
[Xtrain, pathdataOH, varvals, idxOPOH] = chiPhased(Xtrain,pathdataOH,idxOPOH,varvals,y,5,.02)

# Combine Filtered OH Encoded Tiled Genomes and PCA Components
XtrainPCA = csr_matrix(XtrainPCA)
Xtrain = hstack([Xtrain,XtrainPCA],format='csr')

print("==== Saving Outputs... ====")

# Save Final Outputs
np.save('y.npy', y)
np.save('pathdataOH.npy', pathdataOH)
np.save('oldpath.npy', idxOPOH)
np.save('varvals.npy', varvals)
scipy.sparse.save_npz("X.npz", Xtrain)
