import numpy as np
import sqlite3
import seaborn as sns
import pandas as pd
import os

from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder

import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

untapdb = '/data-sdd/cwl_tiling/datafiles/untap.db'
allfile = '/data-sdd/cwl_tiling/keep/by_id/su92l-4zz18-b8rs5x7t6gry16k/all.npy'
infofile = '/data-sdd/cwl_tiling/keep/by_id/su92l-4zz18-b8rs5x7t6gry16k/all-info.npy'
namesfile = '/data-sdd/cwl_tiling/keep/by_id/su92l-4zz18-b8rs5x7t6gry16k/names.npy'

# Format is (X_filename, y_filename, blood type, filter type, augmentation type)
#TODO: Fix the balanced augmentation so it works for *very* unbalanced classes. Right now it only works if the smaller class
# is within a factor of 5 of the bigger class

filenames = [("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy", "A", "chi2", None)]

#filenames = [("blood_type_B_no_filter_no_augmentation_X.npz", "blood_type_B_no_filter_no_augmentation_y.npy", "B", None, None),
#             ("blood_type_Rh_chi2_balanced_augmentation_X.npz", "blood_type_Rh_chi2_balanced_augmentation_y.npy", "Rh", "chi2", "balanced"),
#             ("blood_type_Rh_chi2_no_augmentation_X.npz", "blood_type_Rh_chi2_no_augmentation_y.npy", "Rh", "chi2", None),
#             ("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy", "A", "chi2", None),
#             ("blood_type_B_chi2_no_augmentation_X.npz", "blood_type_B_chi2_no_augmentation_y.npy", "B", "chi2", None)]

for X_filename, y_filename, blood_type, filter_type, augmentation_type in filenames:
    print("===========Beginning work on %s and %s===========" % (X_filename, y_filename))
    sns.set()
    # load data from untap
    conn = sqlite3.connect(untapdb)
    c = conn.cursor()
    c.execute('SELECT * FROM demographics')
    rows = c.fetchall()
    colnames = [i[0] for i in c.description]
    data = pd.DataFrame(rows, columns=colnames)
    conn.close()
    dataBloodType = data[['human_id', 'blood_type']]
    dataBloodType = dataBloodType.replace('', np.nan, inplace=False)
    dataBloodType = dataBloodType.dropna(axis=0, how='any', inplace=False)

    # Creating dummy variables for A, B and rh factor
    dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
    dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
    dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)

    # function to retrieve a tile file from keep
    tiled_data_dir = "./"
    def get_file(name, np_file = True):
        if np_file: 
            return np.load(os.path.join(tiled_data_dir, name))
        else:
            return open(os.path.join(tiled_data_dir, name), 'r')

    Xtrain = np.load(allfile)
    pathdata = np.load(infofile)

    Xtrain += 2
    names_file = get_file(namesfile, np_file = False)
    names = []
    for line in names_file:
        names.append(line[45:54][:-1])

    # Getting phenotypes for huIDs that have associated genotypes

    results = [i.lower() for i in names]

    df = pd.DataFrame(results,columns={'Sample'})
    df['Number'] = df.index
    dataBloodType = data[['human_id', 'blood_type']]
    dataBloodType = dataBloodType.replace('', np.nan, inplace=False)
    dataBloodType = dataBloodType.dropna(axis=0, how='any', inplace=False)

    # Creating dummy variables for A, B and rh factor
    dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
    dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
    dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)

    dataBloodType.human_id = dataBloodType.human_id.str.lower()
    df2 = df.merge(dataBloodType,left_on = 'Sample', right_on='human_id', how='inner')
    del dataBloodType
    df2['blood_type'].value_counts()
    del df
    idx = df2['Number'].values

    Xtrain = Xtrain[idx,:] 

    # Remove tiles (columns) that don't have more than 1 tile varient at every position
    # Actually probably will want to technically do this before the one-hot, so I am keeping these in for the moment

    min_indicator = np.amin(Xtrain, axis=0)
    max_indicator = np.amax(Xtrain, axis=0)

    sameTile = min_indicator == max_indicator
    skipTile = ~sameTile

    idxOP = np.arange(Xtrain.shape[1])
    Xtrain = Xtrain[:, skipTile]
    newPaths = pathdata[skipTile]
    idxOP = idxOP[skipTile]

    # only keep data with less than 10% missing data
    nnz = np.count_nonzero(Xtrain, axis=0)
    fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])

    idxKeep = fracnnz >= 0.9
    Xtrain = Xtrain[:, idxKeep]
    
    if blood_type == "A":
        y = df2.A.values
        print("Extracting data for blood type A")
    elif blood_type == "B":
        y = df2.B.values
        print("Extracting data for blood type B")
    elif blood_type == "Rh":
        y = df2.Rh.values
        print("Extracting data for blood type Rh")
    else:
        raise ValueError("The blood type specified isn't currently handled. You may need to edit the code block around this error to handle it.")
    
    # save information about deleting missing/spanning data
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
    # used later to find the original location of the path from non one hot
    oldpath = np.repeat(idxOP[idxKeep], invals)

    train_data = Xtrain
    blood_types = y

    if augmentation_type == "balanced":
        print("Using balanced data augmentation. Note that this only works when the larger class is up to 5x the size of the smaller one.")
        zeros = np.argwhere(blood_types == 0)
        ones = np.argwhere(blood_types == 1)
        
        if len(zeros) > len(ones):
            longer = zeros
            shorter = ones
        else:
            longer = ones
            shorter = zeros
        keep_idx = np.concatenate((longer, shorter, shorter, shorter, shorter, shorter))
        keep_idx = keep_idx[:len(longer) * 2]
        np.random.shuffle(keep_idx)
        blood_types = blood_types[keep_idx]
        train_data = train_data[keep_idx]
        
        X = train_data.ravel().reshape(-1, train_data.shape[-1])
        y = blood_types.ravel()
    else:
        print("Using no data augmentation")
        randomize_idx = np.arange(len(blood_types))
        np.random.shuffle(randomize_idx)
        X = train_data[randomize_idx,:]
        y = blood_types[randomize_idx]
    
    tiledata = X
    nnz = np.count_nonzero(tiledata,axis=0)
    
    # Run the encoder in parts to determine rows that pass the signficance level (chi^2)

    print("Beginning to one-hot encode data")

    ny = tiledata.shape[1]

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
    
        # print(pathdataOH.shape)
        
        if filter_type == 'chi2':
            print("Using chi2 filter")
            [chi2val,pval] = chi2(Xtrain, y)
            pidxchunk = pval <= 0.02
            Xchunk = Xtrain[:,pidxchunk]
            
        else:
            print("Using no filter")
            print(Xtrain.shape)
            Xchunk = Xtrain
            pidxchunk = np.ones(Xchunk.shape[1], dtype=bool)
            
        pidx=np.concatenate((pidx,pidxchunk),axis=0)
        Xtrain2=hstack([Xtrain2,Xchunk],format='csr')

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
    np.save(y_filename, y)
    scipy.sparse.save_npz(X_filename, Xtrain)

    print("Just created datasets for %s and %s\n" % (X_filename, y_filename))

