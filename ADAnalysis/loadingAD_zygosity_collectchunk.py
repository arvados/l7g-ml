import os
import glob
import pandas as pd
import numpy as np
import re
import argparse 
from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from matplotlib import rcParams
import scipy.sparse
from scipy.sparse import save_npz
import hashlib

def collectData():

    # Setting up inputs

    parser = argparse.ArgumentParser()
    parser.add_argument('Xdatadir', metavar='XDATADIR', help='Directory containing files of tile var matrix')
    parser.add_argument('Xrdir', metavar='XRDIR', help='Directory containing files of tile var matrix')
    parser.add_argument('Xcdir', metavar='XCDIR', help='Directory containing files of tile var matrix')
    parser.add_argument('tagnumdir', metavar='TAGVALS', help='Directory containing path information for tiled data')
    parser.add_argument('tagidxdir', metavar='ORGTAGIDX', help= 'Directory containing original path indicies') 
    parser.add_argument('varvaldir',metavar='VARVAL', help='Directory containing tile variant values')
    parser.add_argument('yfiledir', metavar='YVAL',help='Directory containing y values')

    args = parser.parse_args()

    Xdata_dir = args.Xdatadir
    Xr_dir = args.Xrdir
    Xc_dir = args.Xcdir
    tag_dir = args.tagnumdir
    tagix_dir = args.tagidxdir
    varval_dir = args.varvaldir
    yfile_dir = args.yfiledir

    print("Reading in Data...")

    # Finding all data files

    # Loading in all filtered Tiled Data 
    Xdatastr = Xdata_dir +"/*Xdata*"
    Xcstr = Xc_dir +"/*Xc*"
    Xrstr = Xr_dir +"/*Xr*"

    Xdatafiles = glob.glob(Xdatastr)
    Xcfiles = glob.glob(Xcstr)
    Xrfiles = glob.glob(Xrstr)

    Xdatafiles = Xdatafiles.sort() 
    Xcfiles = Xcfiles.sort()
    Xrfiles = Xrfiles.sort()

    coloffset = 0
    Xc = []
    Xr = []
    Xdata = []

    for fileXdata,fileXr,fileXc in zip(Xdatafiles,Xrfiles,Xcfiles):
       Xdatachunkk = np.load(fileXdata)
       Xdata = np.concatenate((Xdata,Xdatachunk))
       Xrchunk = np.load(fileXr)
       Xr = np.concatenate((Xr,Xrchunk))
       Xcchunk = np.load(fileXc)
       Xcchunk = Xchunk + coloffset
       coloffset = np.maximum(Xcchunk) 
       Xc = np.concatenate((Xc,Xcchunk))
       coloffset = np.amax(Xr)

    print(Xc.shape)
    print(Xr.shape)
    print(Xdata.shape)

    # Loading in Tile Position Tag # and Index Data

    pathstr = pathdata_dir + "/oldpath.npy"
    pathfiles = glob.glob(pathstr)
    pathfiles.sort()

    oldpath = np.load(pathfiles[0])

    for filename in pathfiles[1:]:
       pathchunk = np.load(filename)
       oldpath = np.concatenate((oldpath,pathchunk))

    # Loading in Tile Variant Values

    varstr = varval_dir + "/*_varvars.npy"
    varvalfiles = glob.glob(varstr)
    varvalfiles.sort()

    varvals = np.load(varvalfiles[0])

    for filename in varvalfiles[1:]:
       varchunk = np.load(filename)
       varvals = np.concatenate((varvals,varchunk))

    print(varvals.shape)

    # Loading in Y Values

    # Each set of Y values should be the same, if not - issue with data
    ystr = yval_dir + "/*_y.npy"
    yfiles = glob.glob(ystr)
    yfiles.sort()

    y = np.load(yfiles[0])

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

if __name__ == '__main__':
    collectData()
