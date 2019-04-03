from sklearn.svm import SVC

'''
Use a Kernel Machine for the trust management.
'''


def create_and_fit_svm(train_inputs, train_labels, c_value, gamma):
    '''
    Create and SVM, fit it to the training data and return it.
    '''
    svm = SVC(C=c_value, kernel='rbf', gamma=gamma)

    svm.fit(train_inputs, train_labels)

    return svm


def find_accuracy(svm, data, labels):
    '''
    Give the accuracy of the svm.
    '''
    classifications = svm.predict(data)
    corrects = 0

    for i_classification in enumerate(classifications):
        if i_classification[1] == labels[i_classification[0]]:
            corrects += 1

    return 100 * corrects / len(labels)
