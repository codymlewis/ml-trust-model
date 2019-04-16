import Node

'''
Class for a bad mouthing node (always reports other nodes as malicious)

Author: Cody Lewis
Date: 2019-03-30
'''


class BadMouther(Node.Node):
    '''
    A bad mouthing malicious node.
    '''
    def take_note(self, proxy, service_target, capability_target):
        '''
        Give a bad mouthed note.
        '''
        if proxy.is_malicious():  # say that other malicious nodes are good
            return 1
        return -1
