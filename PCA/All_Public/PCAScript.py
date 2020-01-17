import numpy as np
import scipy as scipy
import scipy.sparse
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix, hstack
from scipy.sparse import csr_matrix, vstack

#a = np.full(1008, True)
#a[186] = False
#a[187] = False
#a[193] = False
#a[198] = False
X = scipy.sparse.load_npz('/home/sarah/keep/by_id/e206007c5c245a0decd02eb2f8599dbb+135/XtrainPCA.npz')
X = X.todense()
print(X.shape)
#quit()
#X2 = X[0:274,:]
#X3 = X[639:1004,:]
#Xfinal = vstack([X2,X3])
X.shape
#svd = TruncatedSVD(n_components=4)
pca = PCA(n_components=3)
X = pca.fit_transform(X)
print(pca.singular_values_)
np.save('XfinalPCAAllNewCombine.npy',X)
