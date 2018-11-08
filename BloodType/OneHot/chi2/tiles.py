# Force Keras to use the CPU
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# NOTE: This code block silences memory allocation warnings, which are empirically annoying.
# It's a good idea to have it on regularly when you're making changes.
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Our imports
from keras.models import Sequential
from keras.layers import Dense
import sqlite3
import pickle
from datetime import datetime
from OneHotEncoding import encode

# old imports
from sklearn.svm import LinearSVC
from sklearn import preprocessing
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import collections

import os
import glob
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import sklearn
from sklearn import svm
from sklearn.feature_selection import chi2
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import OneHotEncoder
import argparse 
from sklearn.utils.validation import assert_all_finite
from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from matplotlib import rcParams
import scipy.sparse

# # Change this to load more pgp data at the peril of your RAM.
# NUM_SAMPLES = -1

# # change for whether to exclude or include hazel
# excludeHazel = True

# # file name of saved classifier
# fileName = 'svc.pkl'

# # read names that have provided survey eye color data
# columns = ['name', 'timestamp', 'id', 'blood_type', 'height', 'weight', 'hw_comments', 'left', 'right', 'left_desc', 'right_desc', 'eye_comments', 'hair', 'hair_desc', 'hair_comments', 'misc', 'handedness']

# # pgp eye color data from survey
# #print "Loading data..."
# surveyData = pd.read_csv("PGP-Survey.csv", names=columns, na_values=['nan', '', 'NaN'])

# # names of the pgp participants
# surveyNames = np.asarray(surveyData['name'].values.tolist())

# # load numpy array of tiled PGP data

# pgpdata = np.load("all.npy", 'r')
# # Delete some of the data.
# #pgpdata = np.delete(pgpdata, np.s_[NUM_SAMPLES::], 0)
# #print("deleted")
# #print(pgpdata.shape)
# #pgpdata = np.fromfile("pgpstuff/tile_data/all.npy", dtype='char', count=2000)

# # load numpy array of names and keep only the huID
# pgpNames = []
# with open("names.npy") as fo:
#     for line in fo:
#         name = line[-29:-21]
#         pgpNames.append(name)

# # simple lambda function to return if the input is a string
# isstr = lambda val: isinstance(val, str)

# eye_color = collections.namedtuple("EyeColor", ['left', 'right'])

# # lookup a name in the survey data and return a tuple of the eye colors
# def getData(name, surveyData, excludeHazel=False):
#     for index, row in surveyData.iterrows():
#         if row['name'] == name:
#             if not excludeHazel:
#                 return eye_color(row['left'], row['right'])
#             else:
#                 if isstr(row['left_desc']) and isstr(row['right_desc']):
#                     if 'azel' in row['left_desc'] or 'azel' in row['right_desc']:
#                         return None
#                 return eye_color(row['left'], row['right'])


# # list of tuples for index and name with eye color data (idx, name)
# nameEyeMap = []
# namePair = collections.namedtuple("NamePair", ['index', 'name'])

# # dictionary of left and right eye colors with respective name, i.e., {"huID": 12}
# leftEyeMap = {}
# rightEyeMap = {}

# existingNames = []

# # loop through pgpNames and add eye color to maps, making sure not to add the same name twice
# for i, name in enumerate(pgpNames):
#     if name in surveyNames and name not in existingNames:
#         existingNames.append(name)
#         # change `excludeHazel=True` to include hazel in the training/testing data.
#         eyeData = getData(name, surveyData, excludeHazel=excludeHazel)
#         if eyeData == None:
#             pass
#         # TODO (AL): This is a hack to take a reduced number of samples to avoid memory errors.
#         # Make it more scalable when it's deployed.
#         elif isstr(eyeData.left) and isstr(eyeData.right):
#             #and i < NUM_SAMPLES:
#             nameEyeMap.append(namePair(i, name))
#             leftEyeMap[name] = eyeData.left
#             rightEyeMap[name] = eyeData.right

# # create lists containing the known eye color names and the unknown eye colors.
# nameIndices, correspondingNames = [], []
# for pair in nameEyeMap:
#     nameIndices.append(pair.index)
#     correspondingNames.append(pair.name)
# knownData = pgpdata[nameIndices]
# unknownData = np.delete(pgpdata, nameIndices, axis=0)
# print(knownData.shape)
# #knownData = preprocessing.scale(knownData.astype('double'))

