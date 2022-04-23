from collections import Counter

from wordinfo.suggesters.utils import generate_regex, generate_suggestion_by_ranked
from wordinfo.suggesters.base import Suggester


class RankSuggester(Suggester):
    def __init__(self, wordlist, *args, **kwargs):
        self._score_by_letter = get_score_by_letter(wordlist)
        self._word_score = {word: score_word(self._score_by_letter, set(word)) for word in wordlist}
        self._ranked = sorted([(word, score) for word, score in self._word_score.items()], key=lambda x: x[1], reverse=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        return generate_suggestion_by_ranked(self._ranked, regex)


class RankModifiedSuggester(RankSuggester):
    def __init__(self, wordlist, *args, expand_selection_index=3, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        self._expand_selection_index = expand_selection_index
        self._dedup_words = [word for word in wordlist if not any(c > 1 for c in Counter(word).values())]
        self._dedup_word_score = {word: score_word(self._score_by_letter, word) for word in self._dedup_words}
        self._dedup_ranked = sorted([(word, score) for word, score in self._dedup_word_score.items()], key=lambda x: x[1], reverse=True)

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
