import modules.strategies as strategies
from modules.player import Player as Player
from modules.tournament import Tournament

if __name__ == '__main__':
    debug = True

    players = [
        Player(name='p1', debug=debug),
        Player(name='p2', debug=debug),
        Player(name='p3', debug=debug),
        Player(name='p4', debug=debug)
    ]

    tournament = Tournament(players=players,
                            games_between_each_two_players=1,
                            rounds_per_game=5,
                            error_rate=.0,
                            top_percentage=.1,
                            survival_bias=.0,
                            debug=debug)

    game_printouts_instructions = {
        # 'show_game_title': True,
        # 'show_round_outcome': True,
        'summarize_game': True,
        # 'visualize_scores': False
    }

    tournament.go(game_printouts_instructions=game_printouts_instructions,
                  summarize_tournament=True)
