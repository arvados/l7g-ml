def yloadAD(ydatafile):
    import numpy as np
    import sqlite3
    import pandas as pd
    import os
    import sys
    import re

    dataADStatus = pd.read_csv(ydatafile,sep='\t')
    dataADStatus['y'] = dataADStatus['AD']

    return dataADStatus

def cleanNamesAD(names):
    import re
   
    names2 = [re.sub('-BL.*','',i) for i in names]
#    names14 = [re.sub('_.+-portable', '',i) for i in names13]
    names = names2
    return names

def syncTilesAD(dfy,names):
    import numpy as np
    import pandas as pd
    import scipy.sparse
    from scipy.sparse import csr_matrix
    from scipy.sparse import hstack
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler

    dfy.SUBJID = dfy.SUBJID.str.lower()
    results = []

    for name in names:
       results.append(name.lower())

    df_names = pd.DataFrame(results,columns={'Sample'})
    df_names['Number'] = df_names.index

    df2 = df_names.merge(dfy,right_on='SUBJID', left_on='Sample', how='inner')
    idx = df2['Number'].values

    print(idx.shape)

    phenoSex = df2['Sex'].values
    phenoSex = np.reshape(phenoSex,(-1, 1))

    phenoAge = df2['Age_baseline']
    phenoAge = phenoAge.replace('90+','90')
    phenoAge = phenoAge.astype('double')
    phenoAge = phenoAge.fillna(value=phenoAge.mean())
    scaler = StandardScaler()
    phenoAge = np.reshape(phenoAge.values,(-1, 1))
    phenoAge = scaler.fit_transform(phenoAge)

    pheno = phenoSex
    pheno = np.hstack((pheno,phenoAge)) 
    y = df2['y'].values

    return y,pheno

def syncTilesADwPCA(dfy,names,PCAnames,tiledPCA):
    import numpy as np
    import pandas as pd
    import scipy.sparse
    from scipy.sparse import csr_matrix
    from scipy.sparse import hstack
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler

    dfy.SUBJID = dfy.SUBJID.str.lower()
    results = []

    for name in names:
       results.append(name.lower())

    dfy.SUBJID = dfy.SUBJID.str.lower()
    dfy.rename(columns = {'SUBJID' : 'Sample'}, inplace = True)

    PCAresults = []

    for PCAname in PCAnames:
       PCAresults.append(PCAname.lower())

    df_names = pd.DataFrame(results,columns={'Sample'})
    df_names['Number'] = df_names.index

    df2 = df_names.merge(dfy,on='Sample', how='inner')
    idx = df2['Number'].values

    df_PCA = pd.DataFrame(PCAresults,columns={'Sample'})
    df_PCA['Number'] = df_PCA.index

    df3 = df2.merge(df_PCA,on='Sample', how='left',suffixes=('_left', '_right'))
    idxPCA = df3['Number_right'].values

    print(df3)
    print(idxPCA)

    tiledPCA = tiledPCA[idxPCA,:]

    phenoSex = df2['Sex'].values
    phenoSex = np.reshape(phenoSex,(-1, 1))

    phenoAge = df2['Age_baseline']
    phenoAge = phenoAge.replace('90+','90')
    phenoAge = phenoAge.astype('double')
    phenoAge = phenoAge.fillna(value=phenoAge.mean())
    scaler = StandardScaler()
    phenoAge = np.reshape(phenoAge.values,(-1, 1))
    phenoAge = scaler.fit_transform(phenoAge)

    pheno = phenoSex
    pheno = np.hstack((pheno,phenoAge))
    y = df2['y'].values

    return y,pheno,tiledPCA

