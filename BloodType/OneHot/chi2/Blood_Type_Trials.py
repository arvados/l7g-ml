import numpy as np
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
filenames = [("blood_type_B_no_filter_no_augmentation_X.npz", "blood_type_B_no_filter_no_augmentation_y.npy"),
             ("blood_type_Rh_chi2_balanced_augmentation_X.npz", "blood_type_Rh_chi2_balanced_augmentation_y.npy"),
             ("blood_type_Rh_chi2_no_augmentation_X.npz", "blood_type_Rh_chi2_no_augmentation_y.npy"),
             ("blood_type_A_chi2_no_augmentation_X.npz", "blood_type_A_chi2_no_augmentation_y.npy"),
             ("blood_type_B_chi2_no_augmentation_X.npz", "blood_type_B_chi2_no_augmentation_y.npy")]

for data, labels in filenames:
    print("Beginning work on another dataset...")
    X = scipy.sparse.load_npz(data)
    y = np.load(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    dataset_name = data[:-6]
    f = open("trials/" + TYPE + "/" + dataset_name + "_" + TYPE + ".txt", "w")
    f.write("Details: LinearSVC with L1 Regularization\n")
    f.write("==========================================================\n")

    crange = np.logspace(-2, 1, 5).tolist()
    print("Training...")

    for C in crange:
        svc_test = LinearSVC(penalty='l1', class_weight='balanced', C=C, dual=False)
        svc_test.fit(X_train, y_train)
        score = svc_test.score(X_test, y_test)
        print("accuracy: %f\n" % score)
        f.write("accuracy: %f\n" % score)
        f.write("C: %f\n" % C)
        d = num_zero(list(svc_test.coef_[0]))
        num_coefficients = len(svc_test.coef_[0])
        percentage_zero = d / num_coefficients

        f.write("Number of zero coefficients: %f\n" % d)
        f.write("Percentage of zero coefficients: %f\n" % percentage_zero)
        f.write("==========================================================\n")

    print("Training completed for this dataset!")
    f.close()

print("Operations have completed and results have been written to disk!")

#======Neural network Trials=======
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
