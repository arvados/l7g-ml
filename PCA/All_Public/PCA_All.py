import numpy as np
import scipy as scipy
import scipy.sparse
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix, hstack
from scipy.sparse import csr_matrix, vstack
import argparse

def pca_all():


   parser = argparse.ArgumentParser()
   parser.add_argument('tilefile', metavar='TILEFILE', help='File containing files of tile var matrix')
 
   args = parser.parse_args()
   tilefile = args.tilefile

#   tilefile = '/home/sarah/keep/by_id/bb4671471a0e3a7dd9440d18637959e3+640/XtrainPCA.npz'
   X = scipy.sparse.load_npz(tilefile)
   X = X.todense()
   print(X.shape)
   pca = PCA(n_components=3)
   X = pca.fit_transform(X)
   print(pca.singular_values_)
   np.save('XfinalPCAAllNewCombine.npy',X)

if __name__ == '__main__':
    pca_all()

