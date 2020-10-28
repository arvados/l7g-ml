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
       enc = OneHotEncoder(sparse=True, dtype=np.uint16)
       tiledgenomesOHchunk = enc.fit_transform(tiledgenomes[:,min_idx:max_idx])
       [chi2val,pval] = chi2(tiledgenomesOHchunk, y)
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

def chiZygosity(tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff):
    #filter by Pearson chi^2 and return one-hot by tile variant considering zygosity (phases considered together, and 1 column for het tile variant and 1 column for hom tile variant)
    import numpy as np
    import scipy.sparse
    from scipy.sparse import csr_matrix
    from scipy.sparse import hstack
    from sklearn.feature_selection import chi2
    from sklearn.preprocessing import OneHotEncoder

    [m,n] = tilegenomes.shape
    m = m/2
    idx = np.linspace(0,n,num=nparts).astype('int')
    tiledgenomesOH = csr_matrix(np.empty([m, 0]))
    tiledgenomesOHhom = csr_matrix(np.empty([m, 0]))
    pidx = np.empty([0,],dtype='bool')
    pidxhom = np.empty([0,],dtype='bool')

    # calculate in chunks because one-hot calculation hits memory bug when
    # sparse matrix gets too large (also allows user to use smaller memory machine)

    for i in range(0,nparts-1):
       min_idx = idx[ichunk]
       max_idx = idx[ichunk+1]
       enc = OneHotEncoder(sparse=True, dtype=np.uint16)
       tiledgenomesOHchunk = enc.fit_transform(tiledata[:,min_idx:max_idx])
       tiledgenomeOHphasechunk = tiledgenomesOHchunk[0:m,:] + tiledgenomesOHchunk[m:2*m,:]

       idx2 = tiledgenomeOHphasechunk >= 2
       datahom = tiledgenomeOHphasechunk.data
       [rhom,chom] = tiledgenomeOHphasechunk.nonzero()
       idx3 = datahom == 2
       datahom = datahom[idx3]
       rhom = rhom[idx3]
       chom = chom[idx3]
    
       tiledgenomeOHhomchunk = csr_matrix((datahom, (rhom, chom)), tiledgenomeOHphasechunk.shape)
       tiledgenomeOHhomchunk[idx2] = 1

       datahet = tiledgenomeOHphasechunk.data
       [rhom,chom] = tiledgenomeOHphasechunk.nonzero()
       idx4 = datahet == 1
       rhom = rhom[idx4]
       chom = chom[idx4]

       tiledgenomeOHhetchunk = csr_matrix((datahet, (rhom, chom)), tiledgenomeOHphasechunk.shape)

       [chi2valhet,pvalhet] = chi2(tiledgenomesOHhetchunk, y)



       [chi2valhom,pvalhom] = chi2(tiledgenomesOHhomchunk, y)
   

def pcaComponents(tiledgenomes,varvals,n):  
    #calculate top n PCA from one-hot encoded tiled genomes
    import numpy as np
    import scipy.sparse
    from sklearn.decomposition import PCA   
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.preprocessing import StandardScaler
  
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)

    tiledgenomesOH = enc.fit_transform(tiledgenomes)

    # Remove spanning and no call tile variants for each position
    # 0 --> Low Quality Tiles, 1 --> Spanning Tiles
    to_keepPCA = varvals > 1

    idkTKPCA = np.nonzero(to_keepPCA)
    idkTKPCA = idkTKPCA[0]

    tiledgenomesOH = tiledgenomesOH[:,idkTKPCA]
    tiledgenomesOH = tiledgenomesOH.todense()

    pca = PCA(n_components=n)
    tiledPCA = pca.fit_transform(tiledgenomesOH)

    scaler = StandardScaler()
    tiledPCA = scaler.fit_transform(tiledPCA)

    return tiledPCA
