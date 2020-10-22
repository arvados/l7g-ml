import numpy as np
from skrebate import ReliefF
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from skrebate.turf import TuRF
import scipy.sparse

print("Loading files...")

# Code for loading files from a google cloud storage bucket

# with tf.gfile.GFile("gs://keen-scion-203518-ml/blood_type_Rh_no_filter_no_augmentation_X.npz") as f:
#     sparse_X = scipy.sparse.load_npz(f)
#     X = sparse_X.toarray()

# with tf.gfile.GFile("gs://keen-scion-203518-ml/blood_type_Rh_no_filter_no_augmentation_y.npy") as f:
#     y = np.load(f)

sparse_X = scipy.sparse.load_npz("blood_type_Rh_no_filter_no_augmentation_X.npz")
X = sparse_X.toarray()[:,:1000]
y = np.load("blood_type_Rh_no_filter_no_augmentation_y.npy")

print("Making pipeline...")
r = TuRF(core_algorithm="ReliefF", n_features_to_select=1000, pct=0.5, verbose=True)

print("Fitting dataset and labels...")
r.fit(X, y, range(X.shape[1]))

np.save("feature_importances.npy", r.feature_importances_)
np.save("top_features.npy", r.top_features_)

print("Complete!")
