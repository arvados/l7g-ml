#/usr/bin/python

# **** get_Data.py ****
# * CREATED FOR: Curii Research
# * AUTHOR: Owen Webb
# * PURPOSE: To process tiled numpy arrays and run a chi2 filter on it 
# * USE: Used prior to ML algorithm Ex: SVM_Trial.py
# * INPUT FILES: untap.db ; all.npy ; all-info.npy ; names.npy
# * OUTPUT FILES: blood_type_A_chi2_no_augmentation_X.npy ; blood_type_A_chi2_no_augmentation_y.npy ;
#                 blood_type_A_chi2_no_augmentation_pathdataoh.npy ; blood_type_A_chi2_no_augmentation_oldpath.npy ; 
#                 blood_type_A_chi2_no_augmentation_varvals.npy

import numpy as np
import sqlite3
import pandas as pd
import os
import sys

import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from scipy.sparse import save_npz

from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.preprocessing import StandardScaler

import hashlib


untapdb = sys.argv[1]
allfile = sys.argv[2]
infofile = sys.argv[3]
namesfile = sys.argv[4]
#if choice.lower() == "blood":
bloodtype = sys.argv[5]

#Use to turn off the chi2 filter
chi2filter = True

# Unnecesary if cwl is run
# untapdb = '/data-sdd/owebb/untap.db'
# allfile = '/home/owebb/keep/by_id/su92l-j7d0g-4mnq9juobvg0qwy/CopyOfTileDataNumpy/all.npy'
# infofile = '/home/owebb/keep/by_id/su92l-j7d0g-4mnq9juobvg0qwy/CopyOfTileDataNumpy/all-info.npy'
# namesfile = '/home/owebb/keep/by_id/su92l-j7d0g-4mnq9juobvg0qwy/CopyOfTileDataNumpy/names.npy'
# bloodtype = 'A'

print("==== Command Line Arguments Received... =====")

# Go get the data from the database as and create dataframe

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

print("==== Loading Files... ====")
Xtrain = np.load(allfile)

Xtrain += 2 # All -2 so makes it to 0
pathdata = np.load(infofile)
names_file = open(namesfile, 'r') #not a "pickeled" file, so must just read it and pull data out of it
names = []

for line in names_file:
    names.append(line[:-1])

names1 = [i.split('/')[-1] for i in names]
names2 = [i.replace('filtered_','') for i in names1]
names3 = [i.replace('.cgf','') for i in names2]
names4 = [i.split('_var')[0] for i in names3]
names5 = [i.split('_GS')[0] for i in names4]
names6 = [i.split('_lcl')[0] for i in names5]
names7 = [i.split('_blood')[0] for i in names6]
names8 = [i.split('_buffy')[0] for i in names7]
names = names8

# simple lambda function to return if the input is a string
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

idxOP = np.arange(Xtrain.shape[1])

nnz = np.count_nonzero(Xtrain, axis=0)
fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])

# Unphasing Data

[m,n] = Xtrain.shape

for ix in range(m):
   n20 = int(n/4)
   ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
   keepa = Xtrain[ix,ieven]
   keepb = Xtrain[ix,ieven+1]
   Xtrain[ix,ieven] = keepb
   Xtrain[ix,ieven+1] = keepa
   del keepa,keepb

# Don't keep X,Y and M data

tile_path = np.trunc(pathdata/(16**5))
idx1 = tile_path >= 863
idx2 = tile_path <= 810
idx3 = idx2

pathdata = pathdata[idx3]
Xtrain = Xtrain[:,idx3]
idxOP = idxOP[idx3]

# Only keeping data that has less than 10% missing data

idxKeep = fracnnz[idx3] >= 0.9
Xtrain = Xtrain[:, idxKeep]

print("==== Extracting Blood Type %s... ====" %bloodtype)
y = df2[bloodtype].values #for blood type A to start

print("Y size: ", y.size)

# save information about deleted missing/spanning data
varvals = np.full(50 * Xtrain.shape[1], np.nan)
nx = 0
varlist = []
for j in range(0, Xtrain.shape[1]):
    u = np.unique(Xtrain[:,j])
    varvals[nx : nx + u.size] = u
    nx = nx + u.size
    varlist.append(u)

varvals = varvals[~np.isnan(varvals)]

def foo(col):
    u = np.unique(col)
    nunq = u.shape
    return nunq

invals = np.apply_along_axis(foo, 0, Xtrain)
invals = invals[0]

# used later to find coefPaths
pathdataOH = np.repeat(pathdata[idxKeep], invals)
# used later to find the original location of the path from non one hot encode
oldpath = np.repeat(idxOP[idxKeep], invals)

tiledata = Xtrain
nnz = np.count_nonzero(tiledata,axis=0)

print("==== One-hot Encoding Data... ====")

# removed randomization here
data_shape = tiledata.shape[1]

parts = 4
idx = np.linspace(0,data_shape,num=parts).astype('int')
Xtrain2 = csr_matrix(np.empty([tiledata.shape[0], 0]))
pidx = np.empty([0,],dtype='bool')

for i in range(0,parts-1):
    min_idx = idx[i]
    max_idx = idx[i+1]
    enc = OneHotEncoder(sparse=True, dtype=np.uint16, categories='auto')
    Xtrain = enc.fit_transform(tiledata[:,min_idx:max_idx])
    [chi2val,pval] = chi2(Xtrain, y)
    print(pval.size)
    print(Xtrain.size)
    if chi2filter == True:
        pidxchunk = pval <= 0.02
    else:
        pidxchunk = pval <= 1
    Xchunk = Xtrain[:,pidxchunk]
    print(Xchunk)
    print(Xtrain2)
    pidx=np.concatenate((pidx,pidxchunk),axis=0)
    if i == 0:
        Xtrain2 = Xchunk
    else:
        Xtrain2= hstack([Xtrain2,Xchunk],format='csr')

pathdataOH = pathdataOH[pidx]
oldpath = oldpath[pidx]
varvals = varvals[pidx]
Xtrain = Xtrain2
to_keep = varvals > 2 
idkTK = np.nonzero(to_keep)
idkTK = idkTK[0]

Xtrain = Xtrain[:,idkTK]
pathdataOH = pathdataOH[idkTK]
oldpath = oldpath[idkTK]
varvals = varvals[idkTK]

#XtrainPCA = csr_matrix(XtrainPCA)
#Xtrain = hstack([Xtrain,XtrainPCA],format='csr')

print(Xtrain.shape)
print(y.shape)
print(pathdataOH.shape)
print(oldpath.shape)
print(varvals.shape)

X_filename = "X.npz"
y_filename = "y.npy"
np.save(y_filename, y)
np.save('pathdataOH.npy', pathdataOH)
np.save('oldpath.npy', oldpath)
np.save('varvals.npy', varvals)
scipy.sparse.save_npz(X_filename, Xtrain)


print("==== Done ====")
