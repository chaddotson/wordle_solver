import re


def generate_regex_for_eliminations(bad_words, letter_tracker):
    """
    Generate the regex for attempting to eliminate as many letters as possible.
    :param bad_words: Words that have been tried.
    :param letter_tracker: Object tracking attempts and results.
    :returns: regex string
    """
    used_letters = set(letter for word in bad_words for letter in word)
    used_letters.update(letter for letter in letter_tracker.at if letter is not None)
    used_letters.update(letter_tracker.invalids)
    used_letters.update(letter for not_at_list in letter_tracker.not_at.values() for letter in not_at_list)

    letters_regex = ''.join('[a-z]' for _ in range(len(letter_tracker.at)))
    contains_regex = ''
    invalids_regex = ''.join(f'(?!.*{invalid})' for invalid in used_letters)
    invalid_words_regex = ''.join(f'(?!{word})' for word in bad_words)
    total_regex = f'^{invalid_words_regex}{invalids_regex}{contains_regex}(?:{letters_regex})$'
    return total_regex


def generate_regex(bad_words, letter_tracker):
    """
    Generate the regex for identifying possible solutions.
    :param bad_words: Words that have been tried.
    :param letter_tracker: Object tracking attempts and results.
    :returns: regex string
    """
    letters_regex = ''.join([f'{"".join(f"(?!{nat})" for nat in letter_tracker.not_at.get(index, []))}[a-z]' if letter_tracker.at[index] is None else letter_tracker.at[index] for index in range(len(letter_tracker.at))])     # noqa: E501
    contains_regex = ''.join(f'(?=.*{letter})' for position_not_ats in letter_tracker.not_at.values() for letter in position_not_ats)   # noqa: E501
    invalids_regex = ''.join(f'(?!.*{invalid})' for invalid in letter_tracker.invalids)
    invalid_words_regex = ''.join(f'(?!{word})' for word in bad_words)
    total_regex = f'^{invalid_words_regex}{invalids_regex}{contains_regex}(?:{letters_regex})$'
    return total_regex


def generate_suggestion_by_ranked(ranked, regex):
    """
    Find the best word given the ranked list that fits the regex.
    :param ranked: A list of ranked words
    :param regex: The regex responsible for finding a fitting suggestion.
    :return: The word to try
    :raises: StopIteration if no word found.
    """
    suggestion, _ = next(pair for pair in ranked if re.search(regex, pair[0]))
    return suggestion
