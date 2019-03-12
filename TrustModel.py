#!/usr/bin/env python3

import numpy as np

class Report:
    def __init__(self, service=0, capability=0, note=0):
        self.service = service
        self.capability = capability
        self.note = note


class Node:
    def __init__(self, service=100, capability=100, note_acc=1.0):
        self.service = service
        self.capability = capability
        self.note_taking_acc = note_acc

    def send_report(self, proxy_service, proxy_capability,
                    service_target, capability_target):
        note = self.take_note(proxy_service, proxy_capability,
                              service_target, capability_target)

        return Report(service_target, capability_target, note)

    def take_note(self, proxy_service, proxy_capability,
                  service_target, capability_target):
        if proxy_service >= service_target and \
                proxy_capability >= capability_target:
            note = 1
        elif proxy_service >= service_target or \
                proxy_service >= capability_target:
            note = 0
        else:
            note = -1

        return note if np.random.rand() < self.note_taking_acc \
            else wrong_note(note)


def wrong_note(note):
    wrong_notes = {-1, 0, 1} - {note}
    return list(wrong_notes)[int(np.round(np.random.rand()))]


if __name__ == '__main__':
    REPORT = Report(50, 50, -1)
    print(f"{REPORT.service}, {REPORT.capability}, {REPORT.note}")
