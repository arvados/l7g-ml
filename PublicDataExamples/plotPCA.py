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

tiledPCA = np.load('tiledPCA.npy')

#header_list = ["number","names","outputname"]
#df = pd.read_csv(namesfile, names=header_list)
#names = df["names"].tolist()
namesfile = "../keep/by_id/37ff79ce0cb92c340e2354350ff623e2+53461/names-GrCh38_1K_set2"
names = np.load(namesfile)
print(names)
myfuncdecode = lambda x: x.decode("utf-8")
names = np.vectorize(myfuncdecode)(names)
names = names.tolist()
print(names)

#names = [i.decode('UTF-8') for i in names] 

cleannames = pgputils.pgpCleanNames(names)
pcaNames = pd.DataFrame(np.column_stack([cleannames, names]),columns=['ID','Filename'])

# Setting Up Colors Based On Geographic Ancestries
ancestry1k = pd.read_csv('igsr_samples.tsv',sep='\t')
ancestry1k = ancestry1k.rename(columns={'Sample name': 'Sample', 'Population code': 'Population'})
ancestryMap = ancestry1k[['Sample','Population']]
ancestryMap['DataSource'] = '1K'
ancestryMap['ID'] = ancestry1k.Sample
ancestryMap['Region'] = ancestry1k.Population
ancestries = ancestryMap[['ID','Region','DataSource']]

z = pcaNames.merge(ancestries, how='left', on='ID')

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
plt.savefig("test1KPCA.png",format='png')
