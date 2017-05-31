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
#df2['blood_type'].value_counts().plot(kind='bar')
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

# Train the SVM
Cval = .078  # SVM penalty parameter
classifier = svm.LinearSVC(penalty='l1', class_weight='balanced', dual=False, C=Cval)
svc = classifier.fit(Xtrain, y)

# Examine model coefficents
maxCoef = svc.coef_.max()
numnz = np.nonzero(svc.coef_)[1].shape
idxNZ = np.nonzero(svc.coef_)

print("Maximum Coefficent (%4.3f):" % maxCoef)
print("Number of Nonzeros Coefficents (%d)" % numnz)

# Perform cross validation
# Calculate Accuracy using 10-fold

n = 10
scores = cross_val_score(classifier, Xtrain, y, cv=n)
print("Accuracy 10-fold: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# Calculate Accuracy using LOO

loo = LeaveOneOut()
scoresLOO = cross_val_score(classifier, Xtrain, y, cv=loo)

print("Accuracy LOO: %0.2f (+/- %0.2f)" % (scoresLOO.mean(), scoresLOO.std() * 2))


# Calc and plot confusion matrix
y_pred = svc.predict(Xtrain)
cnf_matrix = confusion_matrix(y, y_pred)

print(np.matrix(cnf_matrix))


plt.imshow(cnf_matrix,interpolation='nearest', cmap=plt.cm.Blues)
plt.ylabel('True label')
plt.xlabel('Predicted label')

classes = ['B-antigen negative','B-antigen positive']

plt.grid('off')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

for i in range(cnf_matrix.shape[0]):
 for j in  range(cnf_matrix.shape[1]):
        plt.text(j, i, cnf_matrix[i, j],
                 horizontalalignment="center",
                 color= "orangered")

plt.gcf().subplots_adjust(left=0.25, bottom =0.35)
plt.savefig('Images/B_Confusion1hot.png',format='png',dpi=300)


