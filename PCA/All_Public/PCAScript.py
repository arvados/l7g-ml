import numpy as np
import scipy as scipy
import scipy.sparse
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix, hstack
from scipy.sparse import csr_matrix, vstack

a = np.full(1008, True)
# Remove points related to Simons diversity data files that had issues with preprocessing
a[186] = False
a[187] = False
a[193] = False
a[198] = False
X = scipy.sparse.load_npz('/home/sarah/keep/by_id/e8aa8f9f2527c58a2b7b9119a184b12c+429/XtrainPCA.npz')
X = X.todense()
X = X[a,:]
print(X.shape)
X.shape
pca = PCA(n_components=4)
X = pca.fit_transform(X)
print(pca.singular_values_)
np.save('XfinalPCAAll.npy',X)
