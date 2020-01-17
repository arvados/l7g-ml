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
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import argparse 
from sklearn.utils.validation import assert_all_finite
from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from matplotlib import rcParams
import scipy.sparse

def pcafilter():

    # Setting up inputs

    parser = argparse.ArgumentParser()
    parser.add_argument('tilefile1', metavar='TILEFILE1', help='File containing files of tile var matrix')
    parser.add_argument('tilepath1', metavar='TILEPATH1', help='File containing information about tile locations')
    parser.add_argument('tilefile2', metavar='TILEFILE2', help='File containing files of tile var matrix')
    parser.add_argument('tilepath2', metavar='TILEPATH2', help='File containing information about tile locations')
    args = parser.parse_args()
    rcParams.update({'figure.autolayout': True})


    if not os.path.exists('Images'):
      os.makedirs('Images')

    tiledata_file1 = args.tilefile1
    tilepath_file1 = args.tilepath1
    tiledata_file2 = args.tilefile2
    tilepath_file2 = args.tilepath2

    print("Reading in Data...")

    tiledata1= np.load(tiledata_file1)
    pathdata1 = np.load(tilepath_file1)
    tiledata2= np.load(tiledata_file2)
    pathdata2 = np.load(tilepath_file2)

    # Find paths in both pathdata1 and pathdata2

    commonpaths,idc1,idc2 = np.intersect1d(pathdata1,pathdata2,return_indices=True)
#    tiledata = np.vstack((tiledata1[:,idc1],tiledata2[:,idc2])) 
    tiledata1 = tiledata1[:,idc1]
    tiledata2 = tiledata2[:,idc2]
    pathdata = commonpaths

    # Flip phases in tiledata

    [m,n] = tiledata1.shape

    for ix in range(m):     
       n20 = int(n/4)
       ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
       keepa = tiledata1[ix,ieven]
       keepb = tiledata1[ix,ieven+1]
       tiledata1[ix,ieven] = keepb
       tiledata1[ix,ieven+1] = keepa
       del keepa,keepb

    [m,n] = tiledata2.shape

    for ix in range(m):
       n20 = int(n/4)
       ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
       keepa = tiledata2[ix,ieven]
       keepb = tiledata2[ix,ieven+1]
       tiledata2[ix,ieven] = keepb
       tiledata2[ix,ieven+1] = keepa
       del keepa,keepb
  
    tile_path = np.trunc(pathdata/(16**5))
    idx1 = tile_path >= 863
    idx2 = tile_path <= 810
    idx3 = idx2

    idxOP = np.arange(pathdata.shape[0])
    idxOP = idxOP[idx3]

    pathdata = pathdata[idx3]

    print(tiledata1.shape)
    tiledata1 = tiledata1[:,idx3]
    print(tiledata1.shape)

    print(tiledata2.shape)
    tiledata2 = tiledata2[:,idx3]
    print(tiledata2.shape)

    tiledata1 = tiledata1 + 2
    tiledata2 = tiledata2 + 2

    nnz1 = np.count_nonzero(tiledata1,axis=0)
    nnz2 = np.count_nonzero(tiledata2,axis=0)
    nnz = nnz1 + nnz2
    n2 = tiledata1.shape[0] + tiledata2.shape[0]
    fracnnz = np.divide(nnz.astype(float),n2)

    # Only keeping data that has less than 1% missing data

    idxKeep = fracnnz >= 0.99

    tiledata1 = tiledata1[:,idxKeep]
    tiledata2 = tiledata2[:,idxKeep]
    tiledata = np.vstack((tiledata1,tiledata2))

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

    enc = OneHotEncoder(sparse=True, dtype=np.uint16)

    Xtrain = enc.fit_transform(tiledata)

    print(Xtrain.shape)
    
    to_keep = varvals > 2 
    idkTK = np.nonzero(to_keep)
    idkTK = idkTK[0]

    Xtrain = Xtrain[:,idkTK]

    scipy.sparse.save_npz('XtrainPCA.npz', Xtrain)

if __name__ == '__main__':
    pcafilter()
