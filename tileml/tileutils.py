# Useful Utilites for Working with Tiled Datasets

def removeXYM(tiledgenomes,tilepos,idxOP):
    # Remove tiles in X,Y,M Chromosomes
    import numpy as np

    tilepath = np.trunc(tilepos/(16**5))
    idx22= tilepath <= 810

    tilepos = tilepos[idx22]
    tiledgenomes = tiledgenomes[:,idx22]
    idxOP = idxOP[idx22]

    return tiledgenomes, tilepos, idxOP

def syncTiles(dfy,tiledgenomes,names): 
    import numpy as np
    import pandas as pd

    dfy.human_id = dfy.human_id.str.lower()
    results = []

    for name in names:
       results.append(name.lower())

    df_names = pd.DataFrame(results,columns={'Sample'})
    df_names['Number'] = df_names.index

    df2 = df_names.merge(dfy,left_on = 'Sample', right_on='human_id', how='inner')
    idx = df2['Number'].values

    tiledgenomes = tiledgenomes[idx,:]
    y = df2['y'].values

    return tiledgenomes, y    

def randomizePhase(tiledgenomes):
    import numpy as np

    [m,n] = tiledgenomes.shape

    for ix in range(m):
       n20 = int(n/4)
       ieven = (np.random.randint(0,int(n/2),size=n20)) * 2
       keepa = tiledgenomes[ix,ieven]
       keepb = tiledgenomes[ix,ieven+1]
       tiledgenomes[ix,ieven] = keepb
       tiledgenomes[ix,ieven+1] = keepa
       del keepa,keepb

    return tiledgenomes

def qualCutOff(tiledgenomes,tilepos,idxOP,qual): 
    # Keep positions where qual% of the tiles at the position are high quality tiles 
    # Note: Assumes you have added +2 to the tiled set so 0 represents low quality tile placeholder
    import numpy as np

    nnz = np.count_nonzero(tiledgenomes, axis=0)
    fracnnz = np.divide(nnz.astype(float), tiledgenomes.shape[0])
    [m,n] = tiledgenomes.shape
    idxKeep = fracnnz >= qual
    tiledgenomes = tiledgenomes[:, idxKeep]
    tilepos = tilepos[idxKeep]
    idxOP = idxOP[idxKeep]
    print(tilepos.shape)

    return tiledgenomes, tilepos, idxOP

    
def findTileVars(tiledgenomes,tilepos,idxOP):
    # Compute array of tile variants, tile positions, and original indices for a given set of tiled genomes
    # that would match the set of 1-hot data generated from that set of tile genomes
    import numpy as np

    varvals = np.full(50*tiledgenomes.shape[1],np.nan)
    nx = 0

    varlist = []

    for j in range(0,tiledgenomes.shape[1]):
        u = np.unique(tiledgenomes[:,j])
        varvals[nx:nx+u.size] = u
        nx = nx + u.size
        varlist.append(u)

    varvals = varvals[~np.isnan(varvals)]

    def foo(col):
        u = np.unique(col)
        nunq = u.shape
        return nunq

    invals = np.apply_along_axis(foo, 0, tiledgenomes)
    invals = invals[0]

    tileposOH = np.repeat(tilepos, invals)
    idxOPOH = np.repeat(idxOP, invals)

    return tileposOH, idxOPOH, varvals


