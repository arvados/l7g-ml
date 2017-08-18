"""
Applies machine learning to genomic data of 214 individuals to predict blood 
type.

More technically: this script uses the Harvard PGP dataset to train/test 
a linear support vector classifier for bloodtype A+/-. The dataset consists of
both genotypical and phenotypical data. The genomes within the dataset are tiled
and the tiles serve as the features for machine learning. The target label
is the phenotypical blood type, which is self reported by each patient.

Inputs (currently non-interactive/hard-coded):
* Directory for saving outputs
* hiq-pgp - The high quality subset of the Harvard PGP genomic data. Numpy array
* hiq-pgp-info - Column names for the hiq-pgp numpy array. Numpy array
* names-214.npy - Row names for the hiq-pgp numpy array. Numpy array
* hu-pgp.sqlite3 - Database of phenotypes self-reported by patients. Sqlite

Outputs:
* Blood type A confusion matrix plot. PNG.

"""

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
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("data_dir_harvard_pgp_hiq_214", default='/home/keldin/keep/by_id/su92l-4zz18-mp6wrk95q8li17t')
parser.add_argument("data_dir_untap", default='/home/keldin/keep/by_id/su92l-4zz18-ubrp7z77ogbv4r7')
args = parser.parse_args()
hiq_dir = args.data_dir_harvard_pgp_hiq_214
untap_dir = args.data_dir_untap



# The following section contains numpy load statements for each of the "inputs"
# for the script. For each input, there are several possible directories
# corresponding to where that resource is located on each of a few different
# people's machines. Each option can just be un/commented to make it work.
# 
# Plot output directory
#plot_output_dir = "/home/keldin/Images/"
#plot_output_dir = "/home/keldin/keeprw/by_id/su92l-4zz18-hhyjc7arp04d20t/"
#plot_output_dir = "/Users/Keldins/curoverse/Images/"





# All sets with "magic tile" in /data-sdd/tiling/hiq.214

# Xtrain file paths, 1hot:
#hiq_pgp_1hot_path = "/data-sdd/tiling/hiq.214/hiq-pgp-1hot"
#hiq_pgp_1hot_path = "/home/swz/PGP-work/Lightning_Work/PGPFiles/hiq-pgp-1hot"
#hiq_pgp_1hot_path = "/Users/Keldins/curoverse/hiq/hiq-pgp-1hot"
#Xtrain = np.load(hiq_pgp_1hot_path)

# Xtrain file paths, NOT 1hot:
#hiq_pgp_path = "/data-sdd/tiling/hiq.214/hiq-pgp"
hiq_pgp_path = hiq_dir + "/hiq-pgp"
Xtrain = np.load(hiq_pgp_path)





# ohinfo file paths:
# Recall that names-214.npy is an array of essentially huids. In particular, 
# it contains the huids of the participants that have genotypical data in
# hiq-pgp.
#names_path = "/data-sdd/tiling/hiq.214/names-214.npy"
#names_path = "/Users/Keldins/curoverse/hiq/names-214.npy"
names_path = hiq_dir + "/names-214.npy"
ohinfo = np.load(names_path)






# ohPaths file paths, 1hot:
#hiq_pgp_1hot_info_path = "/home/swz/PGP-work/Lightning_Work/PGPFiles/hiq-pgp-1hot-info"
#ohPaths = np.load(hiq_pgp_1hot_info_path)
# ^ this appears to not be used






# justVarPaths file paths, NOT 1hot:
#hiq_pgp_info_path = "/data-sdd/tiling/hiq.214/hiq-pgp-info"
#hiq_pgp_info_path = "/Users/Keldins/curoverse/hiq/hiq-pgp-info"
hiq_pgp_info_path = hiq_dir + "/hiq-pgp-info"
justVarPaths = np.load(hiq_pgp_info_path)








# Loading in phenotype data from PGP database
# Untap path (Harvard PGP phenotype database scrappings)
# These are local "snapshots" of the database.
#untap_path = "/data-sdd/data/untap/hu-pgp.sqlite3"
#untap_path = "/home/sarah/l7g-ml/BloodType/Database/untap.db"
#untap_path = "/Users/Keldins/curoverse/hiq/hu-pgp.sqlite3"
untap_path = untap_dir + "/untap.sqlite3"
conn = sqlite3.connect(untap_path)

c = conn.cursor()
c.execute('SELECT * FROM demographics')
# c now contains all the phenotype data



# c contains all the phenotype data from the db, but we need to put it into
# a pandas dataframe for ease of use.
# Start by getting all the rows of phenotype data, and the column headers

rows = c.fetchall()
# First row of every column description is the column name (i.e. column headers)
# These are the names of phenotype fields
phenotype_names = [(i[0]) for i in c.description]
phenotype_data = pd.DataFrame(rows,columns=phenotype_names)
conn.close()
# At this point, phenotype_data is a pandas dataframe object containing all the
# phenotype data from the untap database. Now it is actually useful and useable
# to the rest of the script.






