import numpy as np

import Functions
import Report

'''
Class for a simulated node in the network.

Author: Cody Lewis
Date: 2019-03-30
'''


class Node:
    '''
    A node in the trust managed network.
    '''
    def __init__(self, service, capability, is_malicious=False):
        self.__service = service
        self.__capability = capability
        self.__is_malicious = is_malicious

    def get_service(self):
        return self.__service

    def get_capability(self):
        return self.__capability

    def is_malicious(self):
        return self.__is_malicious

    def send_report(self, proxy, service_target, capability_target, time):
        '''
        Create a report on a given proxy.
        '''
        note = self.take_note(proxy, service_target, capability_target)

        return Report.Report(service_target, capability_target, note, time)

    def take_note(self, proxy, service_target, capability_target):
        '''
        Take note of the service that the proxy provided.
        '''
        if proxy.is_malicious():
            note = -1
        elif proxy.get_service() >= service_target and \
                proxy.get_capability() >= capability_target:
            note = 1
        elif proxy.get_service() >= service_target or \
                proxy.get_capability() >= capability_target:
            note = 0
        else:
            note = -1

        return note
