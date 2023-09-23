import random

import _helper as helper

from _debuggable import Debuggable


class Strategy(Debuggable):
    def __init__(self, name='Nameless Strategy', debug: bool = False):
        super().__init__(debug=debug)
        self.name = name

    def decide(self, my_moves, their_moves):
        return "Default decision", 1


class Cheater(Strategy):
    def __init__(self, debug: bool = False):
        super().__init__(name='Cheater', debug=debug)

    def decide(self, my_moves, their_moves):
        return "Always cheat", 0


class Goodie(Strategy):
    def __init__(self, debug: bool = False):
        super().__init__(name='Goodie', debug=debug)

    def decide(self, my_moves, their_moves):
        return "Always cooperate", 1


class Copycat(Strategy):
    def __init__(self, change_action_after: int = 1, first_move: int = 1, debug: bool = False):
        name = 'Copycat' if change_action_after == 1 else f'Copykitten {change_action_after} times'
        super().__init__(name=name, debug=debug)
        self.change_action_after = change_action_after
        self.first_move = first_move

    def decide(self, my_moves, their_moves):
        if len(my_moves) == 0:
            action = 'cooperating' if self.first_move == 1 else 'cheating'
            return f'I start by {action}', self.first_move

        if my_moves[-1] == their_moves[-1]:
            return 'My last action was same as theirs, let\'s continue', their_moves[-1]

        else:
            # I'm required to consider changing my action from last time
            consecutive_length = helper.consecutive_equal_length_from_the_end(their_moves)
            if consecutive_length >= self.change_action_after:
                their_action = 'cooperated' if their_moves[-1] == 1 else 'cheated'
                return f'I will change my way now, they {their_action} for {consecutive_length} consecutive times', their_moves[-1]
            else:
                return 'I\'m keeping my action for now', my_moves[-1]


class Random(Strategy):
    def __init__(self, name: str = None, ratio: float = .5, debug: bool = False):
        name = name if name else 'Random ' + str(int(ratio * 100)) + '% to cooperate'
        super().__init__(name=name, debug=debug)
        self.ratio = ratio

    def decide(self, my_moves, their_moves):
        thoughts = 'I am random'
        action = 1 if random.random() < self.ratio else 0

        return thoughts, action


# TODO: Grudger- starts cooperative, but as soon as you betray, Grudger will cheat until the end (with a chance to then flip back and return to their natural tendencies)
# TODO: Inversed-Grudger- starts cheating, but as soon as you cooperate, Inversed-Grudger will cooperate until the end (with a chance to then flip back and return to their natural tendencies)
# TODO: Tester- tests the waters first, to see if you're a sucker. If you retaliated more than p% of their cheats, they'll cooperate forever. else, they'll cheat forever
# TODO - pavlov variations- encourage different outcomes (we both do the same; we both do opposite; we both cooperated; we both cheated) -> 16 pavlovian variations possible
# forgiver - like copycat, but can't hold grudge for long
# forgiver2 - like copycat, but forgives occasionally (randomly)
# Gradual - change the frequency ratio of cooperations/cheatings from low to high or from high to low over time
# repeating sequence (of which Alternator is a special case of 1)
# majority rule - I do what my opponent did most of, in the last p% of their moves
# Add more malicious strategies, that tr to take advantage of cooperative strategies
