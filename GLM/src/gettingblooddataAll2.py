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
import re

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

print("==== Extracting Blood Type %s... ====" %bloodtype)
y = df2[bloodtype].values #for blood type A to start

print("Y size: ", y.size)


#nnz = np.count_nonzero(Xtrain, axis=0)
#fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])

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

nnz = np.count_nonzero(tiledata,axis=0)
fracnnz = np.divide(nnz.astype(float),tiledata.shape[0])

# Don't keep X,Y and M data

tile_path = np.trunc(pathdata/(16**5))
idx1 = tile_path >= 863
idx2 = tile_path <= 810
idx3 = idx2

pathdata = pathdata[idx3]
tiledata = tiledata[:,idx3]
idxOP = idxOP[idx3]

# PCA components

idxKeepPCA = fracnnz[idx3] >= 0.99
tiledataPCA = tiledata[:,idxKeepPCA]

varvalsPCA = np.full(50*tiledataPCA.shape[1],np.nan)
nx=0

varlistPCA = []

for j in range(0,tiledataPCA.shape[1]):
    u = np.unique(tiledataPCA[:,j])
    varvalsPCA[nx:nx+u.size] = u
    nx = nx + u.size
    varlistPCA.append(u)

varvalsPCA = varvalsPCA[~np.isnan(varvalsPCA)]

print(varvalsPCA.shape)

enc = OneHotEncoder(sparse=True, dtype=np.uint16)

XtrainPCA = enc.fit_transform(tiledataPCA)

print(XtrainPCA.shape)

to_keepPCA = varvalsPCA > 1

idkTKPCA = np.nonzero(to_keepPCA)
idkTKPCA = idkTKPCA[0]

XtrainPCA = XtrainPCA[:,idkTKPCA]
XtrainPCA = XtrainPCA.todense()
pca = PCA(n_components=20)
XtrainPCA = pca.fit_transform(XtrainPCA)

scaler = StandardScaler()
XtrainPCA= scaler.fit_transform(XtrainPCA)
[m,n] = tiledata.shape

# Reshaping matrix to account for phases
tiledata = np.concatenate((tiledata[:,0:n:2], tiledata[:,1:n:2]),axis=0)
pathdata = pathdata[0:n:2]
idxOP = idxOP[0:n:2]

# Only keeping data that has less than 10% missing data

#idxKeep = fracnnz[idx3] >= 0.9
nnzRS = np.count_nonzero(tiledata,axis=0)
fracnnzRS = np.divide(nnzRS.astype(float),tiledata.shape[0])
idxKeep = fracnnzRS >= 0.9
tiledata = tiledata[:,idxKeep]

print("Encoding in 1-hot...")
print("Determing new path and varval vectors...")

print(tiledata.shape)

def foo(col):
   u = np.unique(col)
   nunq = u.shape
   return nunq

invals = np.apply_along_axis(foo, 0, tiledata)
invals = invals[0]

varvals = np.full(50*tiledata.shape[1],np.nan)
nx=0

varlist = []
for j in range(0,tiledata.shape[1]):
     u = np.unique(tiledata[:,j])
     varvals[nx:nx+u.size] = u
     nx = nx + u.size
     varlist.append(u)

varvals = varvals[~np.isnan(varvals)]

print(varvals.shape)
pathdataOH = np.repeat(pathdata[idxKeep], invals)
oldpath = np.repeat(idxOP[idxKeep],invals)

print(pathdataOH.shape)
print(oldpath.shape)
print(varvals.shape)

print("Running the Encoder...")

ny = tiledata.shape[1]

print(ny)

nnz = np.count_nonzero(tiledata,axis=0)

print("==== One-hot Encoding Data... ====")

#tiledata_filename = "tiledata.npy"
#np.save(tiledata_filename, tiledata)

data_shape = tiledata.shape[1]

parts = 20
idx = np.linspace(0,data_shape,num=parts).astype('int')
Xtrain2 = csr_matrix(np.empty([m, 0]))
Xtrain2hom = csr_matrix(np.empty([m, 0]))
pidx = np.empty([0,],dtype='bool')
pidxhom = np.empty([0,],dtype='bool')

for ichunk in np.arange(0,parts-1):
#for ichunk in np.arange(25,parts-1):
    print(ichunk)
    print("==== Loading in First Chunk... ====")
    min_idx = idx[ichunk]
    max_idx = idx[ichunk+1]
    print(min_idx)
    print(max_idx)
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)
    Xtrain = enc.fit_transform(tiledata[:,min_idx:max_idx])
    print(Xtrain.shape)

    Xdouble =  Xtrain[0:m,:] + Xtrain[m:2*m,:]
    idx2 = Xdouble >= 2

    datahom = Xdouble.data
    [rhom,chom] = Xdouble.nonzero()
    idx3 = datahom == 2
    datahom = datahom[idx3]
    rhom = rhom[idx3]
    chom = chom[idx3]

    Xtrainhom = csr_matrix((datahom, (rhom, chom)), Xdouble.shape)
    Xtrainhom[idx2] = 1

    datahet = Xdouble.data
    [rhom,chom] = Xdouble.nonzero()
    idx4 = datahet == 1
    datahet = datahet[idx4]
    rhom = rhom[idx4]
    chom = chom[idx4]

    Xtrainhet = csr_matrix((datahet, (rhom, chom)), Xdouble.shape)

    [chi2val,pval] = chi2(Xtrainhet, y)
    print(np.amax(pval))
    print(np.amin(pval))

    pidxchunk = pval <= 0.02
    Xchunk = Xtrainhet[:,pidxchunk]
    print(Xchunk.shape)
    [chi2val2,pval2] = chi2(Xtrainhom, y)
    print(np.amax(pval2))
    print(np.amin(pval2))

    pidxchunk2 = pval2 <= 0.02
    Xchunkhom = Xtrainhom[:,pidxchunk2]
    print(Xchunkhom.shape)

    pidx = np.concatenate((pidx,pidxchunk),axis=0)
    pidxhom = np.concatenate((pidxhom,pidxchunk2),axis=0)

    print(pidx.shape)
    print(pidxhom.shape)
    Xtrain2 = hstack([Xtrain2,Xchunk],format='csr')
    Xtrain2hom = hstack([Xtrain2hom,Xchunkhom],format='csr')

#quit()
pathdataOHhet = pathdataOH[pidx]
oldpathhet = oldpath[pidx]
varvalshet = varvals[pidx]

pathdataOHhom = pathdataOH[pidxhom]
oldpathhom = oldpath[pidxhom]
varvalshom = varvals[pidxhom]

pathdataOH = np.concatenate((pathdataOHhet,pathdataOHhom),axis=0)
oldpath = np.concatenate((oldpathhet,oldpathhom),axis=0)
varvals = np.concatenate((varvalshet,varvalshom),axis=0)

print(pathdataOH.shape)
print(oldpath.shape)
print(varvals.shape)

Xtrain = hstack([Xtrain2,Xtrain2hom],format='csr')
to_keep = varvals > 2
idkTK = np.nonzero(to_keep)
idkTK = idkTK[0]

Xtrain = Xtrain[:,idkTK]
pathdataOH = pathdataOH[idkTK]
oldpath = oldpath[idkTK]
varvals = varvals[idkTK]

XtrainPCA = csr_matrix(XtrainPCA)
Xtrain = hstack([Xtrain,XtrainPCA],format='csr')

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

