import math
from collections import defaultdict
from itertools import combinations

import pandas as pd
from matplotlib import pyplot as plt

from _debuggable import Debuggable
import _helper as helper

from game import Game


class Tournament(Debuggable):
    def __init__(self,
                 players,
                 games_between_each_two_players: int = 0,
                 rounds_per_game: int = 0,
                 error_rate: float = .0,
                 survival_rate: float = .1,
                 survival_bias: float = .0,
                 debug: bool = False):

        super().__init__(debug=debug)

        self.games_between_each_two_players = games_between_each_two_players
        self.rounds_per_game = rounds_per_game
        self.error_rate = error_rate
        self.survival_rate = survival_rate
        self.survival_bias = survival_bias
        self.current_generation = players
        self.generations = [self.current_generation]

    def go(self, game_printouts_instructions: dict, summarize_tournament: bool = False):
        all_tuples = list(combinations(self.current_generation, 2))
        for i, players_tuple in enumerate(all_tuples):
            player_1, player_2 = players_tuple
            game = Game(name=f'Game {i}',
                        player_1=player_1,
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
        sorted_list = sorted(self.current_generation, key=lambda x: -x.score)

        self.print(f'{total_games} games played.')
        self.print('Ranking:')

        amount_of_surviving_players = round(self.survival_rate * len(self.current_generation))
        max_width = max([len(str(player)) for player in self.current_generation])
        for i, player in enumerate(sorted_list):
            if i == amount_of_surviving_players:
                self.print('\t' + 'Survival boundary'.center(max_width, '-'))
            self.print(f'\t{i + 1}. {player}')

    def get_the_surviving_players(self):
        """
        Get the surviving players based on a survival rate and bias.

        Returns:
            list: List of surviving players.
        """

        total_players = len(self.current_generation)

        # Get random indices for the surviving players
        amount_of_surviving_players = round(self.survival_rate * total_players)
        scrambled_indices = helper.scramble_list(list(range(total_players)),
                                                 self.survival_bias)
        indices_of_surviving_players = scrambled_indices[:amount_of_surviving_players]

        # Sort the players by score in descending order
        sorted_list = sorted(self.current_generation, key=lambda x: -x.score)

        # Get the surviving players based on their indices
        surviving_players = [sorted_list[i] for i in indices_of_surviving_players]

        return surviving_players

    def get_next_generation_of_players(self):
        amount_of_players_in_the_tournament_in_total = len(self.current_generation)
        survived_players = self.get_the_surviving_players()
        amount_of_survived_players = len(survived_players)
        multiplication_factors = self.get_multiplication_factors(
            amount_of_players_in_the_tournament_in_total,
            amount_of_survived_players
        )

        new_generation = self.multiply_players(survived_players, multiplication_factors)

        return new_generation

    @staticmethod
    def get_multiplication_factors(total_amount: int, survived_amount: int):
        """
        Spread the total amount over an array of survived_amount elements.

        Args:
            total_amount (int): The total amount to distribute.
            survived_amount (int): The number of elements to distribute the total amount among.

        Returns:
            List[int]: An array of multiplication factors representing the distribution.

        Example:
            If total_amount is 10 and survived_amount is 3, the result could be [4, 3, 3],
            meaning 4 units go to the first element, and 3 units each to the second and third elements.
        """
        multiplication_factors = [0] * survived_amount

        i = 0
        for _ in range(total_amount):
            multiplication_factors[i % survived_amount] += 1
            i += 1

        return multiplication_factors

    @staticmethod
    def multiply_players(survived_players, multiplication_factors):
        new_generation = list()
        for factor, player in zip(multiplication_factors, survived_players):
            for _ in range(factor):
                new_generation.append(player.give_birth())
        return new_generation

    def add_new_generation(self):
        new_generation = self.get_next_generation_of_players()
        self.generations.append(new_generation)
        self.current_generation = new_generation

    @staticmethod
    def value_counts(players):
        strategies = [player.strategy for player in players]
        string_list = [strategy.display_without_keys(['display_name', 'generation', 'score', 'debug']).lstrip('name=') for strategy in strategies]

        # Initialize a defaultdict with int as the default factory
        string_count_dict = defaultdict(int)

        # Count the strings and store the counts in the dictionary
        for string in string_list:
            string_count_dict[string] += 1

        # Convert the defaultdict to a regular dictionary if needed
        string_count_dict = dict(string_count_dict)

        return string_count_dict

    def visualize_history(self):
        df = self.history_as_df()
        helper.visualize_tournament_history(df)

    def history_as_df(self):
        diversity_history = [self.value_counts(generation) for generation in self.generations]
        all_names = diversity_history[0].keys()

        for diversity_dict in diversity_history:
            zero_amounts = {name: 0 for name in all_names if name not in diversity_dict}
            diversity_dict.update(zero_amounts)

        df = pd.DataFrame(diversity_history)

        df.index = [f'Gen. {i}' for i in range(0, len(diversity_history))]

        return df