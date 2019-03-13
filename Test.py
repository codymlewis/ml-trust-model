#!/usr/bin/env python3
import unittest
import numpy as np

import TrustModel

'''
Perform unit tests on the program.

Author: Cody Lewis
Date: 2019-03-12
'''


class TestTrustModel(unittest.TestCase):
    def test_report(self):
        '''
        Test report creation for all possible values
        '''
        for service in range(101):
            for capability in range(101):
                for note in [-1, 0, 1]:
                    self.report_create(service, capability, note)

    def report_create(self, service, capability, note):
        '''
        Test the creation of reports.
        '''
        report = TrustModel.Report(service, capability, note)
        self.assertEqual(report.service, service)
        self.assertEqual(report.capability, capability)
        self.assertEqual(report.note, note)

    def test_wrong_note(self):
        '''
        Test that the wrong note is assigned for each possible note.
        '''
        for note in [-1, 0, 1]:
            self.assertNotEqual(TrustModel.wrong_note(note), note)

    def test_note_take(self):
        '''
        Test that note taking returns the expected values.
        '''
        node = TrustModel.Node()
        proxy = TrustModel.Node()
        self.assertEqual(node.take_note(proxy, 50, 50), 1)
        proxy = TrustModel.Node(100, 1)
        self.assertEqual(node.take_note(proxy, 50, 50), 0)
        proxy = TrustModel.Node(1, 1)
        self.assertEqual(node.take_note(proxy, 50, 50), -1)

    def test_network_creation(self):
        '''
        Test the creation of a network within the trust manager.
        '''
        no_of_nodes = 200
        constrained_nodes = 0.5
        poor_witnesses = 0.2
        malicious_nodes = 0.1
        trust_manager = TrustModel.TrustManager(
            no_of_nodes, constrained_nodes, poor_witnesses, malicious_nodes
        )
        self.assertEqual(len(trust_manager.network), no_of_nodes)
        num_constrained = 0
        num_poor_witnesses = 0
        num_malicious = 0

        for node in trust_manager.network:
            if (node.capability < 100) or (node.service < 100):
                num_constrained += 1
            if node.note_taking_acc < 1.0:
                num_poor_witnesses += 1
            if isinstance(node, TrustModel.BadMouther):
                num_malicious += 1

        self.assertEqual(no_of_nodes * constrained_nodes, num_constrained)
        self.assertEqual(no_of_nodes * poor_witnesses, num_poor_witnesses)
        self.assertEqual(no_of_nodes * malicious_nodes, num_malicious)

    def test_bad_mouther(self):
        '''
        Test the report creation of the bad mouther.
        '''
        proxy = TrustModel.Node(100, 100)
        bad_mouther = TrustModel.BadMouther()
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = TrustModel.Node(1, 100)
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = TrustModel.Node(100, 1)
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = TrustModel.Node(1, 1)
        self.make_report(bad_mouther, proxy, note=-1)

    def make_report(self, client, proxy, service=50, capability=50, note=1):
        '''
        Test that a report matches expected values
        '''
        report = client.send_report(proxy, service, capability)
        self.assertEqual(report.service, service)
        self.assertEqual(report.capability, capability)
        self.assertEqual(report.note, note)

    def test_bootstrap(self):
        trust_manager = TrustModel.TrustManager()
        no_of_transactions = 5

        trust_manager.bootstrap(no_of_transactions)
        self.assertEqual(np.shape(trust_manager.reports), (200, 200))
        for i in range(200):
            for j in range(200):
                if i != j:
                    self.assertEqual(
                        len(trust_manager.reports[i][j]), no_of_transactions
                    )


if __name__ == '__main__':
    unittest.main()
