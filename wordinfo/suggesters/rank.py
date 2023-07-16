from collections import Counter
from functools import cached_property

from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.utils import generate_regex, generate_regex_for_eliminations, generate_suggestion_by_ranked


class RankSuggester(Suggester):
    __pretty_name__ = 'Rank'

    def __init__(self, wordlist, *args, **kwargs):
        self._score_by_letter = get_score_by_letter(wordlist)
        self._word_score = {word: score_word(self._score_by_letter, set(word)) for word in wordlist}
        self._ranked = sorted([(word, score) for word, score in self._word_score.items()], key=lambda x: x[1], reverse=True)  # noqa: E501

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        return generate_suggestion_by_ranked(self._ranked, regex)


class RankEliminationSuggester(RankSuggester):
    """
    Generates wordle guesses based on letter positional dominance but do it attempting to fully eliminate
    characters for the first few attempts.
    """
    __pretty_name__ = 'Rank Elimination {elimination_attempts}'

    def __init__(self, wordlist, elimination_attempts=3, *args, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        self.elimination_attempts = elimination_attempts

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        elimination_regex = generate_regex_for_eliminations(attempt_words, letter_tracker)
        regex = generate_regex(attempt_words, letter_tracker)

        try:
            if len(attempt_words) < self.elimination_attempts:
                return generate_suggestion_by_ranked(self._ranked, elimination_regex)
            # return generate_suggestion_by_ranked(self._dominance_ranked, elimination_regex)
            # if len(attempt_words) < 4:
            else:
                return generate_suggestion_by_ranked(self._ranked, regex)
            # else:
            #     return generate_suggestion_by_ranked(self._dominance_ranked, regex)
        except StopIteration:
            return generate_suggestion_by_ranked(self._ranked, regex)


class RankDedupSuggester(RankSuggester):
    __pretty_name__ = 'Rank (dedup)'

    def __init__(self, wordlist, *args, expand_selection_index=3, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        self._expand_selection_index = expand_selection_index
        self._dedup_words = [word for word in wordlist if not any(c > 1 for c in Counter(word).values())]
        self._dedup_word_score = {word: score_word(self._score_by_letter, word) for word in self._dedup_words}
        self._dedup_ranked = sorted([(word, score) for word, score in self._dedup_word_score.items()], key=lambda x: x[1], reverse=True)  # noqa: E501

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        try:
            if attempt < self._expand_selection_index:
                suggestion = generate_suggestion_by_ranked(self._dedup_ranked, regex)
            else:
                suggestion = generate_suggestion_by_ranked(self._ranked, regex)
        except StopIteration:
            suggestion = generate_suggestion_by_ranked(self._ranked, regex)
        return suggestion


def get_score_by_letter(words):
    counter = Counter()

    for word in words:
        counter.update(word)

    min_count = min(counter.values())

    score_by_letter = {}
    for letter, count in counter.items():
        score_by_letter[letter] = count/min_count

    return score_by_letter


def score_word(score_by_letter, word):
    value = 0
    for letter in word:
        value += score_by_letter[letter]
    return value
