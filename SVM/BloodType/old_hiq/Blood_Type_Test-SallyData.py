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


# Load in Sally's data, already scaled
X1 = np.load("/home/sarah/test/keep/by_id/su92l-4zz18-5go7aan35ql1o65/b_training.npy")
y1 = np.load("/home/sarah/test/keep/by_id/su92l-4zz18-5go7aan35ql1o65/b_training_labels.npy")

# Train the SVM
Cval = 1 # SVM regularization parameter
classifier = svm.LinearSVC(penalty='l1', dual=False, C=Cval)
svc = classifier.fit(X1, y1)

coefs = svc.coef_
y_pred = svc.predict(X1)

# Compute confusion matrix
cnf_matrix = confusion_matrix(y1, y_pred)
print(np.matrix(cnf_matrix))


# Plot the Confusion Matrix

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
plt.savefig('Images/B_Confusion.png',format='png',dpi=300)


# Calculate Accuracy using 10-fold

n = 10
scores = cross_val_score(classifier, X1, y1, cv=n)

print("Accuracy 10-fold: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# Calculate Accuracy using LOO


loo = LeaveOneOut()
scoresLOO = cross_val_score(classifier, X1, y1, cv=loo)

print("Accuracy LOO: %0.2f (+/- %0.2f)" % (scoresLOO.mean(), scoresLOO.std() * 2))
