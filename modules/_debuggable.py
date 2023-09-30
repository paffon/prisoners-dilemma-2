class Debuggable:
    def __init__(self, name: str = 'Nameless Debuggable', debug: bool = False):
        self.name = name
        self.debug = debug

    def __repr__(self):
        # Use self.__dict__ to get a dictionary of all instance attributes
        keys_to_include = self.get_keys_to_include_in_representation()
        attrs = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if key in keys_to_include)
        my_name = self.name
        return f"\'{my_name}\' ({attrs})"

    def get_keys_to_include_in_representation(self):
        keys_to_exclude = ['name', 'debug']
        return [key for key in self.__dict__.keys() if key not in keys_to_exclude]

    def display_without_keys(self, keys_to_exclude):
        # Use self.__dict__ to get a dictionary of all instance attributes
        keys_to_include = [key for key in self.__dict__.keys() if key not in keys_to_exclude]
        attrs = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if key in keys_to_include)
        return attrs

    def print(self, string: object):
        if self.debug:
            print(string)
