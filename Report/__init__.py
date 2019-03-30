class Report:
    '''
    Report that states the context and how well the node performed at that.
    '''
    def __init__(self, service=0, capability=0, note=0, time=0):
        self.service = service
        self.capability = capability
        self.note = note
        self.time = time

    def csv_output(self):
        '''
        Output contained data in a format suitable for a csv
        '''
        return f"{self.service},{self.capability},{self.note},{self.time}"
