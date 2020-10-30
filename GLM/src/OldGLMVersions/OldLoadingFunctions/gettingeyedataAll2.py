
from sklearn import preprocessing
import numpy as np
import pandas as pd
import scipy
import collections
import os
import sys
import re

from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from scipy.sparse import save_npz

from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.preprocessing import StandardScaler

surveyData = sys.argv[1]
allfile = sys.argv[2]
infofile = sys.argv[3]
namesfile = sys.argv[4]
color = sys.argv[5]

includeHazel = False

# read names that have provided survey eye color data
columns = ['name', 'timestamp', 'id', 'blood_type', 'height', 'weight', 'hw_comments', 'left', 'right', 'left_desc', 'right_desc', 'eye_comments', 'hair', 'hair_desc', 'hair_comments', 'misc', 'handedness']

# pgp eye color data from survey
#surveyData = pd.read_csv("/data-sdd/owebb/l7g-ml/EyeColor/eye_color_data/PGP-Survey.csv", names=columns, na_values=['nan', '', 'NaN'])

# names of the pgp participants
surveyData = pd.read_csv(surveyData, names=columns, na_values=['nan', '', 'NaN'])
surveyNames = np.asarray(surveyData['name'].values.tolist())

# tiled_data_dir = "/data-sdd/owebb/keep/by_id/su92l-4zz18-b8rs5x7t6gry16k/

names_file = open(namesfile,'r')
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

eye_color = collections.namedtuple("EyeColor", ['left', 'right'])

# lookup a name in the survey data and return a tuple of the eye colors
def getData(name, surveyData, includeHazel=False):
    for index, row in surveyData.iterrows():
        if row['name'] == name:
            if not includeHazel:
                return eye_color(row['left'], row['right'])
            else:
                if isstr(row['left_desc']) and isstr(row['right_desc']):
                    if 'azel' in row['left_desc'] or 'azel' in row['right_desc']:
                        return None
                return eye_color(row['left'], row['right'])


# list of tuples for index and name with eye color data (idx, name)
nameEyeMap = []
namePair = collections.namedtuple("NamePair", ['index', 'name'])

# dictionary of left and right eye colors with respective name, i.e., {"huID": 12}
leftEyeMap = {}
rightEyeMap = {}

existingNames = []
# loop through pgpNames and add eye color to maps, making sure not to add the same name twice
for i, name in enumerate(names):
    if name in surveyNames and name not in existingNames:
        existingNames.append(name)
        # change `includeHazel=True` to include hazel in the training/testing data.
        eyeData = getData(name, surveyData, includeHazel=includeHazel)
        if eyeData == None:
            pass
        elif isstr(eyeData.left) and isstr(eyeData.right):
            nameEyeMap.append(namePair(i, name))
            leftEyeMap[name] = eyeData.left
            rightEyeMap[name] = eyeData.right

# create lists containing the known eye color names and the unknown eye colors.
nameIndices, correspondingNames = [], []
for pair in nameEyeMap:
    nameIndices.append(pair.index)
    correspondingNames.append(pair.name)

# convert dictionaries to lists 
leftEyeList = []
rightEyeList = []
# nametuple looks like (index, name)
for _, name in nameEyeMap:
    if isstr(leftEyeMap[name]):
        leftEyeList.append(leftEyeMap[name])
    if isstr(rightEyeMap[name]):
        rightEyeList.append(rightEyeMap[name])

blueOrNot = lambda color: 0 if int(color) > 13 else 1
leftEyeList = map(blueOrNot, leftEyeList)

y = np.array(leftEyeList)
print(y.shape)
y_filename = "y.npy"
np.save(y_filename, y)

#quit()
print("==== End Of New Code for Eye Color ====")

tiledata = np.load(allfile)
print(tiledata.shape)
tiledata += 2 # -2 to 0, 0 is missing data
pathdata = np.load(infofile)
print("==== Done Loading Big Files... ====")
idx = nameIndices
tiledata = tiledata[idx,:] 
idxOP = np.arange(tiledata.shape[1])

#nnz = np.count_nonzero(tiledata,axis=0)
#fracnnz = np.divide(nnz.astype(float),tiledata.shape[0])

# Unphasing Data

[m,n] = tiledata.shape

for ix in range(m):
   n20 = int(n/4)
   ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
   keepa = tiledata[ix,ieven]
   keepb = tiledata[ix,ieven+1]
   tiledata[ix,ieven] = keepb
   tiledata[ix,ieven+1] = keepa
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

#nnz = np.count_nonzero(tiledata,axis=0)
#fracnnz = np.divide(nnz.astype(float),tiledata.shape[0])

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
