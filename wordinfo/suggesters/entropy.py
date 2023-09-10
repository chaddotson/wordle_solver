import heapq
import json
import re
from hashlib import sha1
from math import log2
from pathlib import Path

from wordinfo.solver import Wordle
from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.utils import generate_regex, generate_regex_for_eliminations


class EntropySuggester(Suggester):
    """
    Use entropy to suggest words that give us the most information for future guesses.
    """
    __pretty_name__ = 'Entropy'

    def __init__(self, wordlist, cache_path: Path, *args, **kwargs):
        self._words = wordlist
        self._cache_path = cache_path
        cache_path.mkdir(exist_ok=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        words = self._get_viable_words(attempt_words, letter_tracker)

        if len(words) == 1:
            return words[0]

        entropy_by_word = self._get_entropy_by_word(words)
        suggestion = max(entropy_by_word, key=entropy_by_word.get)
        return suggestion

    def _get_viable_words(self, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        words = tuple(word for word in self._words if re.search(regex, word))
        return words

    def _get_entropy_by_word(self, words):
        json_words = json.dumps(words)
        sha1sum = sha1(json_words.encode()).hexdigest()
        cache_file = self._cache_path / f'{sha1sum}_entropy.json'
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                entropy_by_word = json.load(f)
        else:
            entropy_by_word = calculate_entroy_by_word(words)
            with open(cache_file, 'w') as f:
                json.dump(entropy_by_word, f)
        return entropy_by_word


class PopularEntropySuggester(EntropySuggester):
    """
    Use entropy weighted to popularity to suggest words that give us the most information
    for future guesses.
    """

    __pretty_name__ = 'Popular Entropy {cull}'

    def __init__(self, wordlist, cache_path, word_frequency_map, cull=40, *args, **kwargs):
        super().__init__(wordlist, cache_path)
        self._word_frequency_map = word_frequency_map
        self.cull = cull

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        words = self._get_viable_words(attempt_words, letter_tracker)

        if len(words) == 1:
            return words[0]

        entropy_by_word = self._get_entropy_by_word(words)
        top_suggestions = heapq.nlargest(self.cull, entropy_by_word, key=entropy_by_word.get)
        # print(top_suggestions)
        suggestion = sorted(top_suggestions, key=lambda w: self._word_frequency_map.get(w, 0), reverse=True)[0]
        return suggestion


class PopularEntropyEliminationSuggester(PopularEntropySuggester):
    __pretty_name__ = 'Popular Entropy Elimination {elimination_attempts}'

    def __init__(self, wordlist, cache_path, word_frequency_map, elimination_attempts=3, *args, **kwargs):
        super().__init__(wordlist, cache_path, word_frequency_map)
        self.elimination_attempts = elimination_attempts

    def _get_viable_words(self, attempt_words, letter_tracker):
        use_elimination = len(attempt_words) < self.elimination_attempts
        if use_elimination:
            regex = generate_regex_for_eliminations(attempt_words, letter_tracker)
        else:
            regex = generate_regex(attempt_words, letter_tracker)

        words = tuple(word for word in self._words if re.search(regex, word))

        if len(words) == 0 and use_elimination:
            regex = generate_regex(attempt_words, letter_tracker)
            words = tuple(word for word in self._words if re.search(regex, word))

        return words


def calc_part(count, word_count):
    probability = count / word_count
    return probability * log2(1 / probability)


def calculate_entropy(word_count, outcomes):
    return sum(calc_part(count, word_count) for count in outcomes.values())


def calculate_entroy_by_word(words):
    entropy_by_word = {}
    for word in words:
        wordle = Wordle(word)
        possible_outcomes = {}
        for w in words:
            found, guess_result = wordle.guess(w)
            if found:
                continue
            if guess_result not in possible_outcomes:
                possible_outcomes[guess_result] = 0
            possible_outcomes[guess_result] += 1

        word_count = len(words)
        entropy = calculate_entropy(word_count, possible_outcomes)
        entropy_by_word[word] = entropy
    return entropy_by_word