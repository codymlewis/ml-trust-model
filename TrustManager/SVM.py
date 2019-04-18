import numpy as np
from sklearn.svm import SVC

import Functions

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


def get_trusted_list(svm, service_target, capability_target, no_of_nodes):
    '''
    Get the list of nodes that client trusts for a given target service, and capability.
    '''
    trusted_list = dict()

    for i in range(no_of_nodes):
        trusted_list[i] = int(svm.predict([[i, service_target, capability_target]])[0])

    return trusted_list


def time_predict(svm, node_id, service_target, capability_target):
    '''
    Find the average time to predict.
    '''
    predict = Functions.wrap_func(svm.predict, [[node_id, service_target, capability_target]])
    return Functions.time(predict)


def evolve(train_inputs, train_labels, test_inputs, test_labels):
    '''
    Perform an evolutionary algorithm to optimize SVM parameters.
    '''
    genome = hill_climb(
        train_inputs, train_labels, test_inputs, test_labels
    )
    return create_and_fit_svm(train_inputs, train_labels, genome[0], genome[1])


def normalise_genome(genome):
    '''
    Make sure the genome does not have invalid input.
    '''
    for index_gene in enumerate(genome):
        while genome[index_gene[0]] <= 0:
            genome[index_gene[0]] = float(np.random.normal(10, 8, 1))


def generate_genome():
    '''
    Generate a random starting genome.
    '''
    return [float(np.random.normal(50, 2)), float(np.random.normal(1, 0.5))]


def mutate_genome(genome):
    '''
    Take a genome and mutate it, return the mutant.
    '''
    step_size = 0.1 * np.random.normal(0, 5)
    mutant_genome = genome.copy()

    if np.random.normal() < 0:
        step_size = 3 * np.random.normal(0, 5)

    for index_mutant_genome in enumerate(mutant_genome):
        mutant_genome[index_mutant_genome[0]] += float(step_size * np.random.normal(0, 1))

    return mutant_genome


def hill_climb(train_inputs, train_labels, test_inputs, test_labels, acc_goal=99):
    '''
    Evolutionary algorithm to find the optimal parameters for the SVM.
    '''
    counter = 0
    n_epochs = 10_000
    genome = generate_genome()
    normalise_genome(genome)
    svm_champ = create_and_fit_svm(
        train_inputs, train_labels, genome[0], genome[1]
    )
    acc_champ = find_accuracy(svm_champ, test_inputs, test_labels)

    while (acc_champ < acc_goal) and (counter < n_epochs):
        mutant_genome = mutate_genome(genome)
        normalise_genome(mutant_genome)
        svm_mutant = create_and_fit_svm(
            train_inputs, train_labels, mutant_genome[0], mutant_genome[1]
        )
        acc_mutant = find_accuracy(svm_mutant, test_inputs, test_labels)

        if acc_mutant > acc_champ:
            genome = mutant_genome
            acc_champ = acc_mutant
        counter += 1
    return genome
