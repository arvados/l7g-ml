import numpy as np
import sqlite3
import pandas as pd
import os
import sys
import re

ydatabase = "/data-sdd/cwl_tiling/datafiles/untap.db"
conn = sqlite3.connect(ydatabase)
c = conn.cursor()
c.execute('SELECT * FROM survey')
rows = c.fetchall()
colnames = []

for i in c.description:
  colnames.append(i[0])

data = pd.DataFrame(rows, columns=colnames)
conn.close()

dataLeftEye =  data[data['phenotype_category'].str.contains("Basic_Phenotypes:Left Eye \(Photograph")]
dataRightEye =  data[data['phenotype_category'].str.contains("Basic_Phenotypes:Right Eye \(Photograph")]

dataLeftEye['Blue'] = dataLeftEye['phenotype'].astype('double') < 14
dataRightEye['Blue'] = dataRightEye['phenotype'].astype('double') < 14 

print(dataRightEye)

