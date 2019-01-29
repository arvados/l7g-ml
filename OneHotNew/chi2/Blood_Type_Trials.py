import numpy as np
import os
import scipy.sparse
from sklearn import svm, preprocessing, linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras import optimizers
import matplotlib.pyplot as plt
from collections import defaultdict

# utility functions 
def num_zero(lst):
    count = 0
    for x in lst:
        if x == 0:
            count += 1
    return count
    

def SVM_hyperparameter_finder(X, y, num_folds=5):
    crange = np.logspace(-2, 1, 5).tolist()
    param_grid = {'C': crange}
    svm = LinearSVC(penalty='l1', class_weight='balanced', C=C, dual=False)
    grid_search = GridSearchCV(svm, param_grid, cv=num_folds)
    grid_search.fit(X, y)
    print(grid_search.cv_results_)
    return grid_search.best_params_
    
#======SVM Trials=======
TYPE = "svm"
filenames = [("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy")]
#filenames = [("blood_type_B_no_filter_no_augmentation_X.npz", "blood_type_B_no_filter_no_augmentation_y.npy"),
#             ("blood_type_Rh_chi2_balanced_augmentation_X.npz", "blood_type_Rh_chi2_balanced_augmentation_y.npy"),
#             ("blood_type_Rh_chi2_no_augmentation_X.npz", "blood_type_Rh_chi2_no_augmentation_y.npy"),
#             ("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy"),
#             ("blood_type_B_chi2_no_augmentation_X.npz", "blood_type_B_chi2_no_augmentation_y.npy")]

for data, labels in filenames:
    print("Beginning work on another dataset...")
    X = scipy.sparse.load_npz(data)
    y = np.load(labels)

#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    dataset_name = data[:-6]
    directory_name = "trials/" + TYPE
  
    if not os.path.exists(directory_name):
       os.makedirs(directory_name)

    # Loading in path data

    oldpath = np.load(dataset_name+"_oldpath.npy")
    pathdataOH = np.load(dataset_name+"_pathdataOH.npy")
    varvals = np.load(dataset_name+"_varvals.npy")

    f = open("trials/" + TYPE + "/" + dataset_name + "_" + TYPE + ".txt", "w+")
    f.write("Details: LinearSVC with L1 Regularization\n")
    f.write("==========================================================\n")

    crange = np.logspace(-2, 0, 10).tolist()
    print("Training...")

    allscores = []
    allstds = []

    for C in crange:
        svc_test = LinearSVC(penalty='l1', class_weight='balanced', C=C, dual=False)
        svc_test.fit(X, y)
