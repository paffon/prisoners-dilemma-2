import random
import re

from helpers import text_methods
import matplotlib.pyplot as plt
import numpy as np

NARROW_COLUMN = 15  # width in characters
WIDE_COLUMN = 50  # width in characters
SPACING = 1
SEPARATOR = ' ' * SPACING + '│ '
OVERALL_WIDTH = NARROW_COLUMN + SPACING * 2 + WIDE_COLUMN * 2


# def split_string_by_length(input_string, n):
#     if n <= 0:
#         raise ValueError('Width must be longer than 0.')
#
#     return [input_string[j:j + n] for j in range(0, len(input_string), n)]


# def split_long_string(long_string, width):
#     """
#     Split a long string into substrings of maximum length 'width' without breaking words.
#
#     Args:
#         long_string (str): The long string to be split.
#         width (int): The maximum width for each substring.
#
#     Returns:
#         list of str: A list of substrings.
#     """
#     if width <= 0:
#         raise ValueError("Width must be a positive integer.")
#
#     # Initialize variables
#     substrings = []
#     current_width = 0
#     current_substring = []
#
#     # Split the long string into words
#     words = long_string.split()
#
#     for word in words:
#         # If adding the current word to the current substring doesn't exceed the width
#         if current_width + len(word) + len(current_substring) <= width:
#             current_substring.append(word)
#             current_width += len(word)
#         else:
#             # If adding the word exceeds the width, start a new substring
#             substrings.append(" ".join(current_substring))
#             current_substring = [word]
#             current_width = len(word)
#
#     # Add the last remaining substring, if any
#     if current_substring:
#         substrings.append(" ".join(current_substring))
#
#     return substrings


def put_parts_together(instructions, separator: str = SEPARATOR):
    strings_as_lists_of_lines = []
    max_lines = 0

    for string, width, justify in instructions:
        list_of_lines = text_methods.wrap(string, width, justify)

        padded_list_of_lines = []

        for line in list_of_lines:
            padded_line = line.ljust(width)
            padded_list_of_lines.append(padded_line)

        strings_as_lists_of_lines.append(padded_list_of_lines)
        max_lines = max(max_lines, len(padded_list_of_lines))

    result = put_rows_side_by_side(max_lines, strings_as_lists_of_lines, separator)

    return result


def put_rows_side_by_side(max_lines, strings_as_lists_of_lines, separator):
    result = ''

    for line_number in range(max_lines):
        for i, lines in enumerate(strings_as_lists_of_lines):
            current_section_line = ''.ljust(len(lines[0]))
            if line_number < len(lines):
                current_section_line = lines[line_number]
            if i == 0:
                result += current_section_line
            else:
                result += separator + current_section_line
        result += '\n' if line_number + 1 < max_lines else ''

    return result


def print_game_title(game):

    line_title = [
        ('Players:', NARROW_COLUMN, 'right'),
        (game.player_1.name, WIDE_COLUMN, 'center'),
        (game.player_2.name, WIDE_COLUMN, 'center'),
    ]
    line_strategies = [
        ('Strategies:', NARROW_COLUMN, 'right'),
        (game.player_1.strategy.name, WIDE_COLUMN, 'center'),
        (game.player_2.strategy.name, WIDE_COLUMN, 'center'),
    ]
    game.print(game.name)
    for line in [line_title, line_strategies]:
        game.print(put_parts_together(line))
    game.print('_' * OVERALL_WIDTH)


def print_round_outcome(game, data):
    decided_1 = data['decided 1']
    decided_2 = data['decided 2']

    actual_1 = data['actual 1']
    actual_2 = data['actual 2']

    print_actual_1 = f'->{actual_1}' if actual_1 != decided_1 else ''
    print_actual_2 = f'->{actual_2}' if actual_2 != decided_2 else ''

    line_thoughts = [
        ('Thoughts:', NARROW_COLUMN, 'right'),
        (f"\'{data['thoughts 1']}\'", WIDE_COLUMN, 'left'),
        (f"\'{data['thoughts 2']}\'", WIDE_COLUMN, 'left')
    ]
    line_actions = [
        ('Actions:', NARROW_COLUMN, 'right'),
        (f"{data['decided 1']}{print_actual_1}", WIDE_COLUMN, 'left'),
        (f"{data['decided 2']}{print_actual_2}", WIDE_COLUMN, 'left')
    ]
    line_scores = [
        ('Scores:', NARROW_COLUMN, 'right'),
        (data['score 1'], WIDE_COLUMN, 'left'),
        (data['score 2'], WIDE_COLUMN, 'left')
    ]
    line_moves = [
        ('Moves:', NARROW_COLUMN, 'right'),
        (data['moves 1'], WIDE_COLUMN, 'left'),
        (data['moves 2'], WIDE_COLUMN, 'left'),
    ]

    game.print('\nRound ' + data['round number'])
    for line in [line_thoughts, line_actions, line_scores, line_moves]:
        game.print(put_parts_together(line))


def consecutive_equal_length_from_the_end(arr):
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        return 1

    count = 1
    i = len(arr) - 2  # Start from the element before last
    while i >= 0:
        if arr[i] == arr[-1]:
            # Current element equals last element
            count += 1
        else:
            break
        i -= 1
    return count


