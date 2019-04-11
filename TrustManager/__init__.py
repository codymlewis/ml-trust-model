import csv

import numpy as np

import Functions
import Node
import BadMouther
import TrustManager.SVM as SVM


class TrustManager:
    '''
    Create and control the network.
    '''
    def __init__(self, no_of_nodes=50, constrained_nodes=0.5,
                 poor_witnesses=0.2, malicious_nodes=0.1,
                 train_filename="reports-train.csv", test_filename="reports-test_csv"):
        self.__network = []
        self.__train_filename = train_filename
        self.__test_filename = test_filename
        # A real trust model would not be aware of these lists
        # these are for the training
        constrained_list = Functions.get_conditioned_ids(
            no_of_nodes, constrained_nodes
        )
        self.poor_witness_list = Functions.get_conditioned_ids(
            no_of_nodes, poor_witnesses
        )
        self.malicious_list = Functions.get_conditioned_ids(
            no_of_nodes, malicious_nodes
        )

        for i in range(no_of_nodes):
            if i in constrained_list:
                service = np.round(np.random.rand())
                capability = np.round(np.random.rand())
            else:
                service = 100
                capability = 100
            note_acc = np.random.rand() if i in self.poor_witness_list else 1.0
            if i in self.malicious_list:
                self.__network.append(
                    BadMouther.BadMouther(service, capability, note_acc)
                )
            else:
                self.__network.append(Node.Node(service, capability, note_acc))

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

    def bootstrap(self, epochs=100):
        '''
        Go through the network and perform artificial transactions to develop
        reports.
        '''
        print(f"\nBootstrapping network for {epochs} epochs:")
        Functions.print_progress(0, epochs)
        for i in range(1, epochs + 1):
            self.__artificial_transactions(i)
            Functions.print_progress(i, epochs)
        print("Done.")

    def __artificial_transactions(self, current_epoch, report_filename=None):
        '''
        Perform some transactions through the entire network with random
        targets.
        '''
        for i_node_i in enumerate(self.__network):
            for j_node_j in enumerate(self.__network):
                if i_node_i[0] != j_node_j[0]:
                    service_target = np.round(np.random.rand() * 100)
                    capability_target = np.round(np.random.rand() * 100)
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
                        if reports_from_node_i[0] in self.malicious_list:
                            observer_class = 2
                        elif reports_from_node_i[0] in self.poor_witness_list:
                            observer_class = 1
                        else:
                            observer_class = 0
                        report_csv.write(
                            f"{reports_from_node_i[0]},{reports_on_node_j[0]},{reports_on_node_j[1].csv_output()},{observer_class}\n"
                        )

    def read_data(self, filename, delimiter=","):
        train_data = []
        notes = []
        observer_class = []

        with open(filename) as report_csv:
            csv_reader = csv.reader(report_csv, delimiter=delimiter)
            for row in csv_reader:
                train_data.append(row[:4] + row[5:-1])
                notes.append(row[4])
                observer_class.append(row[-1])

        return train_data, notes, observer_class

    def train_svm(self):
        print("Reading data...")
        train_data, notes, observer_class = self.read_data()
        print("Training SVMs...")
        note_svm = SVM.create_and_fit_svm(train_data, notes, 5, 0.1)
        # witness_svm = SVM.create_and_fit_svm(train_data, observer_class, 5, 0.1)

        return note_svm  # , witness_svm

    def evolve_svm(self):
        data, notes, observer_class = self.read_data()
        return SVM.evolve(data, notes, data, notes)
