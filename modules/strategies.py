import random

import _helper as helper

from _debuggable import Debuggable


class Strategy(Debuggable):
    def __init__(self, name: str = 'Nameless Strategy', first_move=1, debug: bool = False):
        super().__init__(debug=debug)
        self.name = name
        self.first_move = {1: 1, 0: 0, 'rand': 1 if random.random() > .5 else 0}[first_move]

    def first_move_thoughts(self):
        if self.first_move is None:
            raise AttributeError(f'first_move was not defined for {self}')
        if self.first_move == 0:
            return 'I start by cheating'
        elif self.first_move == 1:
            return 'I start by cooperating'

    def decide(self, my_moves, their_moves):
        move = 1 if random.random() > 0.75 else 0
        return "Default decision", move


class Cheater(Strategy):
    def __init__(self, debug: bool = False):
        super().__init__(name='Cheater', first_move=0, debug=debug)

    def decide(self, my_moves, their_moves):
        return "Always cheat", 0


class Goody(Strategy):
    def __init__(self, debug: bool = False):
        super().__init__(name='Goody', debug=debug)

    def decide(self, my_moves, their_moves):
        return "Always cooperate", 1


class Copycat(Strategy):
    def __init__(self, change_action_after: int = 1, first_move: int = 1, debug: bool = False):
        name = 'Copycat' if change_action_after == 1 else f'Copykitten {change_action_after} times'
        super().__init__(name=name, first_move=first_move, debug=debug)
        self.change_action_after = change_action_after

    def decide(self, my_moves, their_moves):
        if len(my_moves) == 0:
            return self.first_move_thoughts(), self.first_move

        if my_moves[-1] == their_moves[-1]:
            return 'My last action was same as theirs, let\'s continue', their_moves[-1]

        else:
            # I'm required to consider changing my action from last time
            consecutive_length = helper.consecutive_equal_length_from_the_end(their_moves)
            if consecutive_length >= self.change_action_after:
                their_action = 'cooperated' if their_moves[-1] == 1 else 'cheated'
                return f'I will change my way now, they {their_action} for {consecutive_length} consecutive times', \
                    their_moves[-1]
            else:
                return 'I\'m keeping my action for now', my_moves[-1]


class Random(Strategy):
    def __init__(self, ratio: float = .5, debug: bool = False):
        name = 'Random ' + str(int(ratio * 100)) + '% to cooperate'
        super().__init__(name=name, first_move='rand', debug=debug)
        self.ratio = ratio

    def decide(self, my_moves, their_moves):
        thoughts = 'I am random'
        action = 1 if random.random() < self.ratio else 0

        return thoughts, action


class MajorityRule(Strategy):
    """Majority rule - I do what my opponent did most of, in the last p% of their moves"""
    def __init__(self, first_move: int = 1, minimal_cooperation_ratio: float = 0.5,
                 p_of_their_last_moves: float = 1.0, attenuation_power: float = 0.0,
                 debug: bool = False):
        """
        Initialize Majority Rule class.

        :param first_move (int): The first move to be made.
        :param minimal_cooperation_ratio (float): Below this ratio, I will retaliate with a cheat. The higher the number, the more my opponent needs to cooperate to make me cooperate.
        :param p_of_their_last_moves (float): The portion of their last moves I will consider.
        :param attenuation_power (float): The higher the number, the more weight is given to recent moves.
        :return: None
        """
        super().__init__(name='Majority Rule', first_move=first_move, debug=debug)

        self.lower_limit_of_cooperation = minimal_cooperation_ratio
        self.p_of_their_last_moves = p_of_their_last_moves

        self.attenuation_power = attenuation_power

    def decide(self, my_moves, their_moves):
        if len(my_moves) == 0:
            return self.first_move_thoughts(), self.first_move

        length_of_moves_to_consider = int(len(their_moves) * self.p_of_their_last_moves)
        their_last_moves_to_consider = their_moves[-length_of_moves_to_consider:]
        cooperations_weighted_ratio = self.attenuate_and_sum(their_last_moves_to_consider)

        if cooperations_weighted_ratio > self.lower_limit_of_cooperation:
            return 'You cooperated enough times recently', 1
        else:
            return 'You didn\'t cooperate enough times recently', 0

    def attenuate_and_sum(self, moves):
        total_moves_to_consider = len(moves)

        coefficients = [(x + 1) ** self.attenuation_power for x in range(total_moves_to_consider)]

        weighted_cooperation = [coefficients[i] for i, action in enumerate(moves) if action == 1]

        weighted_cooperation = sum(weighted_cooperation)

        cooperation_ratio = weighted_cooperation / sum(coefficients)

        return cooperation_ratio



# TODO: Grudger- starts cooperative, but as soon as you betray, Grudger will cheat until the end (with a chance to then flip back and return to their natural tendencies)
# TODO: Inversed-Grudger- starts cheating, but as soon as you cooperate, Inversed-Grudger will cooperate until the end (with a chance to then flip back and return to their natural tendencies)
# TODO: Tester- tests the waters first, to see if you're a sucker. If you retaliated more than p% of their cheats, they'll cooperate forever. else, they'll cheat forever
# TODO - pavlov variations- encourage different outcomes (we both do the same; we both do opposite; we both cooperated; we both cheated) -> 16 pavlovian variations possible
# forgiver - like copycat, but can't hold grudge for long
# forgiver2 - like copycat, but forgives occasionally (randomly)
# Gradual - change the frequency ratio of cooperations/cheatings from low to high or from high to low over time
# repeating sequence (of which Alternator is a special case of 1)
# Add more malicious strategies, that tr to take advantage of cooperative strategies