# We wish to select a subset of the phenotype data, namely the huid ("human_id")
# as an identifier, and the blood type itself.
# DataFrame allows indexing by a list, which returns another DataFrame.

dataBloodType = phenotype_data[['human_id','blood_type']]

dataBloodType = dataBloodType.replace('', np.nan, inplace=False)

dataBloodType = dataBloodType.dropna(axis=0, how='any', inplace=False)
# At this point, we've dropped every row (i.e. every patient) that doesn't have
# a blood type listed.


# Creating dummy variables for A, B and Rh factor
# If DataFrame row contains blood type A, then mark as True. You get a pandas
# Series of booleans (as integers: 0,1). Special case: NaN treated as false.
dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
# Same as A, but for B:
dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
# Now the same again, but for Rh (+/-) for A and B. + is treated as True.
dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)
# Other cases:
# AB is a special case where the patient has both A and B antigens, which means
# the A line and the B line above would result in "True". This is fine because
# we expect the genes responsible to have a simple additive effect.
# Blood type O is a special case where the patient is marked "False" for A or B.

# Getting phenotypes for huIDs that have associated genotypes

# Given a byte string, this anon func will return string up to "-" character 
# b'hu040C0A-GS01175-DNA_F05' is what rows of ohinfo look like, so this will
# give us first part of the string, which is the huid.
extract_str_huid = lambda byte_string: byte_string[0:byte_string.find(b"-")]

# Take huid in byte string to utf and lower case
huids = [extract_str_huid(patient_row).decode("utf-8").lower() for patient_row in ohinfo]

huids_df = pd.DataFrame(huids,columns={'Sample'})
huids_df['Number'] = huids_df.index
# Now we have a DataFrame for the huids, with a Number column that matches the
# DataFrame index. The dataframe index will change later after other operations, so we
# need to store it now as Number. Later we can use the Number column to index Xtrain.

# Take huid in bloodtype DataFrame to lower case
dataBloodType.human_id = dataBloodType.human_id.str.lower()

# We wish to create a unified DataFrame for the data in dataBloodType and huids_df
# So we use the merge() method.
# By using option how='inner', we take the intersection of the data in both
# This accomplishes the important task of making sure we're only looking at
# huids (patients) for which we have both phenotypical data (their blood type)
# and genotypical data (their tiled genome).

unified_df =  huids_df.merge(dataBloodType,left_on = 'Sample', right_on='human_id', how='inner')
del dataBloodType
# As a bit of an aside, we plot the totals for the blood types
unified_df['blood_type'].value_counts().plot(kind='bar')
unified_df['blood_type'].value_counts()
del huids_df


# Get genotypes (tiled genome) for participants that had a blood type listed
# in phenotypical data. We can use the Number column, as only entries with blood type
# data remain.

idx = unified_df['Number'].values
Xtrain = Xtrain[idx,:] 



# Some columns (which are tile positions) will be the same throughout 
# (i.e. all participants have the same genes in that region). Because they 
# do not vary, they contribute nothing to the machine learning. Here we
# remove them.

min_indicator = np.amin(Xtrain, axis=0)
max_indicator = np.amax(Xtrain, axis=0)

# If the min value in the column equals the max value, then there must be no
# variation in the column => everyone has the same tile variant
sameTile = min_indicator == max_indicator
skipTile = ~sameTile

print("skipTile shape: " + str(skipTile.shape))
print("Xtrain shape: " + str(Xtrain.shape))
Xtrain = Xtrain[:,skipTile]
print("Xtrain shape after skipTile: " + str(Xtrain.shape))
print("justVarPaths shape: " + str(justVarPaths.shape))
justVarPathsNew = justVarPaths[skipTile]


# Scaling the Training Data

Xtrain = preprocessing.scale(Xtrain.astype('double'))


y = unified_df.A.values

del unified_df

# Train the SVM
Cval = 0.01  # SVM penalty parameter
classifier = svm.LinearSVC(penalty='l1', dual=False, C=Cval)
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


# Calculate predictions and plot confusion matrix
y_pred = svc.predict(Xtrain)
cnf_matrix = confusion_matrix(y, y_pred)

print(np.matrix(cnf_matrix))


plt.imshow(cnf_matrix,interpolation='nearest', cmap=plt.cm.Blues)
plt.ylabel('True label')
plt.xlabel('Predicted label')

classes = ['A-antigen negative','A-antigen positive']

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

# Save plot output
#plt.savefig(plot_output_dir + "A_Confusion1.png", format='png',dpi=300)
plt.savefig('A_Confusion1.png', format='png',dpi=300)

#coefPaths = justVarPathsNew[idxNZ[1]]


#tile_path = np.trunc(coefPaths/(16**5))
#tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
#tile_phase = np.trunc((coefPaths- tile_path*16**5 - 2*tile_step))


#vtile_path = vhex(tile_path.astype('int'))
#vitle_step = vhex(tile_step.astype('int'))


