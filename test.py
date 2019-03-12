#!/usr/bin/env python3
import unittest

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
        self.assertEqual(node.take_note(100, 100, 50, 50), 1)
        self.assertEqual(node.take_note(100, 1, 50, 50), 0)
        self.assertEqual(node.take_note(1, 1, 50, 50), -1)


if __name__ == '__main__':
    unittest.main()