def chiPhased(tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff): 
    #filter by Pearson chi^2 and return one-hot by tile variant with each phase represented seperately
    import numpy as np
    import scipy.sparse
    from scipy.sparse import csr_matrix
    from scipy.sparse import hstack
    from sklearn.feature_selection import chi2
    from sklearn.preprocessing import OneHotEncoder

    data_shape = tiledgenomes.shape[1]
    idx = np.linspace(0,data_shape,num=nparts).astype('int')
    tiledgenomesOH = csr_matrix(np.empty([tiledgenomes.shape[0], 0]))
    pidx = np.empty([0,],dtype='bool')

    # calculate in chunks because one-hot calculation hits memory bug when
    # sparse matrix gets too large (also allows user to use smaller memory machine)

    for i in range(0,nparts-1):
       min_idx = idx[i]
       max_idx = idx[i+1]
       enc = OneHotEncoder(sparse=True)
       tiledgenomesOHchunk = enc.fit_transform(tiledgenomes[:,min_idx:max_idx])
       [chi2val,pval] = chi2(tiledgenomesOHchunk.astype(numpy.float), y.astype(numpy.float))
       pidxchunk = pval <= pcutoff 
       tiledgenomesOHchunkfiltered = tiledgenomesOHchunk[:,pidxchunk]
       pidx = np.concatenate((pidx,pidxchunk),axis=0)

       if i == 0:
           tiledgenomesOH = tiledgenomesOHchunkfiltered 
       else:
           tiledgenomesOH = hstack([tiledgenomesOH,tiledgenomesOHchunkfiltered],format='csr')

    tileposOH = tileposOH[pidx]
    varvals = varvals[pidx]
    idxOPOH = idxOPOH[pidx]

    # Remove spanning , no call tile variants, most common tile variant (usually ref) for each position
    # 0 --> Low Quality Tiles, 1 --> Spanning Tiles, 2--> Most Common Tile Variant (Usually Ref)

    to_keep = varvals > 2
    idkTK = np.nonzero(to_keep)
    idkTK = idkTK[0]
    tiledgenomesOH = tiledgenomesOH[:,idkTK]
    tileposOH = tileposOH[idkTK]
    varvals = varvals[idkTK]
    idxOPOH = idxOPOH[idkTK]

    return tiledgenomesOH, tileposOH, varvals, idxOPOH

def chiZygosity(tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff, zygosityreturn=False):
    #filter by Pearson chi^2 and return one-hot by tile variant considering zygosity (phases considered together, and 1 column for het tile variant and 1 column for hom tile variant)
    import numpy as np
    import scipy.sparse
    from scipy.sparse import csr_matrix
    from scipy.sparse import hstack
    from sklearn.feature_selection import chi2
    from sklearn.preprocessing import OneHotEncoder
    print('inside zygosity')

    data_shape = tiledgenomes.shape
    m = int(data_shape[0]/2)
    n = int(data_shape[1]*2)
    
    idx = np.linspace(0,data_shape[1],num=nparts).astype('int')
       
    idxNN = np.logical_not(np.isnan(y))
    y = y[idxNN] 
    yshape = y.shape
    ym = yshape[0]

    tiledgenomesOHhet = csr_matrix(np.empty([ym, 0]))
    tiledgenomesOHhom = csr_matrix(np.empty([ym, 0]))
    pidxhet = np.empty([0,],dtype='bool')
    pidxhom = np.empty([0,],dtype='bool')
    zygosity_het = np.empty([0,],dtype='int')
    zygosity_hom = np.empty([0,],dtype='int')

    # calculate in chunks because one-hot calculation hits memory bug when
    # sparse matrix gets too large (also allows user to use smaller memory machine)

    for i in range(0,nparts-1):
       min_idx = idx[i]
       max_idx = idx[i+1]
       enc = OneHotEncoder(sparse=True, dtype=np.uint16)
       tiledgenomesOHchunk = enc.fit_transform(tiledgenomes[:,min_idx:max_idx])
       tiledgenomesOHphasechunk = tiledgenomesOHchunk[0:m,:] + tiledgenomesOHchunk[m:2*m,:] 
       datahom = tiledgenomesOHphasechunk.data
       [rhom,chom] = tiledgenomesOHphasechunk.nonzero()
       idx2 = tiledgenomesOHphasechunk >=2
       idx3 = datahom == 2
