from helpers import helper as helper
import strategies

from _debuggable import Debuggable
from player import Player

import random


def flip(action):
    return 0 if action == 1 else 1


class Game(Debuggable):
    def __init__(self,
                 name: str = 'Nameless Game',
                 player_1: Player = Player(),
                 player_2: Player = Player(),
                 rounds_per_game: int = 0,
                 error_rate: float = .0,
                 debug: bool = False):

        super().__init__(name=name, debug=debug)

        self.player_1 = player_1
        self.player_2 = player_2

        self.scores_1 = []
        self.scores_2 = []

        self.rounds_per_game = rounds_per_game
        self.error_rate = error_rate

    def should_flip(self):
        return random.random() < self.error_rate

    def go(self,
           show_game_title: bool = False,
           show_round_outcome: bool = False,
           summarize_game: bool = False,
           visualize_scores: bool = False):

        # Initialize conditions and variables
        player_1 = self.player_1
        player_2 = self.player_2
        initial_score_1 = player_1.score
        initial_score_2 = player_2.score
        intended_moves_1 = []
        intended_moves_2 = []
        moves_1 = []
        moves_2 = []
        scores_in_game_1 = []
        scores_in_game_2 = []

        if show_game_title and self.debug:
            helper.print_game_title(self)

        for round_number in range(1, self.rounds_per_game + 1):
            thoughts_1, decided_action_1 = player_1.decide(moves_1, moves_2, intended_moves_1)
            thoughts_2, decided_action_2 = player_2.decide(moves_2, moves_1, intended_moves_2)

            intended_moves_1.append(decided_action_1)
            intended_moves_2.append(decided_action_2)

            # The game may decide to flip a player's intended action, depending on the game's
            # error rate, or for other reasons.
            actual_action_1 = flip(decided_action_1) if self.should_flip() else decided_action_1
            actual_action_2 = flip(decided_action_2) if self.should_flip() else decided_action_2

            moves_1.append(actual_action_1)
            moves_2.append(actual_action_2)

            player_1.update_score(actual_action_1, actual_action_2)
            player_2.update_score(actual_action_2, actual_action_1)

            # The scores in the game should reflect only the points gained or lost in the current
            # game. Therefore, to calculate the score for a player in a given moment, we subtract
            # their score at the start of the game from the score they have at the moment.
            scores_in_game_1.append(self.player_1.score - initial_score_1)
            scores_in_game_2.append(self.player_2.score - initial_score_2)

            if show_round_outcome and self.debug:
                round_data = {k: str(v) for k, v in {
                    'round number': round_number,
                    'thoughts 1': thoughts_1,
                    'thoughts 2': thoughts_2,
                    'decided 1': decided_action_1,
                    'decided 2': decided_action_2,
                    'actual 1': actual_action_1,
                    'actual 2': actual_action_2,
                    'score 1': self.player_1.score,
                    'score 2': self.player_2.score,
                    'moves 1': moves_1,
                    'moves 2': moves_2
                }.items()}
                helper.print_round_outcome(self, round_data)

        if summarize_game and self.debug:
            helper.summarize_game(self, initial_score_1, moves_1, initial_score_2, moves_2)

        if visualize_scores and self.debug:
            game_info = {
                'error_rate': self.error_rate
            }
            helper.visualize_game_outcome(
                self.player_1.strategy, scores_in_game_1,
                self.player_2.strategy, scores_in_game_2,
                game_info
            )


if __name__ == '__main__':
    s1 = strategies.MajorityRule()
    s2 = strategies.Copycat()

    game = Game(player_1=Player(strategy=s1),
                player_2=Player(strategy=s2),
                rounds_per_game=5,
                error_rate=0.25,
                debug=True)

    game.go(show_game_title=True,
            show_round_outcome=True,
            summarize_game=True,
            visualize_scores=True)
