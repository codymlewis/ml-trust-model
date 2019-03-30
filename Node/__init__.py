import numpy as np

import Functions
import Report


class Node:
    '''
    A node in the trust managed network.
    '''
    def __init__(self, service=100, capability=100, note_acc=1.0):
        self.service = service
        self.capability = capability
        self.note_taking_acc = note_acc  # This is unknown to the trust manager

    def send_report(self, proxy, service_target, capability_target, time):
        '''
        Create a report on a given proxy.
        '''
        note = self.take_note(proxy, service_target, capability_target)

        return Report.Report(service_target, capability_target, note, time)

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
        return Functions.wrong_note(note)
