'''
Class for reports, which state the context of a service and rates it.
'''


class Report:
    '''
    Report that states the context and how well the node performed at that.
    '''
    def __init__(self, service=0, capability=0, note=0, time=0):
        self.__service = service
        self.__capability = capability
        self.__note = note
        self.__time = time

    def get_service(self):
        return self.__service

    def get_capability(self):
        return self.__capability

    def get_note(self):
        return self.__note

    def get_time(self):
        return self.__time

    def csv_output(self):
        '''
        Output contained data in a format suitable for a csv
        '''
        return f"{self.__service},{self.__capability},{self.__note}"
