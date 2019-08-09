
from sklearn import preprocessing
import numpy as np
import pandas as pd
import scipy
import collections
import os
import sys

from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from scipy.sparse import save_npz

from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder


surveyData = sys.argv[1]
allfile = sys.argv[2]
infofile = sys.argv[3]
namesfile = sys.argv[4]
color = sys.argv[5]  #use to get either blue or brown?

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

get_name = lambda full_name: full_name[45:53]
names = map(get_name, names)

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

print("==== End Of New Code for Eye Color ====")

# allfile = tiled_data_dir + 'all.npy'
# infofile = tiled_data_dir + 'all-info.npy'
print("==== Loading Big Files... ====")
Xtrain = np.load(allfile)
Xtrain += 2 # All -2 so makes it to 0
pathdata = np.load(infofile)
print("==== Done Loading Big Files... ====")
idx = nameIndices
Xtrain = Xtrain[idx,:] 

min_indicator = np.amin(Xtrain, axis=0)
max_indicator = np.amax(Xtrain, axis=0)

sameTile = min_indicator == max_indicator
skipTile = ~sameTile #this is the inverse operator for boolean

idxOP = np.arange(Xtrain.shape[1])
Xtrain = Xtrain[:, skipTile]
newPaths = pathdata[skipTile]
idxOP = idxOP[skipTile]
# only keep data with less than 10% missing data
nnz = np.count_nonzero(Xtrain, axis=0)
fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])
idxKeep = fracnnz >= 0.9
Xtrain = Xtrain[:, idxKeep]

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
pathdataOH = np.repeat(newPaths[idxKeep], invals)
# used later to find the original location of the path from non one hot encode
oldpath = np.repeat(idxOP[idxKeep], invals)

randomize_idx = np.arange(len(y))
np.random.shuffle(randomize_idx)
tiledata = Xtrain[randomize_idx,:]
y = y[randomize_idx]
print("random y: ", y)

nnz = np.count_nonzero(tiledata,axis=0)

print("==== One-hot Encoding Data... ====")

data_shape = tiledata.shape[1]

parts = 4
idx = np.linspace(0,data_shape,num=parts).astype('int')
Xtrain2 = csr_matrix(np.empty([tiledata.shape[0], 0]))
pidx = np.empty([0,],dtype='bool')

for i in range(0,parts-1):
    min_idx = idx[i]
    max_idx = idx[i+1]
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)
    Xtrain = enc.fit_transform(tiledata[:,min_idx:max_idx])
    [chi2val,pval] = chi2(Xtrain, y)
    pidxchunk = pval <= 0.02
    Xchunk = Xtrain[:,pidxchunk]
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