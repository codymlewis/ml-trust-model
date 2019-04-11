import numpy as np
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


def evolve(train_inputs, train_labels, test_inputs, test_labels):
    genome, acc = hill_climb(
        train_inputs, train_labels, test_inputs, test_labels
    )
    return f"C: {genome[0]}, gamma: {genome[1]}, accuracy: {acc}"


def normalise_genome(genome):
    for index_gene in enumerate(genome):
        while genome[index_gene[0]] <= 0:
            genome[index_gene[0]] = \
                float(np.random.normal(10, 8, 1))


def generate_genome():
    '''
    Generate a random starting genome.
    '''
    return [float(g) for g in list(np.random.normal(50, 20, 2))]


def mutate_genome(genome):
    '''
    Take a genome and mutate it, return the mutant.
    '''
    step_size = 0.1 * np.random.normal(0, 5)
    mutant_genome = genome.copy()

    if np.random.normal() < 0:
        return generate_genome()  # Introduce annealing

    for index_mutant_genome in enumerate(mutant_genome):
        mutant_genome[index_mutant_genome[0]] += \
            float(step_size * np.random.normal(0, 5))

    return mutant_genome


def crossover(genome_a, genome_b):
    '''
    Possibly crossover genome_b into genome_a and return the result.
    '''
    crossover_genome = []
    crossed_over = False

    for gene_pair in zip(genome_a, genome_b):
        if not crossed_over and np.random.normal() < 0:
            crossover_genome.append(gene_pair[1])
        else:
            crossover_genome.append(gene_pair[0])

    return crossover_genome


def hill_climb(train_inputs, train_labels, test_inputs, test_labels, acc_goal=99):
    '''
    Evolutionary algorithm to find the optimal number of neurons for the ANN.
    '''
    counter = 0
    n_epochs = 100_000
    genome = generate_genome()
    svm_champ = create_and_fit_svm(
        train_inputs, train_labels, genome[0], genome[1]
    )
    acc_champ = find_accuracy(svm_champ, test_inputs, test_labels)

    while (acc_champ < acc_goal) and (counter < n_epochs):
        mutant_genome = mutate_genome(genome)
        mutant_genome = crossover(mutant_genome, genome)
        print(f"Epoch: {counter}, Current mutant genome: {mutant_genome}, Current champion genome: {genome} at accuracy: {acc_champ}")
        svm_mutant = create_and_fit_svm(
            train_inputs, train_labels, mutant_genome[0], mutant_genome[1]
        )
        acc_mutant = find_accuracy(svm_mutant, test_inputs, test_labels)

        if acc_mutant > acc_champ:
            genome = mutant_genome
            acc_champ = acc_mutant
        counter += 1
    return genome, acc_champ
