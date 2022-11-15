#!/usr/bin/env python3

import numpy as np
import pandas as pd
import re
import subprocess
import sys

def make_extendedpattern(df):
  """Make extended pattern for searching annotation vcf.
  For example, extended pattern for tile variant 9559125-3 includes
  9559125-3, 9559125-2, 9559125-1."""
  features = df["feature"].to_list()
  tilevarpattern = r"\d+-\d+-[01]"
  tilevars = set([feature for feature in features if re.match(tilevarpattern, feature)])
  extendedtilevars = []
  for tilevar in tilevars:
    pos = int(tilevar.split("-")[0])
    num = int(tilevar.split("-")[1])
    for i in range(num, 0, -1):
      extendedtilevars.append(",{}-{},".format(pos, i))
  extendedpattern = "|".join(extendedtilevars)
  return extendedpattern

def annotate_feature(feature, annotation):
  """Look for a feature in the annotation string.
  For example, if 9559125-3 is not found, then look for 9559125-2, 9559125-1,
  until a feature is found."""
  annodict = {"hgvs": "", "rsid": "", "af": ""}
  tilevarpattern = r"\d+-\d+-[01]"
  if not re.match(tilevarpattern, feature):
    return annodict
  pos = int(feature.split("-")[0])
  num = int(feature.split("-")[1])
  for i in range(num, 0, -1):
    pattern = re.compile(r'.*,{}-{},.*'.format(pos, i), re.MULTILINE)
    lines = re.findall(pattern, annotation)
    if len(lines) == 0:
      continue
    hgvslist = []
    rsidlist = []
    aflist = []
    for line in lines:
      fields = line.split("\t")
      hgvs = fields[2].split(";")[0]
      hgvslist.append(hgvs)
      if ";" in fields[2]:
        rsid = fields[2].split(";")[1]
      else:
        rsid = ""
      rsidlist.append(rsid)
      last = fields[-1].split("|")[-1]
      if "AC=" in last:
        af = "AC="+last.split("AC=")[1]
      else:
        af = ""
      aflist.append(af)
    annodict["hgvs"] = "|".join(hgvslist)
    annodict["rsid"] = "|".join(rsidlist)
    annodict["af"] = "|".join(aflist)
    break
  return annodict

def annotate_dataframe(df, annotation):
  """Annotate dataframe given annotation lines found in annotation vcf.
  Adding HGVS, RSID, AF (allele frequency) fields."""
  features = df["feature"].to_list()
  hgvslist = []
  rsidlist = []
  aflist = []
  for feature in features:
    annodict = annotate_feature(feature, annotation)
    hgvslist.append(annodict["hgvs"])
    rsidlist.append(annodict["rsid"])
    aflist.append(annodict["af"])
  df["hgvs"] = hgvslist
  df["rsid"] = rsidlist
  df["af"] = aflist

def main():
  featurecoeffile, annoationvcf = sys.argv[1:]
  df = pd.read_table(featurecoeffile)
  pattern = make_extendedpattern(df)
  ps = subprocess.Popen(["zcat", annoationvcf], stdout=subprocess.PIPE)
  annotation = subprocess.check_output(["egrep", "'{}'".format(pattern)], stdin=ps.stdout, encoding='UTF-8')
  ps.wait()
  annotate_dataframe(df, annotation)
  df.to_csv("feature_coef_annotated.tsv", sep='\t', index=False)

if __name__ == "__main__":
  main()
