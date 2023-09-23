class Debuggable:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def print(self, string: object):
        if self.debug:
            print(string)