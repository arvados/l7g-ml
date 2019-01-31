from sklearn.svm import SVC
import numpy as np
import sys
from sklearn.linear_model import SGDClassifier

print("Loading numpy arrays...")
encoded = np.load(sys.argv[1])
blood_types = np.load(sys.argv[2])
print("Numpy loaded")
from dask_ml.model_selection import GridSearchCV
crange = np.logspace(-4, 3, 15).tolist()
param_space = {"C": crange}

model = SVC(class_weight='balanced', kernel='linear', verbose=1)

#search = GridSearchCV(model, param_space, cv=5, n_jobs=4, pre_disptch="2*n_jobs")
search = GridSearchCV(model, param_space, cv=5, n_jobs=5)
print("Fitting...")
try:
	search.fit(encoded, blood_types)
except Exception as e:
	print("Error: " + str(e))
print(search.best_params_)
from sklearn.externals import joblib
joblib.dump(search, "search.pkl")