#        score = svc_test.score(X_test, y_test)
#        print("accuracy: %f\n" % score)
#        f.write("accuracy: %f\n" % score)
        f.write("C: %f\n" % C)
        d = np.nonzero(svc_test.coef_)[1].shape[0]
        num_coefficients = svc_test.coef_.shape[0]
        percentage_zero = float(d) / float(num_coefficients)

        f.write("Number of zero coefficients: %f\n" % d)
        f.write("Percentage of zero coefficients: %f\n" % percentage_zero)
     
        n = 10
        scores = cross_val_score(svc_test, X, y, cv=n)
        allscores.append(scores.mean())
        allstds.append(scores.std())
        f.write("Accuracy 10-fold: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
        f.write("==========================================================\n")

    # Finding "best" C value

    cMax = crange[-1]
    accMax = allscores[-1] - allstds[-1]

    for x in range(len(crange)-1,1,-1):
       accNew = allscores[x-1]
       if accNew >= accMax:
          accMax = accNew - allstds[x-1]
          cMax = crange[x-1]
          idx = x

    print(idx)
    print(cMax)
    print(allscores[idx])
    print(allstds[idx])

    print("Training completed for this dataset!")

    svc = LinearSVC(penalty='l1', class_weight='balanced', C=cMax, dual=False)
    svc.fit(X, y)
  
    # Examine model coefficents

    maxCoef = np.absolute(svc.coef_).max()

    idxM = np.argmax(np.absolute(svc.coef_))
    numnz = np.nonzero(svc.coef_)[1].shape
    idxNZus = np.nonzero(svc.coef_)[1]
    coefs = svc.coef_[0,:]

    nnzcoefs = coefs[idxNZus]

    idxSort = np.argsort(np.absolute(nnzcoefs))
    idxSort = np.flipud(idxSort)
    idxNZ = idxNZus[idxSort]

    coefPaths = pathdataOH[idxNZ]

    tile_path = np.trunc(coefPaths/(16**5))
    tile_step = np.trunc((coefPaths - tile_path*16**5)/2)
    tile_phase = np.trunc((coefPaths- tile_path*16**5 - 2*tile_step))
    print("Maximum Coefficent (%4.3f):" % maxCoef)
    print("Number of Nonzeros Coefficents (%d)" % numnz)

    tile_loc = np.column_stack((tile_path, tile_step))
    print(tile_loc)
    print(nnzcoefs[idxSort])
    print(oldpath[idxNZ])
    print(varvals[idxNZ])

    f.close()
print("Operations have completed and results have been written to disk!")


exit()

#=====Neural network Trials=======
TYPE = "neural_network"
LEARNING_RATE = .0001
BATCH_SIZE = 10
EPOCHS = 30
CROSS_VALIDATION_FOLDS = 5

isModelSummaryWritten = False
filenames = [("blood_type_B_no_filter_no_augmentation_X.npz", "blood_type_B_no_filter_no_augmentation_y.npy"),
             ("blood_type_Rh_chi2_balanced_augmentation_X.npz", "blood_type_Rh_chi2_balanced_augmentation_y.npy"),
             ("blood_type_Rh_chi2_no_augmentation_X.npz", "blood_type_Rh_chi2_no_augmentation_y.npy"),
             ("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy"),
             ("blood_type_B_chi2_no_augmentation_X.npz", "blood_type_B_chi2_no_augmentation_y.npy")]

def make_classifier():
    global isModelSummaryWritten
    
    model = Sequential()
    model.add(Dense(2, input_dim=X_train.shape[1], activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1, activation='sigmoid', kernel_initializer='he_normal'))
    model.compile(loss='binary_crossentropy', optimizer=optimizers.adam(lr=LEARNING_RATE), metrics=['accuracy'])
    
    if not isModelSummaryWritten:
        model.summary(print_fn=lambda x: f.write(x + '\n'))
        isModelSummaryWritten = True
    return model

for data, labels in filenames:
    global isModelSummaryWritten
    isModelSummaryWritten = False
    
    print("Beginning work on another dataset...")
    X = scipy.sparse.load_npz(data)
    y = np.load(labels)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dataset_name = data[:-6]
    
    f = open("trials/" + TYPE + "/" + dataset_name + "_" + TYPE + ".txt", "w")
    f.write("Details: No hidden layer--only an input and output layer with one relu and one sigmoid activation.\n")
    f.write("Learning Rate: %f\n" % LEARNING_RATE)
    f.write("Batch Size: %f\n" % BATCH_SIZE)
    f.write("==========================================================\n")
    
    classifier = KerasClassifier(build_fn = make_classifier, batch_size=BATCH_SIZE, epochs=EPOCHS)
    scores = cross_val_score(classifier, X, y, cv=CROSS_VALIDATION_FOLDS)
    print("Accuracy 5-fold: %0.2f (+/- %0.2f)\n" % (scores.mean(), scores.std()))
    f.write("Accuracy 5-fold: %0.2f (+/- %0.2f)\n" % (scores.mean(), scores.std()))
    f.close()
print("Operations have completed and results have been written to disk!")

#======Neural network Trials=======
TYPE = "neural_network_2"
LEARNING_RATE = .0001
BATCH_SIZE = 10
EPOCHS = 200
CROSS_VALIDATION_FOLDS = 5
DETAILS = "Details: One hidden layer. Very shallow but still quite different from a linear model\n"

isModelSummaryWritten = False
filenames = [("blood_type_B_no_filter_no_augmentation_X.npz", "blood_type_B_no_filter_no_augmentation_y.npy"),
             ("blood_type_Rh_chi2_balanced_augmentation_X.npz", "blood_type_Rh_chi2_balanced_augmentation_y.npy"),
             ("blood_type_Rh_chi2_no_augmentation_X.npz", "blood_type_Rh_chi2_no_augmentation_y.npy"),
             ("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy"),
             ("blood_type_B_chi2_no_augmentation_X.npz", "blood_type_B_chi2_no_augmentation_y.npy")]


def make_classifier():
    global isModelSummaryWritten
    
    model = Sequential()
    model.add(Dense(5, input_dim=X_train.shape[1], activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(10, activation='sigmoid', kernel_initializer='he_normal'))
    model.add(Dense(1, activation='sigmoid', kernel_initializer='he_normal'))
    model.compile(loss='binary_crossentropy', optimizer=optimizers.adam(lr=LEARNING_RATE), metrics=['accuracy'])
    
    if not isModelSummaryWritten:
        model.summary(print_fn=lambda x: f.write(x + '\n'))
        isModelSummaryWritten = True
    return model

for data, labels in filenames:
    global isModelSummaryWritten
    isModelSummaryWritten = False
    
    print("Beginning work on another dataset...")
    X = scipy.sparse.load_npz(data)
    y = np.load(labels)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    dataset_name = data[:-6]
    
    f = open("trials/" + TYPE + "/" + dataset_name + "_" + TYPE + ".txt", "w")
    f.write(DETAILS)
    f.write("Learning Rate: %f\n" % LEARNING_RATE)
    f.write("Batch Size: %f\n" % BATCH_SIZE)
    f.write("Number of Epochs: %f\n" % EPOCHS)
    f.write("==========================================================\n")
    
    classifier = KerasClassifier(build_fn = make_classifier, batch_size=BATCH_SIZE, epochs=EPOCHS)
    scores = cross_val_score(classifier, X, y, cv=CROSS_VALIDATION_FOLDS)
    print("Accuracy 5-fold: %0.2f (+/- %0.2f)\n" % (scores.mean(), scores.std()))
    f.write("Accuracy 5-fold: %0.2f (+/- %0.2f)\n" % (scores.mean(), scores.std()))
    f.close()
print("Operations have completed and results have been written to disk!")
