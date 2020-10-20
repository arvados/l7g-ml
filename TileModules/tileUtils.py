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


def removeCommonVariant(tiledgenomes,tilepos,idxOP)
    # Remove most common tile variant (tile variant of 0 -- usually reference) at each tile position
    # Note: Assumes you have added +2 to the tiled set so 2 represents most common tile
  
    
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


def chiPhased():  #filter by Pearson chi^2 and return one-hot by tile variant using phase

def chiZygosity():  #filter by Pearson chi^2 and return one-hot by tile variant using zygosity


def pcaComponents(tilegenomes,tilepos):  #create top n PCA components
   
    



