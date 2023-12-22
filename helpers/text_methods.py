def wrap(text, width, just='left'):
    """
    Wraps the given text to fit within the specified width.

    Args:
        text (str): The input text to be wrapped.
        width (int): The maximum width of each line.
        just (str): left, right, center, to width

    Returns:
        str: The wrapped text.

    Raises:
        RuntimeError: If a line longer than the specified width is encountered.

    """
    words = text.split(" ")

    lines = []
    line = ''

    while len(words) > 0:
        space_to_be_added = ''
        if len(line) > 0:
            space_to_be_added = ' '

        free_slots = width - len(line)

        word = words.pop(0)
        len(word)  # This line appears to be missing an assignment. Perhaps you meant len(word)?

        if len(word) > free_slots:  # +1 for space
            if free_slots == 2:
                lines.append(line)
                line = ''
                words.insert(0, word)
            else:
                subword_1 = word[:free_slots - 2]
                subword_2 = word[free_slots - 2:]
                line += space_to_be_added + subword_1 + '-'

                words.insert(0, subword_2)
        else:
            line += space_to_be_added + word

        if len(line) >= width - 1:
            lines.append(line)
            line = ''

        if len(line) > width:
            raise RuntimeError('New line longer than width. Cannot be')

    if line != '':
        lines.append(line)

    if just == 'to width':
        justified_lines = justify_lines(lines, width)  # It seems 'justify' is not defined in this code.
    else:
        justified_lines = []
        for line in lines:
            justification_method = {
                'left': lambda string: string.ljust(width),
                'right': lambda string: string.rjust(width),
                'center': lambda string: string.center(width),
            }[just]

            new_line = justification_method(line)

            justified_lines.append(new_line)

    return justified_lines


def justify_lines(lines, width):
    """
    Justify a list of lines to a given width by adding spaces between words.

    Args:
    lines (list of str): List of input lines to be justified.
    width (int): The desired width of each line after justification.

    Returns:
    list of str: List of justified lines with spaces added between words.
    """
    new_lines = []  # Initialize an empty list to store the justified lines

    for i, line in enumerate(lines):
        total_amount_of_spaces_to_add = width - len(line)
        words = line.split(' ')  # Split the line into words

        array_of_spaces = [' '] * (len(words) - 1)  # Create a list of spaces to interlace between words

        j = 0
        for _ in range(total_amount_of_spaces_to_add):
            array_of_spaces[j % (len(words) - 1)] += ' '  # Distribute spaces evenly between words
            j += 1

        new_list = interlace_lists(words, array_of_spaces)  # Interlace words and spaces
        new_line = ''.join(new_list)  # Join the list into a single string
        new_lines.append(new_line)  # Append the justified line to the result list

    return new_lines


def interlace_lists(list1, list2):
    """
    Interlace (interleave) two lists into a single list.

    Args:
        list1 (list): The first list.
        list2 (list): The second list.

    Returns:
        list: The interlaced list.
    """
    interlaced = []
    min_len = min(len(list1), len(list2))

    for i in range(min_len):
        interlaced.append(list1[i])
        interlaced.append(list2[i])

    # Add any remaining elements from the longer list, if any
    interlaced.extend(list1[min_len:])
    interlaced.extend(list2[min_len:])

    return interlaced