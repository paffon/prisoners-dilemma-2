from itertools import combinations

from _debuggable import Debuggable

from game import Game

class Tournament(Debuggable):
    def __init__(self,
                 players,
                 games_between_each_two_players: int = 0,
                 rounds_per_game: int = 0,
                 error_rate: float = .0,
                 top_percentage: float = .1,
                 survival_bias: float = .0,
                 debug: bool = False):

        super().__init__(debug=debug)

        self.players = players
        self.games_between_each_two_players = games_between_each_two_players
        self.rounds_per_game = rounds_per_game
        self.error_rate = error_rate
        self.top_percentage = top_percentage
        self.survival_bias = survival_bias

    def go(self, summarize_tournament: bool = False):
        all_tuples = list(combinations(self.players, 2))
        for player_1, player_2 in all_tuples:
            Game(player_1=player_1,
                 player_2=player_2,
                 rounds_per_game=self.rounds_per_game,
                 error_rate=self.error_rate,
                 debug=self.debug).go()
        # TODO add a tournament summary routine