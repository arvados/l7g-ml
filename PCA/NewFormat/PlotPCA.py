#usr/bin/python
import os
os.environ.get('DISPLAY','')
import matplotlib as mpl
mpl.use('Agg')      # This line must come before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import pandas as pd
import os
import sys
import re
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

a = '../../tileml'
b = '../../pgpml'
sys.path.insert(0, a)
sys.path.insert(0, b)

import tileutils as tileutils
import pgputils as pgputils
pcafile = "/keep/by_id/2xpu4-4zz18-fy4yjurootb8g6o/tiledPCA.npy" 
namesfile =  "/keep/by_id/2xpu4-4zz18-fy4yjurootb8g6o/labels.csv"

# Load PCA Data
tiledPCA = np.load(pcafile)

# Loading in Names of Samples

header_list = ["number","names","outputname"]
df = pd.read_csv(namesfile, names=header_list)
names = df["names"].tolist()

print(names)
cleannames = pgputils.pgpCleanNames(names)

pcaNames = pd.DataFrame(np.column_stack([cleannames, names]),columns=['ID','Filename'])

print(pcaNames)

# Setting Up Colors Based On Geographic Ancestries
ancestry1k = pd.read_csv('igsr_samples.tsv',sep='\t')
ancestry1k = ancestry1k.rename(columns={'Sample name': 'Sample', 'Population code': 'Population'})
ancestryMap = ancestry1k[['Sample','Population']]
ancestryMap['DataSource'] = '1K'
ancestryMap['ID'] = ancestry1k.Sample
ancestryMap['Region'] = ancestry1k.Population
ancestries = ancestryMap[['ID','Region','DataSource']]
print(ancestries)

z = pcaNames.merge(ancestries, how='left', on='ID')
print(z)

z['Color'] = 'black'
idxAmerica1k = z['Region'].isin(['PUR', 'CLM','MXL','PEL'])
idxEurope1k = z['Region'].isin(['TSI','IBS','CEU','GBR','FIN'])
idxAfrica1k = z['Region'].isin(['LWK','MSL','GWD','YRI','ESN','ACB','ASW'])
idxEastAsia1k = z['Region'].isin(['KHV','CDX','CHS','CHB','JPT'])
idxSouthAsia1k = z['Region'].isin(['STU','ITU','BEB','GIH','PJL'])
z.Color[idxAmerica1k] = 'firebrick'
z.Color[idxEurope1k] = 'green'
z.Color[idxAfrica1k] = 'coral'
z.Color[idxEastAsia1k] = 'royalblue'
z.Color[idxSouthAsia1k] = 'blueviolet'

plt.figure
plt.scatter(tiledPCA[:,0],tiledPCA[:,1],c=z.Color,marker ="o",s=40,alpha = 0.5)
xlabel="PCA Component 1"
ylabel="PCA Component 2"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.savefig("1KADPCA12.png",format='png')

plt.figure
plt.scatter(tiledPCA[:,1],tiledPCA[:,2],c=z.Color,marker ="o",s=40,alpha = 0.5)
xlabel="PCA Component 2"
ylabel="PCA Component 3"
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.savefig("1KADPCA23.png",format='png')
