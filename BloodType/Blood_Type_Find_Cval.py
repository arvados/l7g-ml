import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
from sklearn import svm
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix

# All sets with "magic tile" in /data-sdd/tiling/hiq.214
#Xtrain = np.load("/home/swz/PGP-work/Lightning_Work/PGPFiles/hiq-pgp-1hot")
ohinfo = np.load("/data-sdd/tiling/hiq.214/names-214.npy")
#ohPaths = np.load("/home/swz/PGP-work/Lightning_Work/PGPFiles/hiq-pgp-1hot-info")
Xtrain = np.load("/data-sdd/tiling/hiq.214/hiq-pgp")
justVarPaths = np.load("/data-sdd/tiling/hiq.214/hiq-pgp-info")


# Loading in phenotype data from PGP database

conn = sqlite3.connect('/home/sarah/l7g-ml/BloodType/Database/untap.db')
c = conn.cursor()
c.execute('SELECT * FROM demographics')
rows = c.fetchall()
colnames = [(i[0]) for i in c.description]
data = pd.DataFrame(rows,columns=colnames)
conn.close()


# Find ids for phenotypes with blood type
dataBloodType = data[['human_id','blood_type']]
dataBloodType= dataBloodType.replace('', np.nan, inplace=False)
dataBloodType = dataBloodType.dropna(axis=0, how='any', inplace=False)

# Creating dummy variables for A, B and rh factor
dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)


# Getting phenotypes for huIDs that have associated genotypes

g2 = lambda x:x[0:x.find(b"-")]
results = [g2(i).decode("utf-8").lower() for i in ohinfo]

df = pd.DataFrame(results,columns={'Sample'})
df['Number'] = df.index


dataBloodType.human_id = dataBloodType.human_id.str.lower()
df2 =  df.merge(dataBloodType,left_on = 'Sample', right_on='human_id', how='inner')
del dataBloodType
df2['blood_type'].value_counts().plot(kind='bar')
df2['blood_type'].value_counts()
del df

# Get genotypes that have associated blood type phenotype


idx = df2['Number'].values
Xtrain = Xtrain[idx,:] 


# Remove tiles (columns) that don't have more than 1 tile varient at every position

min_indicator = np.amin(Xtrain, axis=0)
max_indicator = np.amax(Xtrain, axis=0)

sameTile = min_indicator == max_indicator
skipTile = ~sameTile

Xtrain = Xtrain[:,skipTile]
justVarPathsNew = justVarPaths[skipTile]


# Scaling the Training Data

Xtrain = preprocessing.scale(Xtrain.astype('double'))


y = df2.B.values

del df2

Citr = np.logspace(-3, 1, 10)
Citr = Citr.tolist()
scores = []


for idC, Cval in enumerate(Citr):
# Train the SVM
#Cval = 0.01  # SVM penalty parameter

    classifier = svm.LinearSVC(penalty='l1', dual=False, C=Cval)
#svc = classifier.fit(Xtrain, y)

# Examine model coefficents
#maxCoef = svc.coef_.max()
#numnz = np.nonzero(svc.coef_)[1].shape
#idxNZ = np.nonzero(svc.coef_)

# Perform cross validation
# Calculate Accuracy using 10-fold

    n = 10
    cvscores = cross_val_score(classifier, Xtrain, y, cv=n)
    scores.append(cvscores.mean())
    print("%1.3f Accuracy 10-fold: %0.2f (+/- %0.2f)" % (Cval, cvscores.mean(), cvscores.std() * 2))


plt.subplot(1, 1)
plt.xlabel('C')
plt.ylabel('CV Score')
plt.semilogx(Ccal, scores, label="fraction %.2f")
plt.legend(loc="best")
plt.savefig('Images/CvalsB.png',format='png',dpi=300)
