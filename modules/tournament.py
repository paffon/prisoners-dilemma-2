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

    def go(self, game_printouts_instructions: dict, summarize_tournament: bool = False):
        all_tuples = list(combinations(self.players, 2))
        for player_1, player_2 in all_tuples:
            game = Game(player_1=player_1,
                        player_2=player_2,
                        rounds_per_game=self.rounds_per_game,
                        error_rate=self.error_rate,
                        debug=self.debug)
            game.go(show_game_title=game_printouts_instructions.get('show_game_title', None),
                    show_round_outcome=game_printouts_instructions.get('show_round_outcome', None),
                    summarize_game=game_printouts_instructions.get('summarize_game', None),
                    visualize_scores=game_printouts_instructions.get('visualize_scores', None))
        if summarize_tournament and self.debug:
            self.summarize(all_tuples)

    def summarize(self, all_tuples):
        self.print(F'{"*" * 18}\nTOURNAMENT SUMMARY\n{"." * 18}')

        total_games = len(all_tuples)
        sorted_list = sorted(self.players, key=lambda x: -x.score)

        self.print(f'{total_games} games played.')
        separator = '\n\t'
        printable = '\t' + separator.join([str(player) for player in sorted_list])
        self.print(f'Top scores:\n{printable}')