# # convert dictionaries to lists
# leftEyeList = []
# rightEyeList = []
# # nametuple looks like (index, name)
# for _, name in nameEyeMap:
#     if isstr(leftEyeMap[name]):
#         leftEyeList.append(leftEyeMap[name])
#     if isstr(rightEyeMap[name]):
#         rightEyeList.append(rightEyeMap[name])

# blueOrNot = lambda color: 0 if int(color) > 13 else 1
# leftEyeList = list(map(blueOrNot, leftEyeList))

# leftEyeList = np.array(leftEyeList)
# np.save("eye_color_labels.npy", leftEyeList)
# # One Hot encode.
# tiledata = knownData + 2
# pathdata = np.load("all-info.npy", 'r')
#encode(tiledata, pathdata)


# =========START of SARAH'S CODE=============
encoded = np.load("train_data.npy")
blood_types = np.load("blood_types.npy")
zeros = np.argwhere(blood_types == 0)
ones = np.argwhere(blood_types == 1)
keep_idx = np.concatenate((zeros, ones, ones))
keep_idx = keep_idx[:49 * 2]
np.random.shuffle(keep_idx)
blood_keep = blood_types[keep_idx]
encoded_keep = encoded[keep_idx]
encoded_keep = encoded_keep.ravel().reshape(-1, encoded_keep.shape[-1])
blood_keep = blood_keep.ravel()

X = encoded_keep
tiledata = X
y = blood_keep

nnz = np.count_nonzero(tiledata,axis=0)

fracnnz = np.divide(nnz.astype(float),tiledata.shape[0])

# Only keeping data that has less than 10% missing data

idxKeep1 = fracnnz >= 0.9
#    tiledata = tiledata[:,idxKeep]

tiledata = tiledata - 1

nnz = np.count_nonzero(tiledata,axis=0)

fracnnz2 = np.divide(nnz.astype(float),tiledata.shape[0])

idxKeep2 = fracnnz2 >= 0.8

tiledata = tiledata + 1

idxKeepboth = fracnnz + fracnnz2 > 1.8

idxKeep12 = np.logical_and(idxKeep1,idxKeep2)
idxKeep = np.logical_and(idxKeepboth,idxKeep12)
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

# pathdataOH =  np.repeat(pathdata[idxKeep],invals)
# oldpath = np.repeat(idxOP[idxKeep],invals)

# Run the encoder in parts to determine rows that pass the signficance level (chi^2)

print("Running the Encoder...")

ny = tiledata.shape[1]

print(ny)

nparts = 4

idx = np.linspace(0,ny,num=nparts).astype('int')

Xtrain2 = csr_matrix(np.empty([tiledata.shape[0], 0]))
pidx = np.empty([0,],dtype='bool')

for ichunk in np.arange(0,nparts-1):
    imin = idx[ichunk]
    imax = idx[ichunk+1]
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)

    # 1-hot encoding tiled data
    Xtrain = enc.fit_transform(tiledata[:,imin:imax])

    print(Xtrain.shape)
    # print(pathdataOH.shape)
    
    [chi2val,pval] = chi2(Xtrain, y)
    print(np.amax(pval))
    print(np.amin(pval))

    pidxchunk = pval <= 0.02
    Xchunk = Xtrain[:,pidxchunk]

    print(ichunk)
    print(Xchunk.shape)

    pidx=np.concatenate((pidx,pidxchunk),axis=0)
    Xtrain2=hstack([Xtrain2,Xchunk],format='csr')

# pathdataOH = pathdataOH[pidx]
# oldpath = oldpath[pidx]
varvals = varvals[pidx]

print(Xtrain2.shape)
# print(oldpath.shape)

# TODO: ADD THIS BACK IN. chi2 won't work otherwise.
Xtrain = Xtrain2

to_keep = varvals > 2 
idkTK = np.nonzero(to_keep)
idkTK = idkTK[0]

Xtrain = Xtrain[:,idkTK]
# pathdataOH = pathdataOH[idkTK]
# oldpath = oldpath[idkTK]
varvals = varvals[idkTK]

# np.save(chrom+'_pathdataOH.npy', pathdataOH)
# np.save(chrom+'_oldpath.npy',oldpath)
chrom = "blood_type"
# np.save(chrom+'_varvars.npy',varvals)
np.save(chrom+'_y.npy',y)
scipy.sparse.save_npz(chrom+'_Xtrain.npz', Xtrain)