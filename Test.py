#!/usr/bin/env python3
import unittest
import numpy as np

import Functions
import Report
import Node
import BadMouther
import TrustManager

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
                    for time in range(10):
                        self.report_create(service, capability, note, time)

    def report_create(self, service, capability, note, time):
        '''
        Test the creation of reports.
        '''
        report = Report.Report(service, capability, note, time)
        self.assertEqual(report.get_service(), service)
        self.assertEqual(report.get_capability(), capability)
        self.assertEqual(report.get_note(), note)
        self.assertEqual(report.get_time(), time)
        self.assertEqual(
            report.csv_output(), f"{service},{capability},{note}"
        )

    def test_wrong_note(self):
        '''
        Test that the wrong note is assigned for each possible note.
        '''
        for note in [-1, 0, 1]:
            self.assertNotEqual(Functions.wrong_note(note), note)

    def test_note_take(self):
        '''
        Test that note taking returns the expected values.
        '''
        node = Node.Node(100, 100)
        proxy = Node.Node(100, 100)
        self.assertEqual(node.take_note(proxy, 50, 50), 1)
        proxy = Node.Node(100, 1)
        self.assertEqual(node.take_note(proxy, 50, 50), 0)
        proxy = Node.Node(1, 1)
        self.assertEqual(node.take_note(proxy, 50, 50), -1)

    def test_network_creation(self):
        '''
        Test the creation of a network within the trust manager.
        '''
        no_of_nodes = 200
        constrained_nodes = 0.5
        poor_witnesses = 0.2
        malicious_nodes = 0.1
        trust_manager = TrustManager.TrustManager(no_of_nodes, constrained_nodes, poor_witnesses, malicious_nodes)
        self.assertEqual(len(trust_manager.get_network()), no_of_nodes)
        num_constrained = 0
        num_malicious = 0

        for node in trust_manager.get_network():
            if (node.get_capability() < TrustManager.CAP_MAX) or (node.get_service() < TrustManager.SERVICE_MAX):
                num_constrained += 1
            if isinstance(node, BadMouther.BadMouther):
                num_malicious += 1

        self.assertEqual(no_of_nodes * constrained_nodes, num_constrained)
        self.assertEqual(no_of_nodes * malicious_nodes, num_malicious)

    def test_bad_mouther(self):
        '''
        Test the report creation of the bad mouther.
        '''
        proxy = Node.Node(100, 100)
        bad_mouther = BadMouther.BadMouther(1, 1)
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = Node.Node(1, 100)
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = Node.Node(100, 1)
        self.make_report(bad_mouther, proxy, note=-1)
        proxy = Node.Node(1, 1)
        self.make_report(bad_mouther, proxy, note=-1)

    def make_report(self, client, proxy, service=1,
                    capability=1, note=1, time=0):
        '''
        Test that a report matches expected values
        '''
        report = client.send_report(proxy, service, capability, time)
        self.assertEqual(report.get_service(), service)
        self.assertEqual(report.get_capability(), capability)
        self.assertEqual(report.get_note(), note)
        self.assertEqual(report.get_time(), time)

    def test_bootstrap(self):
        trust_manager = TrustManager.TrustManager(no_of_nodes=50)
        no_of_transactions = 5

        trust_manager.bootstrap(no_of_transactions, False, verbose=False)
        self.assertEqual(np.shape(trust_manager.get_reports()), (50, 50))


if __name__ == '__main__':
    unittest.main()
