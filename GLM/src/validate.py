#!/usr/bin/env python3

import numpy as np
import scipy as sc
import sklearn as sk
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression

def filter_row_column(row_column, row_indices, column_indices):
  row = row_column[0]
  column = row_column[1]
  row_pass = np.isin(row, row_indices)
  column_pass = np.isin(column, column_indices)
  both_pass = row_pass & column_pass
  row_filtered = row[both_pass]
  column_filtered = column[both_pass]
  row_column_filtered = np.array([row_filtered, column_filtered])
  return row_column_filtered

def extract_tilevars(countfile, threshold):
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
  column_sublist = []
  ct = onehot_columns.transpose()
  for i in range(len(ct)):
    tilevar = tuple(ct[i, :3])
    if tilevar in tilevars:
      column_sublist.append(i)
  column_indices = np.array(column_sublist)
  return column_indices

def make_matrix(row_column):
  data = np.ones(row_column.shape[1])
  row = row_column[0]
  column = row_column[1]
  matrix = sc.sparse.csr_matrix((data, (row, column)))
  return matrix

def make_labels(samplesfile):
  labels = {}
  indices = []
  ads = []
  with open(samplesfile) as f:
    for line in f:
      index = int(line.strip().split(',')[0])
      ad = int(line.strip().split(',')[2])
      indices.append(index)
      ads.append(ad)
  # this is subject to change
  training_len = int(0.8*len(indices))
  training_indices = indices[:training_len]
  training_ads = ads[:training_len]
  validation_indices = indices[training_len:]
  validation_ads = ads[training_len:]
  labels["training"] = np.array([training_indices, training_ads])
  labels["validation"] = np.array([validation_indices, validation_ads])
  return labels

def main():
  onehotfile, onehotcolumnfile, samplesfile, countfile, threshold = sys.argv[1:]
  row_column = np.load(onehotfile)
  onehot_columns = np.load(onehotcolumnfile)
  threshold = int(threshold)
  labels = make_labels(samplesfile)
  training_indices = labels["training"][0]
  training_ads = labels["training"][1]
  validation_indices = labels["validation"][0]
  validation_ads = labels["validation"][1]
  tilevars = extract_tilevars(countfile, threshold)
  column_indices = get_column_indices(onehot_columns, tilevars)
  training_row_column = filter_row_column(row_column, training_indices, column_indices)
  training_matrix = make_matrix(training_row_column)
  clf = LogisticRegression(penalty='none', max_iter=500).fit(training_matrix, training_ads)
  validation_row_column = filter_row_column(row_column, validation_indices, column_indices)
  validation_matrix = make_matrix(validation_row_column)
  prediction = np.take(clf.predict(validation_matrix), validation_indices)
  score = sk.metrics.accuracy_score(validation_ads, prediction)
  print(score)
  cm = confusion_matrix(validation_ads, prediction)
  disp = ConfusionMatrixDisplay(confusion_matrix=cm)
  disp.plot()
  plt.savefig('confusion_matrix.png')

if __name__ == "__main__":
  main()
