import pandas as pd
import numpy as np
import glob,os
import math
import glob, os
import sys

dirname, outcsv = sys.argv[1:3]

os.chdir(dirname)
initialFile = 1
files = glob.glob("*min*.txt")
print(files)

for file in files:
   bootfile = pd.read_csv(file, delimiter='\t')
   bootfile = bootfile.dropna()

   bootfileSmall = bootfile.set_index('feature')
   bootfileSmall = bootfileSmall.T
   bootfileSmall = bootfileSmall.reset_index()
   bootfileSmall = bootfileSmall.drop(['index'], axis=1)

   if initialFile == 1:
      totalBoot = bootfileSmall
      initialFile = 0
   else:
      totalBoot = pd.concat([totalBoot, bootfileSmall])

totalBoot = totalBoot.fillna(0)
meanCoef = totalBoot.mean()
stdCoef = totalBoot.std()
CI1 = meanCoef + stdCoef
CI2 = meanCoef - stdCoef
allCI = pd.concat([meanCoef, CI2, CI1, stdCoef], axis=1)
print(allCI)
sign1 = CI1 > 0
sign2 = CI2 > 0

testSign = sign1 == sign2
CIrobust1 = CI1[testSign.values]
CI2robust = CI2[testSign.values]
meanrobust = meanCoef[testSign.values]

totalCI = pd.concat([CIrobust1, meanrobust, CI2robust], axis=1)
print(totalCI)
#totalCI.to_csv('CI.csv', index=True)

ccount = totalBoot.apply(lambda x: np.count_nonzero(x)/len(files))
ccount.to_csv(outcsv, index=True)
