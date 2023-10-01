import random

import modules.strategies as strategies
from modules.player import Player as Player
from modules.tournament import Tournament

if __name__ == '__main__':
    debug = True

    all_strategies = [
        strategies.Strategy(),
        strategies.Cheater(),
        strategies.Goody(),
        strategies.Copycat(),
        strategies.Random(),
        strategies.MajorityRule()
    ] * 10

    players = [Player(f'p{i+1}', strategy=strategy, debug=debug) for i, strategy in enumerate(all_strategies)]

    tournament = Tournament(players=players,
                            games_between_each_two_players=3,
                            rounds_per_game=100,
                            error_rate=.0,
                            survival_rate=.3,
                            survival_bias=.1,
                            debug=debug)

    game_printouts_instructions = {
        # 'show_game_title': True,
        # 'show_round_outcome': True,
        # 'summarize_game': True,
        # 'visualize_scores': True
    }

    for _ in range(4):
        tournament.go(game_printouts_instructions=game_printouts_instructions,
                      summarize_tournament=False)

        tournament.add_new_generation()

    tournament.visualize_history()
