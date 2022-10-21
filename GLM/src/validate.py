#!/usr/bin/env python3

import numpy as np
import pandas as pd
import scipy as sc
import sklearn as sk
import sys
import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

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

def make_dataframe(samplesfile, phenotypedir):
  """Make dataframe with phenotype data."""
  df_samples = pd.read_csv(samplesfile, names=["index", "SampleID", "AD", "status"], header=None)
  phenotype_dfs = []
  for root, dirs, files in os.walk(phenotypedir):
    for name in files:
      phenotype_file = os.path.join(root, name)
      df = pd.read_csv(phenotype_file, sep='\t')[["SampleID", "Sex", "Age_baseline"]]
      phenotype_dfs.append(df)
  df_phenotype = pd.concat(phenotype_dfs)
  dfm = pd.merge(df_samples, df_phenotype, on="SampleID", how="left")
  dfm["Age_normalized"] = dfm["Age_baseline"].replace("90+", "90").astype("double")
  dfm["Age_normalized"] = dfm["Age_normalized"].fillna(value=dfm["Age_normalized"].mean())
  dfm["Age_normalized"] = StandardScaler().fit_transform(dfm[["Age_normalized"]])
  return dfm

def main():
  onehotfile, onehotcolumnfile, samplesfile, phenotypedir, countfile, threshold = sys.argv[1:]
  row_column = np.load(onehotfile)
  matrix = make_matrix(row_column)
  onehot_columns = np.load(onehotcolumnfile)
  threshold = int(threshold)
  df = make_dataframe(samplesfile, phenotypedir)
  training_indices = df[df["status"]=="training"]["index"].to_numpy()
  training_ads = df[df["status"]=="training"]["AD"].to_numpy()
  training_phenotypes = df[df["status"]=="training"][["Sex", "Age_normalized"]].to_numpy()
  validation_indices = df[df["status"]=="validation"]["index"].to_numpy()
  validation_ads = df[df["status"]=="validation"]["AD"].to_numpy()
  validation_phenotypes = df[df["status"]=="validation"][["Sex", "Age_normalized"]].to_numpy()
  tilevars = extract_tilevars(countfile, threshold)
  column_indices = get_column_indices(onehot_columns, tilevars)
  # horizontally stack phenotype matrix (sex and age) with training/validation submatrix
  training_matrix = sc.sparse.hstack((training_phenotypes, matrix[training_indices][:, column_indices]))
  validation_matrix = sc.sparse.hstack((validation_phenotypes, matrix[validation_indices][:, column_indices]))
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
