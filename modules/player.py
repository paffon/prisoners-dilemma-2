from _debuggable import Debuggable
from strategies import Strategy


class Player(Debuggable):
    def __init__(self,
                 name: str = 'Nameless Player',
                 strategy: Strategy = Strategy(),
                 generation: int = 0,
                 score: int = 0,
                 debug: bool = False):

        super().__init__(debug=debug)

        self.name = name
        self.generation = generation
        self.display_name = f'{self.name} (gen: {generation})'
        self.strategy = strategy
        self.score = score

    def decide(self, my_moves, their_moves):
        strategy = self.strategy
        thoughts, decided_action = strategy.decide(my_moves, their_moves)

        return thoughts, decided_action

    def update_score(self, my_action, their_action):
        if my_action == 1:
            self.score -= 1

        if their_action == 1:
            self.score += 3

    def give_birth(self):
        new_player = Player(name=self.name,
                            generation=self.generation + 1,
                            strategy=self.strategy,
                            debug=self.debug)
        return new_player
