import _helper as helper

from _debuggable import Debuggable
from strategies import Strategy


class Player(Debuggable):
    def __init__(self,
                 name: str = 'Nameless Player',
                 strategy: Strategy = Strategy(),
                 debug: bool = False):

        super().__init__(debug=debug)

        self.name = name
        self.strategy = strategy
        self.score = 0

    def decide(self, my_moves, their_moves):
        strategy = self.strategy
        thoughts, decided_action = strategy.decide(my_moves, their_moves)

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
