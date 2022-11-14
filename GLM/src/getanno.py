#!/usr/bin/env python3

import numpy as np
import pandas as pd
import re
import subprocess
import sys

def make_pattern(df):
  """Make pattern for searching annotation vcf."""
  features = df["feature"].to_list()
  tilevarpattern = r"\d+-\d+-[01]"
  tilevars = set([feature for feature in features if re.match(tilevarpattern, feature)])
  patterntilevars = [",{},".format("-".join(tilevar.split("-")[:2])) for tilevar in tilevars]
  pattern = "|".join(patterntilevars)
  return pattern

def annotate_dataframe(df, annotation):
  """Annotate dataframe given annotation lines found in annotation vcf.
  Adding HGVS, RSID, AF (allele frequency) fields."""
  features = df["feature"].to_list()
  tilevarpattern = r"\d+-\d+-[01]"
  hgvslist = []
  rsidlist = []
  aflist = []
  for feature in features:
    if not re.match(tilevarpattern, feature):
      hgvslist.append("")
      rsidlist.append("")
      aflist.append("")
      continue
    tilevar = "-".join(feature.split("-")[:2])
    pattern = re.compile(r'.*,{},.*'.format(tilevar), re.MULTILINE)
    lines = re.findall(pattern, annotation)
    if not lines:
      hgvslist.append("")
      rsidlist.append("")
      aflist.append("")
      continue
    feature_hgvslist = []
    feature_rsidlist = []
    feature_aflist = []
    for line in lines:
      fields = line.split("\t")
      hgvs = fields[2].split(";")[0]
      feature_hgvslist.append(hgvs)
      if ";" in fields[2]:
        rsid = fields[2].split(";")[1]
      else:
        rsid = ""
      feature_rsidlist.append(rsid)
      last = fields[-1].split("|")[-1]
      if "AF" in last:
        af = last
      else:
        af = ""
      feature_aflist.append(af)
    hgvslist.append("|".join(feature_hgvslist))
    rsidlist.append("|".join(feature_rsidlist))
    aflist.append("|".join(feature_aflist))
  df["hgvs"] = hgvslist
  df["rsid"] = rsidlist
  df["af"] = aflist

def main():
  featurecoeffile, annoationvcf = sys.argv[1:]
  df = pd.read_table(featurecoeffile)
  pattern = make_pattern(df)
  ps = subprocess.Popen(["zcat", annoationvcf], stdout=subprocess.PIPE)
  annotation = subprocess.check_output(["egrep", "'{}'".format(pattern)], stdin=ps.stdout, encoding='UTF-8')
  annotate_dataframe(df, annotation)
  df.to_csv("feature_coef_annotated.tsv", sep='\t', index=False)

if __name__ == "__main__":
  main()