#       datahom[idx3] = 1
       datahom = datahom[idx3]
       rhom = rhom[idx3]
       chom = chom[idx3]

       # creating sparse matrix 1-hot representation of where tile variant is hom    
       tiledgenomesOHhomchunk = csr_matrix((datahom, (rhom, chom)), tiledgenomesOHphasechunk.shape)
       tiledgenomesOHhomchunk[idx2] = 1

       datahet = tiledgenomesOHphasechunk.data
       [rhom,chom] = tiledgenomesOHphasechunk.nonzero()
       idx4 = datahet == 1
       datahet = datahet[idx4]
       rhom = rhom[idx4]
       chom = chom[idx4]

       # creating sparse matrix 1-hot representation of where each tile variant is het
       tiledgenomesOHhetchunk = csr_matrix((datahet, (rhom, chom)), tiledgenomesOHphasechunk.shape)

       tiledgenomesOHhetchunk = tiledgenomesOHhetchunk[idxNN,:]
       tiledgenomesOHhomchunk = tiledgenomesOHhomchunk[idxNN,:]
       
       [chi2valhet,pvalhetchunk] = chi2(tiledgenomesOHhetchunk, y)
       pidxchunkhet = pvalhetchunk <= pcutoff

       tiledgenomesOHhetchunkfiltered = tiledgenomesOHhetchunk[:,pidxchunkhet]
       chunkhetsize = np.shape(tiledgenomesOHhetchunkfiltered)
       zygosity_chunkhet = np.ones((chunkhetsize[1],), dtype=int)
       pidxhet = np.concatenate((pidxhet,pidxchunkhet),axis=0)

       [chi2valhom,pvalhomchunk] = chi2(tiledgenomesOHhomchunk, y)

       pidxchunkhom = pvalhomchunk <= pcutoff
       tiledgenomesOHhomchunkfiltered = tiledgenomesOHhomchunk[:,pidxchunkhom]
       chunkhomsize = np.shape(tiledgenomesOHhomchunkfiltered)
       zygosity_chunkhom = int(2)*np.ones((chunkhomsize[1],), dtype=int)
       pidxhom = np.concatenate((pidxhom,pidxchunkhom),axis=0)
       

       tiledgenomesOHhet = hstack([tiledgenomesOHhet,tiledgenomesOHhetchunkfiltered],format='csr')
       tiledgenomesOHhom = hstack([tiledgenomesOHhom,tiledgenomesOHhomchunkfiltered],format='csr')
       zygosity_hom = np.concatenate((zygosity_hom,zygosity_chunkhom),axis=0)
       zygosity_het = np.concatenate((zygosity_het,zygosity_chunkhet),axis=0)
       pvalhom = np.concatenate((pvalhom,pvalhomchunk),axis=0) 
       pvalhet = np.concatenate((pvalhet,pvalhetchunk),axis=0)

    tileposOHhet = tileposOH[pidxhet]
    varvalshet = varvals[pidxhet]
    idxOPOHhet = idxOPOH[pidxhet]
    pvalhet = pvalhet[pidxhet]

    tileposOHhom = tileposOH[pidxhom]
    varvalshom = varvals[pidxhom]
    idxOPOHhom = idxOPOH[pidxhom]
    pvalhom = pvalhom[pidxhom]

    tileposOH = np.concatenate((tileposOHhet,tileposOHhom),axis=0)
    varvals = np.concatenate((varvalshet,varvalshom),axis=0)
    idxOPOH = np.concatenate((idxOPOHhet,idxOPOHhom),axis=0)
    zygosity = np.concatenate((zygosity_het,zygosity_hom),axis=0)
    pval = np.concatenate((pvalhet,pvalhom),axis=0)

    tiledgenomesOH = hstack([tiledgenomesOHhet,tiledgenomesOHhom],format='csr')
    # Remove spanning , no call tile variants, most common tile variant (usually ref) for each position
    # 0 --> Low Quality Tiles, 1 --> Spanning Tiles, 2--> Most Common Tile Variant (Usually Ref)

    to_keep = varvals > 2
    idkTK = np.nonzero(to_keep)
    idkTK = idkTK[0]

    tiledgenomesOH = tiledgenomesOH[:,idkTK]
    tileposOH = tileposOH[idkTK]
    varvals = varvals[idkTK]
    idxOPOH = idxOPOH[idkTK]
    pval = pvals[idxTK]
    zygosity = zygosity[idxTK]

    if zygosityreturn:
        return tiledgenomesOH, tileposOH, varvals, idxOPOH, zygosity, pval
    else:
        return tiledgenomesOH, tileposOH, varvals, idxOPOH

def pcaComponents(tiledgenomes,varvals,n):  
    #calculate top n PCA from one-hot encoded tiled genomes
    import numpy as np
    import scipy.sparse
    from sklearn.decomposition import PCA   
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler
  
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)
    print(tilegnomesOH.shape)

    tiledgenomesOH = enc.fit_transform(tiledgenomes)

    # Remove spanning, no call tile and ref variants for each position
    # 0 --> Low Quality Tiles, 1 --> Spanning Tiles, 2 ---> Ref 
    to_keepPCA = varvals > 2 

    idkTKPCA = np.nonzero(to_keepPCA)
    idkTKPCA = idkTKPCA[0]

    tiledgenomesOH = tiledgenomesOH[:,idkTKPCA]
    tiledgenomesOH = tiledgenomesOH.todense()

    print(tilegenomesOH.shape)
    pca = PCA(n_components=n)
    tiledPCA = pca.fit_transform(tiledgenomesOH)

    scaler = StandardScaler()
    tiledPCA = scaler.fit_transform(tiledPCA)

    return tiledPCA
