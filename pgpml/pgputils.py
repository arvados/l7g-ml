def yloadBlood(ydatabase,bloodtype):
    import numpy as np
    import sqlite3
    import pandas as pd
    import os
    import sys
    import re

    conn = sqlite3.connect(ydatabase)
    c = conn.cursor()
    c.execute('SELECT * FROM demographics')
    rows = c.fetchall()
    colnames = []

    for i in c.description:
       colnames.append(i[0])

    data = pd.DataFrame(rows, columns=colnames)
    conn.close()

    dataBloodType = data[['human_id','blood_type']]
    dataBloodType = dataBloodType.replace('', np.nan, inplace=False)
    dataBloodType = dataBloodType.dropna(axis=0, inplace=False)

    #Encodes blood type to integers
    dataBloodType['A'] = dataBloodType['blood_type'].str.contains('A',na=False).astype(int)
    dataBloodType['B'] = dataBloodType['blood_type'].str.contains('B',na=False).astype(int)
    dataBloodType['O'] = dataBloodType['blood_type'].str.contains('O',na=False).astype(int)
    dataBloodType['Rh'] = dataBloodType['blood_type'].str.contains('\+',na=False).astype(int)

    dataBloodType['y'] = dataBloodType[bloodtype]

    return dataBloodType 

def pgpCleanNames(names):
    import re
   
    names1 = [i.split('/')[-1] for i in names]
    names2 = [i.replace('filtered_','') for i in names1]
    names3 = [i.replace('.haplotypeCalls.er.raw','') for i in names2]
    names4 = [i.replace('_cg_data_ASM','') for i in names3]
    names5 = [i.replace('data_','') for i in names4]
    names6 = [i.replace('.cgf','') for i in names5]
    names7 = [i.split('_var')[0] for i in names6]
    names8 = [i.split('_GS')[0] for i in names7]
    names9 = [i.split('_lcl')[0] for i in names8]
    names10 = [i.split('_blood')[0] for i in names9]
    names11 = [i.split('_buffy')[0] for i in names10]
    names12 = [i.split('_noHLA')[0] for i in names11]
    names13 = [re.sub('_(S1|sorted).genome','',i) for i in names12]
    names14 = [re.sub('_.+-portable', '',i) for i in names13]
    names = names14

    return names
