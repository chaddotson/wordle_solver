from functools import cached_property
from pathlib import Path

from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.dominance import DominanceEliminationSuggester
from wordinfo.suggesters.entropy import PopularEntropySuggester
from wordinfo.suggesters.rank import RankEliminationSuggester


class DominananceEntropyEliminationSuggester(Suggester):
    __pretty_name__ = 'Dominance Entropy Elimination {elimination_attempts}'

    def __init__(self, wordlist, cache_path: Path, word_frequency_map,  elimination_attempts=3, *args, **kwargs):
        self.elimination_attempts = elimination_attempts
        self._domination_suggester = DominanceEliminationSuggester(wordlist, elimination_attempts)
        self._entropy_suggester = PopularEntropySuggester(wordlist, cache_path, word_frequency_map)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        if len(attempt_words) < self.elimination_attempts:
            return self._domination_suggester.get_suggestion(attempt, attempt_words, letter_tracker)
        return self._entropy_suggester.get_suggestion(attempt, attempt_words, letter_tracker)


class RankEntropyEliminationSuggester(Suggester):
    __pretty_name__ = 'Rank Entropy Elimination {elimination_attempts}'

    def __init__(self, wordlist, cache_path: Path, word_frequency_map,  elimination_attempts=3, *args, **kwargs):
        self.elimination_attempts = elimination_attempts
        self._rank_suggester = RankEliminationSuggester(wordlist, elimination_attempts)
        self._entropy_suggester = PopularEntropySuggester(wordlist, cache_path, word_frequency_map)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        if len(attempt_words) < self.elimination_attempts:
            return self._rank_suggester.get_suggestion(attempt, attempt_words, letter_tracker)
        return self._entropy_suggester.get_suggestion(attempt, attempt_words, letter_tracker)
