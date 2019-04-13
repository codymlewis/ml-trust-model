import csv

import numpy as np

import Functions
import Node
import BadMouther
import TrustManager.SVM as SVM
import TrustManager.ANN as ANN

CAP_MAX = 10
SERVICE_MAX = 6


class TrustManager:
    '''
    Create and control the network.
    '''
    def __init__(self, no_of_nodes=50, constrained_nodes=0.5, malicious_nodes=0.1, malicious_reporters=0.1,
                 train_filename="reports-train.csv", test_filename="reports-test.csv"):
        self.__network = []
        self.__train_filename = train_filename
        self.__test_filename = test_filename
        # A real trust model would not be aware of these lists
        # these are for the training
        constrained_list = Functions.get_conditioned_ids(
            no_of_nodes, constrained_nodes
        )
        malicious_node_list = Functions.get_conditioned_ids(
            no_of_nodes, malicious_nodes
        )
        malicious_reporter_list = Functions.get_conditioned_ids(
            no_of_nodes, malicious_reporters
        )

        for i in range(no_of_nodes):
            if i in constrained_list:
                service = int(np.floor(np.random.rand() * SERVICE_MAX))
                capability = int(np.floor(np.random.rand() * CAP_MAX))
            else:
                service = SERVICE_MAX
                capability = CAP_MAX
            if i in malicious_reporter_list:
                self.__network.append(
                    BadMouther.BadMouther(service, capability, i in malicious_node_list)
                )
            else:
                self.__network.append(Node.Node(service, capability, i in malicious_node_list))

        self.__reports = [
            [None for _ in range(no_of_nodes)] for _ in range(no_of_nodes)
        ]

    def set_filenames(self, train_filename, test_filename):
        self.__train_filename = train_filename
        self.__test_filename = test_filename

    def get_network(self):
        return self.__network

    def get_reports(self):
        return self.__reports

    def bootstrap(self, epochs=100, filewrite=True):
        '''
        Go through the network and perform artificial transactions to develop
        reports.
        '''
        print(f"\nBootstrapping network for {epochs} epochs:")
        Functions.print_progress(0, epochs)
        for i in range(1, epochs + 1):
            self.__artificial_transactions(i, self.__train_filename if filewrite else None)
            self.__artificial_transactions(i, self.__test_filename if filewrite else None)
            Functions.print_progress(i, epochs)
        print()
        print("Done.")

    def __artificial_transactions(self, current_epoch, report_filename=None):
        '''
        Perform some transactions through the entire network with random
        targets.
        '''
        for i_node_i in enumerate(self.__network):
            for j_node_j in enumerate(self.__network):
                if i_node_i[0] != j_node_j[0]:
                    service_target = int(np.floor(np.random.rand() * SERVICE_MAX)) + 1
                    capability_target = int(np.floor(np.random.rand() * CAP_MAX)) + 1
                    self.__reports[i_node_i[0]][j_node_j[0]] = i_node_i[1].send_report(
                        j_node_j[1],
                        service_target,
                        capability_target,
                        current_epoch
                    )
        if report_filename:
            self.save_reports_csv(report_filename)

    def save_reports_csv(self, filename):
        '''
        Save a csv on the report data
        '''
        with open(filename, "a") as report_csv:
            for reports_from_node_i in enumerate(self.__reports):
                for reports_on_node_j in enumerate(reports_from_node_i[1]):
                    if reports_from_node_i[0] != reports_on_node_j[0]:
                        report_csv.write(
                            f"{reports_from_node_i[0]},{reports_on_node_j[0]},{reports_on_node_j[1].csv_output()}\n"
                        )

    def train_svm(self):
        '''
        Fit a pair of SVMs to predict expected notes and observer class respectively.
        '''
        train_data, notes = read_data(self.__train_filename)
        note_svm = SVM.create_and_fit_svm(train_data, notes, 5, 0.1)

        return note_svm

    def evolve_svm(self):
        '''
        Perform an evolutionary algorithm to find the optimal values of C and gamma
        for the respective SVMs.
        '''
        train_data, train_notes = read_data(self.__train_filename)
        test_data, test_notes = read_data(self.__test_filename)

        with open("svm_params.csv", "w") as param_file:
            total_reporters = len(train_data.keys())
            progress = 0
            Functions.print_progress(progress, total_reporters)
            for reporter_id in train_data.keys():
                svm_params = SVM.evolve(
                    train_data[reporter_id],
                    train_notes[reporter_id],
                    test_data[reporter_id],
                    test_notes[reporter_id]
                )
                progress += 1
                Functions.print_progress(progress, total_reporters)
                param_file.write(f"{reporter_id},{svm_params}\n")
        print()

    def train_ann(self):
        train_data, train_notes = read_data(self.__train_filename, dict_mode=False)
        test_data, test_notes = read_data(self.__test_filename, dict_mode=False)
        ANN.create_and_train_ann(train_data, train_notes, test_data, test_notes)

    def load_classifiers(self):
        '''
        Load the classifiers for each node in the network.
        '''
        svms = dict()
        data, notes = read_data(self.__train_filename)

        with open("svm_params.csv") as param_file:
            param_reader = csv.reader(param_file)
            for row in param_reader:
                svms[int(row[0])] = SVM.create_and_fit_svm(data, notes, int(row[1]), int(row[2]))

        return svms


def read_data(filename, delimiter=",", dict_mode=True):
    '''
    Read data from a csv of reports.
    '''
    if dict_mode:
        train_data = dict()
        notes = dict()
    else:
        train_data = []
        notes = []

    with open(filename) as report_csv:
        csv_reader = csv.reader(report_csv, delimiter=delimiter)
        for row in csv_reader:
            if dict_mode:
                reporter_id = int(row[0])
                if train_data.get(reporter_id):
                    train_data[reporter_id].append(row[1:-1])
                    notes[reporter_id].append(row[-1])
                else:
                    train_data[reporter_id] = [row[1:-1]]
                    notes[reporter_id] = [row[-1]]
            else:
                train_data.append(row[:-1])
                notes.append(row[-1])

    return train_data, notes
