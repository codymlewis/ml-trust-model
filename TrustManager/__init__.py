import os
import csv

import numpy as np
import joblib
import graphviz
from tensorflow import keras

import Functions
import Node
import BadMouther
import TrustManager.SVM as SVM
import TrustManager.ANN as ANN

CAP_MAX = 10
SERVICE_MAX = 6

'''
Manage the network and establish trust between nodes within it.

Author: Cody Lewis
Date: 2019-03-30
'''


class TrustManager:
    '''
    Create and control the network.
    '''
    def __init__(self, no_of_nodes=50, constrained_nodes=0.5, malicious_nodes=0.1, malicious_reporters=0.1,
                 use_svm=True, train_filename="reports-train.csv", test_filename="reports-test.csv"):
        self.__network = []
        self.__train_filename = train_filename
        self.__test_filename = test_filename
        self.__use_svm = use_svm
        self.__predictor = None
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

    def set_use_svm_flag(self, use_svm):
        self.__use_svm = use_svm

    def get_network(self):
        return self.__network

    def get_reports(self):
        return self.__reports

    def get_no_of_nodes(self):
        return len(self.__network)

    def reset_predictor(self):
        self.__predictor = None

    def save(self):
        if self.__predictor:
            del self.__predictor
        if not os.path.exists("data"):
            os.makedirs("data")
        joblib.dump(self, "data/trust_manager.pkl")

    def bootstrap(self, epochs=100, filewrite=True, verbose=True):
        '''
        Go through the network and perform artificial transactions to develop
        reports.
        '''
        if verbose:
            print(f"\nBootstrapping network for {epochs} epochs:")
            Functions.print_progress(0, epochs)
        for i in range(1, epochs + 1):
            self.__artificial_transactions(i, self.__train_filename if filewrite else None)
            self.__artificial_transactions(i, self.__test_filename if filewrite else None)
            if verbose:
                Functions.print_progress(i, epochs, prefix=f"{i}/{epochs}")
        if verbose:
            print()

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

    def train(self, cont):
        '''
        Train the predictor.
        '''
        if self.__use_svm:
            self.evolve_svm()
            self.load_svms()
        else:
            self.train_ann(cont)
            self.load_ann()

    def evolve_svm(self):
        '''
        Perform an evolutionary algorithm to find the optimal values of C and gamma
        for the respective SVMs.
        '''
        train_data, train_notes = read_data(self.__train_filename)
        test_data, test_notes = read_data(self.__test_filename)

        svms = dict()
        total_reporters = len(train_data.keys())
        progress = 0

        Functions.print_progress(progress, total_reporters, prefix=f"{progress}/{total_reporters}")
        for reporter_id, _ in train_data.items():
            svms[reporter_id] = SVM.evolve(
                train_data[reporter_id], train_notes[reporter_id], test_data[reporter_id], test_notes[reporter_id]
            )
            progress += 1
            Functions.print_progress(progress, total_reporters, prefix=f"{progress}/{total_reporters}")

        if not os.path.exists("data"):
            os.makedirs("data")
        joblib.dump(svms, "data/SVMs.pkl")
        print()

    def train_ann(self, cont):
        '''
        Train the artificial neural network.
        '''
        train_data, train_notes = read_data(self.__train_filename, dict_mode=False)
        test_data, test_notes = read_data(self.__test_filename, dict_mode=False)

        if cont and os.path.exists("data/ANN.h5"):
            self.load_ann()
        ANN.create_and_train_ann(train_data, train_notes, test_data, test_notes,
                                 model=self.__predictor).save("data/ANN.h5")

    def load_svms(self):
        '''
        Load the kernel machine classifiers for each node in the network.
        '''
        self.__predictor = joblib.load("data/SVMs.pkl")

    def load_ann(self):
        '''
        Load the neural network classifier.
        '''
        self.__predictor = dict()
        self.__predictor = keras.models.load_model(f"data/ANN.h5")

    def get_all_recommendations(self, service_target, capability_target):
        '''
        Get all of the predicted recommendations from each node, for each node.
        '''
        trusted_lists = dict()
        no_of_nodes = self.get_no_of_nodes()

        for client_id in range(no_of_nodes):
            if self.__use_svm:
                if not self.__predictor:
                    self.load_svms()
                trusted_lists[client_id] = SVM.get_trusted_list(
                    self.__predictor[client_id], service_target, capability_target, no_of_nodes
                )
            else:
                if not self.__predictor:
                    self.load_ann()
                trusted_lists[client_id] = ANN.get_trusted_list(
                    self.__predictor, client_id, service_target, capability_target, no_of_nodes
                )

        return trusted_lists

    def graph_recommendations(self, client_id, service_target, capability_target):
        '''
        Create a DiGraph of the recommendations for the client at the target service and capability.
        '''
        graph = graphviz.Digraph(comment="Recommendations DiGraph")
        trusted_lists = self.get_all_recommendations(service_target, capability_target)
        for node_id in range(self.get_no_of_nodes()):
            graph.node(
                f"{node_id}",
                f"{node_id}",
                color="red" if self.__network[node_id].is_malicious() else "blue",
                style="filled",
                fontcolor="white"
            )
        for other_node_id, trust_val in trusted_lists[client_id].items():
            graph.edge(
                f"{client_id}",
                f"{other_node_id}",
                color="red" if trust_val == -1 else "purple" if trust_val == 0 else "blue"
            )
        if not os.path.exists("graphs"):
            os.makedirs("graphs")
        predictor_name = "SVM" if self.__use_svm else "ANN"
        graph.render(f"graphs/id{client_id}_s{service_target}_c{capability_target}_{predictor_name}_recommendations.gv", view=False)

    def find_best_servers(self, client_id, service_target, capability_target):
        '''
        Give a list of trusted nodes for the client at the target service and capability.
        '''
        if self.__use_svm:
            if not self.__predictor:
                self.load_svms()
            trusted_list = SVM.get_trusted_list(
                self.__predictor[client_id], service_target, capability_target, len(self.__network)
            )
        else:
            if not self.__predictor:
                self.load_ann()
            trusted_list = ANN.get_trusted_list(
                self.__predictor, client_id, service_target, capability_target, len(self.__network)
            )
        return trusted_list

    def __find_and_rate_best_server(self, client_index, service, capability, predictions):
        '''
        Predict the best server and return the note that the client gives it.
        '''
        good_indices = []
        okay_indices = []

        for index, prediction in predictions[service][capability][client_index].items():
            if index != client_index:
                if prediction == 1:
                    good_indices.append(index)
                elif prediction == 0:
                    okay_indices.append(index)

        if good_indices:
            server_index = good_indices[int(np.floor(np.random.rand() * len(good_indices)))]
            note = self.__network[client_index].take_note(self.__network[server_index], service, capability)
        elif okay_indices:
            server_index = okay_indices[int(np.floor(np.random.rand() * len(okay_indices)))]
            note = self.__network[client_index].take_note(self.__network[server_index], service, capability)
        else:
            note = -1

        return note

    def __simulate_and_rate_trans(self, epochs):
        '''
        Simulate epochs transactions and count the number of various ratings given by clients.
        '''
        bad_transactions = 0
        okay_transactions = 0
        good_transactions = 0
        predictions = dict()

        Functions.print_progress(0, epochs, prefix=f"0/{epochs}")
        for epoch in range(1, epochs + 1):
            service = int(np.floor(np.random.rand() * (SERVICE_MAX + 1)))
            capability = int(np.floor(np.random.rand() * (CAP_MAX + 1)))
            client_index = int(np.floor(np.random.rand() * len(self.__network)))
            if not predictions.get(service):
                predictions[service] = dict()
            if not predictions[service].get(capability):
                predictions[service][capability] = self.get_all_recommendations(service, capability)

            note = self.__find_and_rate_best_server(client_index, service, capability, predictions)

            if note == -1:
                bad_transactions += 1
            elif note == 0:
                okay_transactions += 1
            else:
                good_transactions += 1
            Functions.print_progress(epoch, epochs, prefix=f"{epoch}/{epochs}")
        print()

        return bad_transactions, okay_transactions, good_transactions

    def simulate_transactions(self, epochs):
        '''
        Simulate epochs number of random transactions and return the percentage of bad
        transactions that have occured.
        '''
        print("Simulating transactions...")
        bad_transactions, okay_transactions, good_transactions = self.__simulate_and_rate_trans(epochs)

        return Functions.calc_percentage(bad_transactions, epochs), \
            Functions.calc_percentage(okay_transactions, epochs), \
            Functions.calc_percentage(good_transactions, epochs)

    def time_predict(self):
        '''
        Find the average time it take to make a prediction.
        '''
        client = 1
        server = 2
        service = 1
        capability = 1
        if self.__use_svm:
            if not self.__predictor:
                self.load_svms()
            avg_time = SVM.time_predict(self.__predictor[client], server, service, capability)
        else:
            if not self.__predictor:
                self.load_ann()
            avg_time = ANN.time_predict(self.__predictor, client, server, service, capability)
        return avg_time


def load(train_filename, test_filename, use_svm):
    '''
    Load a previously saved trust manager.
    '''
    trust_manager = joblib.load("data/trust_manager.pkl")

    trust_manager.set_filenames(train_filename, test_filename)
    trust_manager.set_use_svm_flag(use_svm)
    trust_manager.reset_predictor()

    return trust_manager


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
