from sklearn.svm import LinearSVC
import numpy as np
import sys
from sklearn.linear_model import SGDClassifier

print("Loading numpy arrays...")
encoded = np.load(sys.argv[1])
blood_types = np.load(sys.argv[2])
print("Numpy loaded")
from dask_ml.model_selection import GridSearchCV
crange = np.logspace(-4, 1.5, 10).tolist()
param_space = {"alpha": crange}

model = SGDClassifier(penalty='l1', class_weight='balanced', learning_rate='optimal', verbose=1, max_iter=10)
#model = LinearSVC(penalty="l2", dual=False, verbose=1, max_iter=1000)

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
