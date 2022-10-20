#!/usr/bin/env python3

import numpy as np
import scipy as sc
import sklearn as sk
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression

def extract_tilevars(countfile, threshold):
  """Extract the set of tile variants that exceed given threshold."""
  tilevars = set([])
  with open(countfile) as f:
    for line in f:
      count = int(line.split(',')[1])
      if count >= threshold:
        tilevarstr = line.split(',')[0]
        tilevar = tuple(int(a) for a in tilevarstr.split('-'))
        tilevars.add(tilevar)
  return tilevars

def get_column_indices(onehot_columns, tilevars):
  """Get tile varians indices in onehot columns."""
  column_sublist = []
  ct = onehot_columns.transpose()
  for i in range(len(ct)):
    tilevar = tuple(ct[i, :3])
    if tilevar in tilevars:
      column_sublist.append(i)
  column_indices = np.array(column_sublist)
  return column_indices

def make_matrix(row_column):
  """Make sparse matrix from row/column numpy."""
  data = np.ones(row_column.shape[1])
  row = row_column[0]
  column = row_column[1]
  matrix = sc.sparse.csr_matrix((data, (row, column)))
  return matrix

def extract_submatrix(matrix, row_indices, column_indices):
  """Extract submatrix from full matrix given row indices and column indices."""
  matrixarray = matrix.toarray()
  submatrix = matrixarray.take(row_indices, axis=0).take(column_indices, axis=1)
  matrix = sc.sparse.csr_matrix(submatrix)
  return matrix

def make_labels(samplesfile):
  """Make labels of training indices and AD status and
  validation indices and AD status."""
  labels = {}
  training_indices = []
  training_ads = []
  validation_indices = []
  validation_ads = []
  with open(samplesfile) as f:
    for line in f:
      index = int(line.strip().split(',')[0])
      ad = int(line.strip().split(',')[2])
      status = line.strip().split(',')[3]
      if status == "training":
        training_indices.append(index)
        training_ads.append(ad)
      elif status == "validation":
        validation_indices.append(index)
        validation_ads.append(ad)
  labels["training"] = np.array([training_indices, training_ads])
  labels["validation"] = np.array([validation_indices, validation_ads])
  return labels

def main():
  onehotfile, onehotcolumnfile, samplesfile, countfile, threshold = sys.argv[1:]
  row_column = np.load(onehotfile)
  full_matrix = make_matrix(row_column)
  onehot_columns = np.load(onehotcolumnfile)
  threshold = int(threshold)
  labels = make_labels(samplesfile)
  training_indices = labels["training"][0]
  training_ads = labels["training"][1]
  validation_indices = labels["validation"][0]
  validation_ads = labels["validation"][1]
  tilevars = extract_tilevars(countfile, threshold)
  column_indices = get_column_indices(onehot_columns, tilevars)
  training_matrix = extract_submatrix(full_matrix, training_indices, column_indices)
  validation_matrix = extract_submatrix(full_matrix, validation_indices, column_indices)
  # logitstic regression training with balanced weights
  clf = LogisticRegression(penalty='none', class_weight='balanced', max_iter=500).fit(training_matrix, training_ads)
  prediction = clf.predict(validation_matrix)
  score = sk.metrics.accuracy_score(validation_ads, prediction)
  print(score)
  cm = confusion_matrix(validation_ads, prediction)
  disp = ConfusionMatrixDisplay(confusion_matrix=cm)
  disp.plot()
  plt.savefig('confusion_matrix.png')

if __name__ == "__main__":
  main()