def visualize_game_outcome(strategy_1,
                           scores_1: list,
                           strategy_2,
                           scores_2: list,
                           game_info: dict):
    """
    Visualizes the game outcome over rounds for two players with move labels as score deltas.

    Args:
        strategy_1 (str): The first strategy object itself.
        scores_1 (list): List of scores for the first player.
        strategy_2 (str): The seconds strategy object itself.
        scores_2 (list): List of scores for the second player.
        game_info (dict): a dictionary of the game's parameters for display.

    Returns:
        None

    This function takes the names and scores of two players and plots their scores
    over rounds using Matplotlib as line plots with move labels as score deltas.

    """
    # Create a list of rounds (assuming equal number of rounds for both players)
    rounds = range(1, len(scores_1) + 1)

    # Calculate score deltas for each player
    score_deltas_1 = [scores_1[i] - (0 if i == 0 else scores_1[i - 1]) for i in range(len(scores_1))]
    score_deltas_2 = [scores_2[i] - (0 if i == 0 else scores_2[i - 1]) for i in range(len(scores_2))]

    # Create line plots for each player with scores as data points and default colors
    # Line plot for player 1
    plt.plot(rounds, scores_1, label=strategy_1, marker='h', linestyle='-', markersize=5)
    # Line plot for player 2
    plt.plot(rounds, scores_2, label=strategy_2, marker='H', linestyle='-', markersize=5)

    # Add labels for score deltas as annotations with matching colors
    zipped = zip(rounds, score_deltas_1, score_deltas_2, scores_1, scores_2)
    for round_num, delta_1, delta_2, score_1, score_2 in zipped:

        if round_num != 1:  # Skip the first round as there is no previous round to compare

            plt.annotate(f'+{delta_1}', (round_num + .1, score_1),
                         textcoords="offset points", xytext=(0, 10),
                         ha='center', color='tab:blue')

            plt.annotate(f'+{delta_2}', (round_num - .1, score_2),
                         textcoords="offset points", xytext=(0, 10),
                         ha='center', color='tab:orange')

    # Add labels and title
    plt.xlabel('Round')  # Label for x-axis
    plt.ylabel('Score')  # Label for y-axis

    printable_game_info = '\n'.join([f'{k}: {v}' for k, v in game_info.items()])
    plt.title(f'Game Outcome Over Rounds\n{printable_game_info}')  # Title of the plot

    # Set the x-axis limits to start from 0 and end a bit over the maximum round number
    plt.xlim(0, max(rounds) + 1)

    # Show integer values on the x-axis ticks
    plt.xticks(rounds)

    # Add a legend
    plt.legend()  # Display legend for player names

    # Show the chart
    plt.show()


def add_sign(number):
    """
    Add a sign to a number.

    Parameters:
    number (int): The input number.

    Returns:
    str: The number with a '+' if positive, '-' if negative, or unchanged if 0.
    """
    # Check if the number is positive
    if number > 0:
        return '+' + str(number)
    # Check if the number is negative
    elif number < 0:
        return str(number)
    # If the number is zero, return it as a string
    return str(number)


def summarize_game(game, initial_score_1, moves_1, initial_score_2, moves_2):
    line_sep = '_' * OVERALL_WIDTH
    game.print(f'\n{line_sep}\n{game.name} summary:\n')
    score_delta_1 = game.player_1.score - initial_score_1
    score_delta_2 = game.player_2.score - initial_score_2

    signed_delta_1 = add_sign(score_delta_1)
    signed_delta_2 = add_sign(score_delta_2)

    # Display players' properties and score gain/loss in this game
    line_names_and_scores = [
        ('Names & scores', NARROW_COLUMN, 'left'),
        (f'{game.player_1.name}, score: {game.player_1.score} ({signed_delta_1})', WIDE_COLUMN, 'left'),
        (f'{game.player_2.name}, score: {game.player_2.score} ({signed_delta_2})', WIDE_COLUMN, 'left')]
    line_strategies = [
        ('Strategies', NARROW_COLUMN, 'left'),
        (str(game.player_1.strategy), WIDE_COLUMN, 'left'),
        (str(game.player_2.strategy), WIDE_COLUMN, 'left')]
    line_moves = [
        ('Moves', NARROW_COLUMN, 'left'),
        ('[' + ', '.join([str(action) for action in moves_1]) + ']', WIDE_COLUMN, 'left'),
        ('[' + ', '.join([str(action) for action in moves_2]) + ']', WIDE_COLUMN, 'left'),
    ]

    for line in [line_names_and_scores, line_strategies, line_moves]:
        game.print(put_parts_together(line))


def scramble_list(array: list, chaos_factor: float):
    """
    Scramble the elements in a list based on a chaos factor.

    Args:
        array (list): The input list to be scrambled.
        chaos_factor (float): A value between 0 and 1 indicating the degree of scrambling.

    Returns:
        list: The scrambled list.

    """
    # Calculate the number of elements to move based on the chaos_factor.
    num_elements_to_move = int(len(array) * chaos_factor)

    for _ in range(num_elements_to_move):
        # Remove an element from the list
        element_to_move = array.pop(random.randint(0, len(array) - 1))

        # Generate a random index and reinsert the element at that index
        random_index = random.randint(0, len(array))
        array.insert(random_index, element_to_move)

    return array


def visualize_tournament_history(df):
    """
    Visualizes tournament history using a 100% stacked bar chart.

    Args:
        df (pd.DataFrame): A DataFrame with name counts for each generation.

    Returns:
        None
    """
    # Calculate the total count for each generation
    generation_totals = df.sum(axis=1)

    # Calculate the percentage of each name in each generation
    df_percentage = df.div(generation_totals, axis=0) * 100

    # Create a 100% stacked bar chart
    ax = df_percentage.plot(kind='bar', stacked=True, figsize=(10, 6))

    # Set labels and title
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Generation')
    ax.set_title('Percentage of Names in Each Generation')

    # Make x-ticks horizontal
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    # Display the chart
    plt.legend(title='Name')
    plt.show()
