import matplotlib.pyplot as plt


NARROW_COLUMN = 10  # width in characters
WIDE_COLUMN = 30  # width in characters
SPACES = 10
SEPARATOR = ' ' * SPACES
OVERALL_WIDTH = NARROW_COLUMN + SPACES * 2 + WIDE_COLUMN * 2


def split_string_by_length(input_string, n):
    if n <= 0:
        raise ValueError('Width must be longer than 0.')

    return [input_string[j:j + n] for j in range(0, len(input_string), n)]


def split_long_string(long_string, width):
    """
    Split a long string into substrings of maximum length 'width' without breaking words.

    Args:
        long_string (str): The long string to be split.
        width (int): The maximum width for each substring.

    Returns:
        list of str: A list of substrings.
    """
    if width <= 0:
        raise ValueError("Width must be a positive integer.")

    # Initialize variables
    substrings = []
    current_width = 0
    current_substring = []

    # Split the long string into words
    words = long_string.split()

    for word in words:
        # If adding the current word to the current substring doesn't exceed the width
        if current_width + len(word) + len(current_substring) <= width:
            current_substring.append(word)
            current_width += len(word)
        else:
            # If adding the word exceeds the width, start a new substring
            substrings.append(" ".join(current_substring))
            current_substring = [word]
            current_width = len(word)

    # Add the last remaining substring, if any
    if current_substring:
        substrings.append(" ".join(current_substring))

    return substrings


def put_parts_together(instructions):
    strings_as_lists_of_lines = []
    max_lines = 0

    for string, width in instructions:
        list_of_lines = split_long_string(string, width)

        padded_list_of_lines = []

        for line in list_of_lines:
            padded_line = line.ljust(width)
            padded_list_of_lines.append(padded_line)

        strings_as_lists_of_lines.append(padded_list_of_lines)
        max_lines = max(max_lines, len(padded_list_of_lines))

    result = ''

    for line_number in range(max_lines):
        for i, lines in enumerate(strings_as_lists_of_lines):
            current_section_line = ''.ljust(len(lines[0]))
            if line_number < len(lines):
                current_section_line = lines[line_number]
            if i == 0:
                result += current_section_line
            else:
                result += SEPARATOR + current_section_line
        result += '\n' if line_number + 1 < max_lines else ''

    return result

def print_game_title(game):
    part_0 = 'Round #'
    part_1 = game.player_1.strategy.name
    part_2 = game.player_2.strategy.name

    instructions = [
        (part_0, NARROW_COLUMN),
        (part_1, WIDE_COLUMN),
        (part_2, WIDE_COLUMN)
    ]

    s = put_parts_together(instructions)
    s += '\n' + '_' * OVERALL_WIDTH

    game.print(s)


def print_round_outcome(game, data):
    part_0 = 'Round ' + data['round number']

    decided_1 = data['decided 1']
    decided_2 = data['decided 2']

    actual_1 = data['actual 1']
    actual_2 = data['actual 2']

    print_actual_1 = f'->{actual_1}' if actual_1 != decided_1 else ''
    print_actual_2 = f'->{actual_2}' if actual_2 != decided_2 else ''

    part_1 = data['thoughts 1'] + ': ' + data['decided 1'] + print_actual_1
    part_2 = data['thoughts 2'] + ': ' + data['decided 2'] + print_actual_2

    instructions = [
        (part_0, NARROW_COLUMN),
        (part_1, WIDE_COLUMN),
        (part_2, WIDE_COLUMN)
    ]

    thoughts_and_actions = put_parts_together(instructions)

    scores = put_parts_together([
        ('Score:', NARROW_COLUMN),
        (data['score 1'], WIDE_COLUMN),
        (data['score 2'], WIDE_COLUMN),
    ])

    game.print(thoughts_and_actions + '\n' + scores)

    game.print('_' * OVERALL_WIDTH)


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

def visualize_game_outcome(name_1, scores_1, name_2, scores_2):
    """
    Visualizes the game outcome over rounds for two players.

    Args:
        name_1 (str): The name of the first player.
        scores_1 (list): List of scores for the first player.
        name_2 (str): The name of the second player.
        scores_2 (list): List of scores for the second player.

    Returns:
        None

    This function takes the names and scores of two players and plots their scores
    over rounds using Matplotlib.

    """
    # Create a list of rounds (assuming equal number of rounds for both players)
    rounds = range(1, len(scores_1) + 1)

    # Plot the scores for each player
    plt.plot(rounds, scores_1, label=name_1, marker='o')  # Plot scores for player 1
    plt.plot(rounds, scores_2, label=name_2, marker='s')  # Plot scores for player 2

    # Add labels and title
    plt.xlabel('Round')  # Label for x-axis
    plt.ylabel('Score')  # Label for y-axis
    plt.title('Game Outcome Over Rounds')  # Title of the plot

    # Show integer values on the x-axis ticks
    plt.xticks(range(1, len(rounds) + 1))

    # Add a legend
    plt.legend()  # Display legend for player names

    # Show the chart
    plt.show()
