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
    parser.add_argument('tilefile', metavar='TILEFILE', help='File containing files of tile var matrix')
    parser.add_argument('tilepath', metavar='TILEPATH', help='File containing information about tile locations')

    args = parser.parse_args()
    rcParams.update({'figure.autolayout': True})


    if not os.path.exists('Images'):
      os.makedirs('Images')

    tiledata_file = args.tilefile
    tilepath_file = args.tilepath

    print("Reading in Data...")

    tiledata= np.load(tiledata_file)
    pathdata = np.load(tilepath_file)

    # Flip phases in tiledata

    [m,n] = tiledata.shape

    for ix in range(m): 
       n20 = int(n/4)
       ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
       keepa = tiledata[ix,ieven]
       keepb = tiledata[ix,ieven+1]
       tiledata[ix,ieven] = keepb
       tiledata[ix,ieven+1] = keepa
       del keepa,keepb

    tile_path = np.trunc(pathdata/(16**5))
    idx1 = tile_path >= 863
    idx2 = tile_path <= 810
    idx3 = idx2

    idxOP = np.arange(pathdata.shape[0])
    idxOP = idxOP[idx3]

    pathdata = pathdata[idx3]

    print(tiledata.shape)
    tiledata = tiledata[:,idx3]
    print(tiledata.shape)

    tiledata = tiledata + 2

    nnz = np.count_nonzero(tiledata,axis=0)
    fracnnz = np.divide(nnz.astype(float),tiledata.shape[0])

    # Only keeping data that has less than 1% missing data

    idxKeep = fracnnz >= 0.99

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

    enc = OneHotEncoder(sparse=True, dtype=np.uint16)

    Xtrain = enc.fit_transform(tiledata)

    print(Xtrain.shape)
 
    to_keep = varvals > 1
    idkTK = np.nonzero(to_keep)
    idkTK = idkTK[0]

    Xtrain = Xtrain[:,idkTK]

    scipy.sparse.save_npz('XtrainPCA.npz', Xtrain)

if __name__ == '__main__':
    pcafilter()
