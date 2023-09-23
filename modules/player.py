import _helper as helper

from _debuggable import Debuggable
from strategies import Strategy


class Player(Debuggable):
    def __init__(self,
                 strategy: Strategy = Strategy(),
                 debug: bool = False):

        super().__init__(debug)

        self.strategy = strategy

        self.score = 0

    def __repr__(self):
        # Use self.__dict__ to get a dictionary of all instance attributes
        keys_to_include = self.get_keys_to_include_in_representation()
        attrs = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if key in keys_to_include)
        return f"Player({attrs})"

    def get_keys_to_include_in_representation(self):
        return [key for key in self.__dict__.keys() if key != 'debug']

    def decide(self, my_moves, their_moves):
        thoughts, decided_action = self.strategy.decide(my_moves, their_moves)

        return thoughts, decided_action

    def update_score(self, my_action, their_action):
        if my_action == 1:
            self.score -= 1

        if their_action == 1:
            self.score += 3

    def copy(self):
        new_player = Player(strategy=self.strategy,
                            debug=self.debug)
        return new_player
