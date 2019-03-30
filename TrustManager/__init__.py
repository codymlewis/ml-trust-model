import numpy as np

import Functions
import Node
import BadMouther


class TrustManager:
    '''
    Create and control the network.
    '''
    def __init__(self, no_of_nodes=200, constrained_nodes=0.5,
                 poor_witnesses=0.2, malicious_nodes=0.1):
        self.network = []
        constrained_list = Functions.get_conditioned_ids(
            no_of_nodes, constrained_nodes
        )
        poor_witness_list = Functions.get_conditioned_ids(
            no_of_nodes, poor_witnesses
        )
        malicious_list = Functions.get_conditioned_ids(
            no_of_nodes, malicious_nodes
        )

        for i in range(no_of_nodes):
            if i in constrained_list:
                service = np.round(np.random.rand())
                capability = np.round(np.random.rand())
            else:
                service = 100
                capability = 100
            note_acc = np.random.rand() if i in poor_witness_list else 1.0
            if i in malicious_list:
                self.network.append(
                    BadMouther.BadMouther(service, capability, note_acc)
                )
            else:
                self.network.append(Node.Node(service, capability, note_acc))

        self.reports = [
            [[] for _ in range(no_of_nodes)] for _ in range(no_of_nodes)
        ]

    def bootstrap(self, epochs=100):
        '''
        Go through the network and perform artificial transactions to develop
        reports.
        '''
        print(f"\nBootstrapping network for {epochs} epochs:")
        Functions.print_progress(0, epochs)
        for i in range(1, epochs + 1):
            self._artificial_transactions(i)
            Functions.print_progress(i, epochs)
        print("Done.")

    def _artificial_transactions(self, current_epoch):
        '''
        Perform some transactions through the entire network with random
        targets.
        '''
        for i_node_i in enumerate(self.network):
            for j_node_j in enumerate(self.network):
                if i_node_i[0] != j_node_j[0]:
                    service_target = np.round(np.random.rand() * 100)
                    capability_target = np.round(np.random.rand() * 100)
                    self.reports[i_node_i[0]][j_node_j[0]].append(
                        i_node_i[1].send_report(
                            j_node_j[1],
                            service_target,
                            capability_target,
                            current_epoch
                        )
                    )

    def save_reports_csv(self, filename="reports.csv"):
        '''
        Save a csv on the report data
        '''
        with open(filename, "w") as report_csv:
            for reports_from_node_i in enumerate(self.reports):
                for reports_on_node_j in enumerate(reports_from_node_i[1]):
                    for report in reports_on_node_j[1]:
                        report_csv.write(
                            f"{reports_from_node_i[0]},{reports_on_node_j[0]},{report.csv_output()}\n"
                        )
