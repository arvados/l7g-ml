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

def randomizePhase(tiledgenomes)
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
    idxKeep = fracnnz[idx3] >= qual
    tiledgenomes = tiledgenomes[:, idxKeep]
    tilepos = tilepos[idxKeep]
    idxOP = idxOP[idxKeep]

    return tiledgenomes, tilepos, idxOP

    
def findTileVars(tiledgenomes,tilepos,idxOP)
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

    tileposOH = np.repeat(tilepos[idxKeep], invals)
    idxOPOH = np.repeat(idxOP[idxKeep], invals)

    return tileposOH, idxOPOH, varvals


def chiPhased(tiledgenomes,tileposOH,idxOPOH,varvals,y,nparts,pcutoff): 
    #filter by Pearson chi^2 and return one-hot by tile variant with each phase represented seperately

    data_shape = tiledgenomes.shape[1]
    idx = np.linspace(0,data_shape,num=parts).astype('int')
    tiledgenomesOH = csr_matrix(np.empty([tiledgenomes.shape[0], 0]))
    pidx = np.empty([0,],dtype='bool')

    # calculate in chunks because one-hot calculation hits memory bug when
    # sparse matrix gets too large (also allows user to use smaller memory machine)

    for i in range(0,nparts-1):
       min_idx = idx[i]
       max_idx = idx[i+1]
       enc = OneHotEncoder(sparse=True, dtype=np.uint16, categories='auto')
       tiledgenomeOHchunk = enc.fit_transform(tilegenomes[:,min_idx:max_idx])
       [chi2val,pval] = chi2(tiledgenomesOHchunk, y)
       pidxchunk = pval <= pcutoff 
       tiledgenomeOHchunkfiltered = tiledgenomeOHchunk[:,pidxchunk]
       pidx = np.concatenate((pidx,pidxchunk),axis=0)

       if i == 0:
           tiledgenomesOH = tiledgenomeOHchunk 
       else:
           tiledgenomesOH  = hstack([tiledgenomesOH,tiledgenomeOHchunk],format='csr')

       tileposOH = tileposOH[pidx]
       varvals = varvals[pidx]

       to_keep = varvals > 2
       idkTK = np.nonzero(to_keep)
       idkTK = idkTK[0]

       tiledgenomesOH = tiledgenomesOH[:,idkTK]
       tileposOH = tileposOH[idkTK]
       varvals = varvals[idkTK]
       idxOPOH = idxOPOH[idxTK]

       return tiledgenomesOH, tileposOH, varvals, idxOPOH

def chiZygosity():  #filter by Pearson chi^2 and return one-hot by tile variant using zygosity


def pcaComponents(tilegenomes,varvals,n):  
    #calculate top n PCA from one-hot encoded tiled genomes
    import numpy as np
    import scipy.sparse
    from sklearn.decomposition import PCA   
  
    enc = OneHotEncoder(sparse=True, dtype=np.uint16)

    XtrainPCA = enc.fit_transform(tiledataPCA)

    # Remove spanning and no call tile variants for each position
    # 0 --> Low Quality Tiles, 1 --> Spanning Tiles
    to_keepPCA = varvalsPCA > 1

    idkTKPCA = np.nonzero(to_keepPCA)
    idkTKPCA = idkTKPCA[0]

    XtrainPCA = XtrainPCA[:,idkTKPCA]
    XtrainPCA = XtrainPCA.todense()

    tiledgenomesOH = tiledgenomesOH.todense()
    pca = PCA(n_components=n)
    tiledPCA = pca.fit_transform(tiledgenomesOH)

    scaler = StandardScaler()
    tiledPCA= scaler.fit_transform(tiledPCA)

    return tiledPCA
