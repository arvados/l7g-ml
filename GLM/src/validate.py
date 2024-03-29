#!/usr/bin/env python3

import numpy as np
import pandas as pd
import scipy as sc
import sklearn as sk
import sys
import os
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, log_loss, confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def extract_tilevars(countfile, allauxiliaries, fractionthreshold):
  """Extract the set of tile variants and auxiliaries that exceed given
  fraction threshold."""
  tilevars = set([])
  auxiliaries = []
  with open(countfile) as f:
    for line in f:
      fraction = float(line.strip().split(',')[1])
      if fraction < fractionthreshold:
        continue
      feature = line.strip().split(',')[0]
      if feature in allauxiliaries:
        auxiliaries.append(feature)
      else:
        tilevar = tuple(int(a) for a in feature.split('-'))
        tilevars.add(tilevar)
  return (tilevars, auxiliaries)

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

def train_validate(auxiliaries, column_indices, df, matrix, onehot_columns):
  """Train and validate logistic regression model."""
  training_indices = df[df["TrainingValidation"]==1]["Index"].to_numpy()
  training_ads = df[df["TrainingValidation"]==1]["CaseControl"].to_numpy()
  training_auxiliaries = df[df["TrainingValidation"]==1][auxiliaries].to_numpy()
  validation_indices = df[df["TrainingValidation"]==0]["Index"].to_numpy()
  validation_ads = df[df["TrainingValidation"]==0]["CaseControl"].to_numpy()
  validation_auxiliaries = df[df["TrainingValidation"]==0][auxiliaries].to_numpy()
  # horizontally stack phenotype matrix with training/validation submatrix
  training_matrix = sc.sparse.hstack((training_auxiliaries, matrix[training_indices][:, column_indices]))
  validation_matrix = sc.sparse.hstack((validation_auxiliaries, matrix[validation_indices][:, column_indices]))
  # logitstic regression training with balanced weights
  clf = LogisticRegression(penalty='none', class_weight='balanced', max_iter=500).fit(training_matrix, training_ads)
  prediction = clf.predict(validation_matrix)
  coef = clf.coef_.flatten()
  accuracy = sk.metrics.accuracy_score(validation_ads, prediction)
  roc_auc = roc_auc_score(validation_ads, clf.predict_proba(validation_matrix)[:,1])
  log_likelihood = -log_loss(validation_ads, clf.predict_proba(validation_matrix), normalize=False)
  dict_output = {"feature": auxiliaries +
                            ["{}-{}-{}".format(onehot_columns[0,i], onehot_columns[1,i], onehot_columns[2,i]) for i in column_indices],
                 "coef": coef}
  df_output = pd.DataFrame(dict_output)
  df_output = df_output.reindex(df_output["coef"].abs().sort_values(ascending=False).index)
  cm = confusion_matrix(validation_ads, prediction)
  display = ConfusionMatrixDisplay(confusion_matrix=cm)
  return (accuracy, roc_auc, log_likelihood, df_output, display)

def main():
  onehotfile, onehotcolumnfile, samplesauxiliaryfile, countfile, fractionthreshold, apoetile = sys.argv[1:]
  row_column = np.load(onehotfile)
  matrix = make_matrix(row_column)
  onehot_columns = np.load(onehotcolumnfile)
  df = pd.read_table(samplesauxiliaryfile)
  allauxiliaries = df.columns.values.tolist()[4:]
  auxiliaries_dict = {}
  column_indices_dict = {}
  accuracy_dict = {}
  roc_auc_dict = {}
  log_likelihood_dict = {}
  df_output_dict = {}
  display_dict = {}
  # run the model with features selected by glmnetboot
  fractionthreshold = float(fractionthreshold)
  tilevars, auxiliaries_dict["glmnetboot_features"] = extract_tilevars(countfile, allauxiliaries, fractionthreshold)
  column_indices_dict["glmnetboot_features"] = get_column_indices(onehot_columns, tilevars)
  (accuracy_dict["glmnetboot_features"], roc_auc_dict["glmnetboot_features"], log_likelihood_dict["glmnetboot_features"],
    df_output_dict["glmnetboot_features"], display_dict["glmnetboot_features"]) = train_validate(
    auxiliaries_dict["glmnetboot_features"], column_indices_dict["glmnetboot_features"], df, matrix, onehot_columns)
  # locate apoe, which is the first feature selectd by glmnetboot
  apoe_pos, apoe_num = apoetile.split("-")[:2]
  apoe_pos, apoe_num = int(apoe_pos), int(apoe_num)
  apoe_column_indices = [i for i in column_indices_dict["glmnetboot_features"]
                         if onehot_columns[0,i] == apoe_pos and onehot_columns[1,i] == apoe_num]
  apoe_column_indices = np.array(apoe_column_indices)
  # set up comparison models
  comparisonmodels= ["sex-age_normalized", "allauxiliaries", "apoe",
                     "sex-age_normalized-apoe", "allauxiliaries-apoe"]
  auxiliaries_dict["sex-age_normalized"] = ["Sex", "Age_normalized"]
  column_indices_dict["sex-age_normalized"] = np.array([])
  auxiliaries_dict["allauxiliaries"] = allauxiliaries
  column_indices_dict["allauxiliaries"] = np.array([])
  auxiliaries_dict["apoe"] = []
  column_indices_dict["apoe"]= apoe_column_indices
  auxiliaries_dict["sex-age_normalized-apoe"] = ["Sex", "Age_normalized"]
  column_indices_dict["sex-age_normalized-apoe"] = apoe_column_indices
  auxiliaries_dict["allauxiliaries-apoe"] = allauxiliaries
  column_indices_dict["allauxiliaries-apoe"] = apoe_column_indices
  for model in comparisonmodels:
    (accuracy_dict[model], roc_auc_dict[model], log_likelihood_dict[model],
      df_output_dict[model], display_dict[model]) = train_validate(
      auxiliaries_dict[model], column_indices_dict[model], df, matrix, onehot_columns)
  for model in ["glmnetboot_features"]+comparisonmodels:
    print("model: {}".format(model))
    print("accuracy: {}".format(accuracy_dict[model]))
    print("roc_auc: {}".format(roc_auc_dict[model]))
    if model in comparisonmodels:
      degrees_of_freedom = np.abs(len(auxiliaries_dict[model]) + len(column_indices_dict[model])
        - len(auxiliaries_dict["glmnetboot_features"]) - len(column_indices_dict["glmnetboot_features"]))
      pvalue = sc.stats.chi2.sf(-2*(log_likelihood_dict[model] - log_likelihood_dict["glmnetboot_features"]), degrees_of_freedom)
      print("pvalue comparing to glmnetboot_features: {}".format(pvalue))
    print(df_output_dict[model].to_string(index=False))
    print()
    display_dict[model].plot()
    plt.savefig("confusion_matrix_{}.png".format(model))
  df_output_dict["glmnetboot_features"].to_csv("feature_coef.tsv", sep='\t', index=False)

if __name__ == "__main__":
  main()
