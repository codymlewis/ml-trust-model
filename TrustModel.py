#!/usr/bin/env python3

import numpy as np

'''
A trust model simulation which uses machine learning techniques to find trust.

Author: Cody Lewis
Date: 2019-03-12
'''


class Report:
    '''
    Report that states the context and how well the node performed at that.
    '''
    def __init__(self, service=0, capability=0, note=0):
        self.service = service
        self.capability = capability
        self.note = note


class Node:
    '''
    A node in the trust managed network
    '''
    def __init__(self, service=100, capability=100, note_acc=1.0):
        self.service = service
        self.capability = capability
        self.note_taking_acc = note_acc  # This is unknown to the trust manager

    def send_report(self, proxy, service_target, capability_target):
        '''
        Create a report on a given proxy.
        '''
        note = self.take_note(proxy, service_target, capability_target)

        return Report(service_target, capability_target, note)

    def take_note(self, proxy, service_target, capability_target):
        if proxy.service >= service_target and \
                proxy.capability >= capability_target:
            note = 1
        elif proxy.service >= service_target or \
                proxy.capability >= capability_target:
            note = 0
        else:
            note = -1

        if np.random.rand() < self.note_taking_acc:
            return note
        return wrong_note(note)


class BadMouther(Node):
    '''
    A bad mouthing malicious node.
    '''
    def take_note(self, proxy, service_target, capability_target):
        return -1


class TrustManager:
    '''
    Create and control the network.
    '''
    def __init__(self, no_of_nodes=200, constrained_nodes=0.5,
                 poor_witnesses=0.2, malicious_nodes=0.1):
        self.network = []
        ids = [i for i in range(no_of_nodes)]
        constrained_list = []
        for _ in range(int(no_of_nodes * constrained_nodes)):
            constrained_list.append(ids.pop(np.random.randint(len(ids))))
        ids = [i for i in range(no_of_nodes)]
        poor_witness_list = []
        for _ in range(int(no_of_nodes * poor_witnesses)):
            poor_witness_list.append(ids.pop(np.random.randint(len(ids))))

        for i in range(no_of_nodes):
            if i in constrained_list:
                service = np.round(np.random.rand())
                capability = np.round(np.random.rand())
            else:
                service = 100
                capability = 100
            note_acc = np.random.rand() if i in poor_witness_list else 1.0
            self.network.append(Node(service, capability, note_acc))

        self.reports = [
            [[] for _ in range(no_of_nodes)] for _ in range(no_of_nodes)
        ]

    def bootstrap(self, epochs=1_000):
        '''
        Go through the network and perform artificial transactions to develop
        reports.
        '''
        for _ in range(epochs):
            self._artificial_transactions()

    def _artificial_transactions(self):
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
                            j_node_j[1], service_target, capability_target
                        )
                    )


def wrong_note(note):
    '''
    Get the wrong note randomly
    '''
    wrong_notes = {-1, 0, 1} - {note}
    return list(wrong_notes)[int(np.round(np.random.rand()))]


if __name__ == '__main__':
    pass
