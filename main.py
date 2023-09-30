import modules.strategies as strategies
from modules.player import Player as Player
from modules.tournament import Tournament

if __name__ == '__main__':
    debug = True

    players = [Player(f'p{i+1}', debug=debug) for i in range(20)]

    tournament = Tournament(players=players,
                            games_between_each_two_players=1,
                            rounds_per_game=5,
                            error_rate=.0,
                            survival_rate=.15,
                            survival_bias=.05,
                            debug=debug)

    game_printouts_instructions = {
        # 'show_game_title': True,
        # 'show_round_outcome': True,
        # 'summarize_game': True,
        # 'visualize_scores': False
    }

    for _ in range(2):
        tournament.go(game_printouts_instructions=game_printouts_instructions,
                      summarize_tournament=True)

        tournament.add_new_generation()