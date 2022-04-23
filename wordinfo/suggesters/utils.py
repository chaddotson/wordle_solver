import re


def generate_regex_for_eliminations(bad_words, letter_tracker):
    used_letters = [letter for word in bad_words for letter in word]
    used_letters.extend(letter_tracker.invalids)
    used_letters.extend(set(letter for not_at_list in letter_tracker.not_at.values() for letter in not_at_list))

    letters_regex = ''.join('[a-z]' for _ in range(len(letter_tracker.at)))
    contains_regex = ''
    invalids_regex = ''.join(f'(?!.*{invalid})' for invalid in used_letters)
    invalid_words_regex = ''.join(f'(?!{word})' for word in bad_words)
    total_regex = f'^{invalid_words_regex}{invalids_regex}{contains_regex}(?:{letters_regex})$'

    return total_regex


def generate_regex(bad_words, letter_tracker):
    letters_regex = ''.join([f'{"".join(f"(?!{nat})" for nat in letter_tracker.not_at.get(index, []))}[a-z]' if letter_tracker.at[index] is None else letter_tracker.at[index] for index in range(len(letter_tracker.at))])
    contains_regex = ''.join(f'(?=.*{letter})' for position_not_ats in letter_tracker.not_at.values() for letter in position_not_ats)
    invalids_regex = ''.join(f'(?!.*{invalid})' for invalid in letter_tracker.invalids)
    invalid_words_regex = ''.join(f'(?!{word})' for word in bad_words)
    total_regex = f'^{invalid_words_regex}{invalids_regex}{contains_regex}(?:{letters_regex})$'
    return total_regex


def generate_suggestion_by_ranked(ranked, regex):
    # print(regex)
    # try:
    suggestion, _ = next(pair for pair in ranked if re.search(regex, pair[0]))
    # except StopIteration:
    #     suggestion, _ = next(pair for pair in ranked if re.search(regex[1], pair[0]))
    return suggestion
