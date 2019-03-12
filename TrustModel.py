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
        self.note_taking_acc = note_acc

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

        return note if np.random.rand() < self.note_taking_acc \
            else wrong_note(note)


def wrong_note(note):
    '''
    Get the wrong note randomly
    '''
    wrong_notes = {-1, 0, 1} - {note}
    return list(wrong_notes)[int(np.round(np.random.rand()))]


if __name__ == '__main__':
    REPORT = Report(50, 50, -1)
    print(f"{REPORT.service}, {REPORT.capability}, {REPORT.note}")
