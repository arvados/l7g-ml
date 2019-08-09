import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
from sklearn import svm
from sklearn.model_selection import cross_val_score, LeaveOneOut, train_test_split
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns
import os
sns.set()
# load data from untap
conn = sqlite3.connect('./untap.db')
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

Xtrain = np.load('./all.npy')
path_data = np.load('./all-info.npy')

Xtrain += 2
names_file = get_file("names.npy", np_file = False)
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
print(Xtrain.shape)


# Remove tiles (columns) that don't have more than 1 tile varient at every position
# Actually probably will want to technically do this before the one-hot, so I am keeping these in for the moment

min_indicator = np.amin(Xtrain, axis=0)
max_indicator = np.amax(Xtrain, axis=0)

sameTile = min_indicator == max_indicator
skipTile = ~sameTile

idxOP = np.arange(Xtrain.shape[1])
Xtrain = Xtrain[:, skipTile]
newPaths = path_data[skipTile]
idxOP = idxOP[skipTile]

Xtrain.shape

# only keep data with less than 10% missing data
nnz = np.count_nonzero(Xtrain, axis=0)
fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])

idxKeep = fracnnz >= 0.9
Xtrain = Xtrain[:, idxKeep]
y = df2.B.values

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

print(varvals.shape)
np.save("./varvals.npy", varvals)

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
np.save("./idx_keep.npy", idxKeep)
np.save("./path_data_oh.npy", pathdataOH)
np.save("./old_path.npy", oldpath)
np.save("./train_data.npy", Xtrain)
np.save("./blood_types.npy", y)
np.save('./path_data.npy', newPaths)