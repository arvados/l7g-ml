import pandas as pd
import numpy as np
import sqlite3
from sklearn import svm
from sklearn.model_selection import cross_val_score, LeaveOneOut, train_test_split
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
import os

from sys import argv
# load data from untap
print("Loading untap data...")
conn = sqlite3.connect(argv[4])
c = conn.cursor()
c.execute('SELECT * FROM demographics')
rows = c.fetchall()
colnames = [i[0] for i in c.description]
data = pd.DataFrame(rows, columns=colnames)
conn.close()

print("Processing data...")
dataBloodType = data[['human_id', 'blood_type']]
dataBloodType = dataBloodType.replace('', np.nan, inplace=False)
dataBloodType = dataBloodType.dropna(axis=0, how='any', inplace=False)

# Creating dummy variables for A, B and rh factor
dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)

print("Loading tile data from keep. This may take a while...")
Xtrain = np.load(argv[1])
path_data = np.load(argv[3])

Xtrain += 2

names_file = open(argv[2], 'r')
names = []
for line in names_file:
    names.append(line[45:54][:-1])

# Getting phenotypes for huIDs that have associated genotypes

print("Loading phenotype data...")
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
#df2

df2['blood_type'].value_counts()
del df

# Get genotypes that have associated blood type phenotype
idx = df2['Number'].values

Xtrain = Xtrain[idx,:] 
Xtrain.shape

# Remove tiles (columns) that don't have more than 1 tile varient at every position
# Actually probably will want to technically do this before the one-hot, so I am keeping these in for the moment

min_indicator = np.amin(Xtrain, axis=0)
max_indicator = np.amax(Xtrain, axis=0)

sameTile = min_indicator == max_indicator
skipTile = ~sameTile

Xtrain = Xtrain[:,skipTile]
newPaths = path_data[skipTile]

# only keep data with less than 10% missing data
print("Deleting data with more than 10% missing data...")
nnz = np.count_nonzero(Xtrain, axis=0)
fracnnz = np.divide(nnz.astype(float), Xtrain.shape[0])

idxKeep = fracnnz >= 0.9
idxOP = np.arange(Xtrain.shape[1])
Xtrain = Xtrain[:, idxKeep]

y = df2.A.values

# save information about deleting missing/spanning data
print("Calculating varvals...")
varvals = np.full(50 * Xtrain.shape[1], np.nan)
nx = 0

varlist = []
for j in range(0, Xtrain.shape[1]):
    u = np.unique(Xtrain[:,j])
    varvals[nx : nx + u.size] = u
    nx = nx + u.size
    varlist.append(u)

varvals = varvals[~np.isnan(varvals)]

print("Varvals shape:", varvals.shape)

def foo(col):
    u = np.unique(col)
    nunq = u.shape
    return nunq

invals = np.apply_along_axis(foo, 0, Xtrain)
invals = invals[0]
print("Calculated invals successfully.")

print("Calculating path data...")
# used later to find coefPaths
pathdataOH = np.repeat(newPaths[idxKeep], invals)
# used later to find the original location of the path from non one hot
oldpath = np.repeat(idxOP[idxKeep], invals)

print("Starting one-hot encoding. This may take a while...")
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()

encoded = enc.fit_transform(Xtrain)

print("Encoding finished. Deleting No-Calls and Spanning Tiles...")
to_keep = varvals >= 2
idxTK = np.nonzero(to_keep)
idxTK = idxTK[0]

encoded = encoded[:, idxTK]
varvals = varvals[idxTK]
pathdataOH = pathdataOH[idxTK]
oldpath = oldpath[idxTK]
print("Processing finished. Starting machine learning...")
X_train, X_test, y_train, y_test = train_test_split(encoded, y, test_size=0.2)

# C = 0.02  # SVM regularization parameter
classifier = LinearSVC(penalty='l1', class_weight='balanced', dual=False, C=.02)
svc = classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(accuracy_score(y_test, y_pred))
def printCoefs(classifier):
    # retrieve all the nonzero coefficients and zip them with their respective indices
    nonzeroes = np.nonzero(classifier.coef_[0])[0]
    coefs = zip(nonzeroes, classifier.coef_[0][nonzeroes])

    # sort the coefficients by their value, instead of index
    coefs.sort(key = lambda x: x[1], reverse=True)

    for coef in coefs[:50]:
        print coef
printCoefs(svc)
