import heapq
import json
import re
from hashlib import sha1
from math import log2
from pathlib import Path

from wordinfo.solver import Wordle
from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.utils import generate_regex


class EntropySuggester(Suggester):
    def __init__(self, wordlist, cache_path: Path, *args, **kwargs):
        self._words = wordlist
        self._cache_path = cache_path
        cache_path.mkdir(exist_ok=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)

        words = tuple(word for word in self._words if re.search(regex, word))

        if len(words) == 1:
            return words[0]

        # if len(attempt_words) == 0:
        json_words = json.dumps(words)
        sha1sum = sha1(json_words.encode()).hexdigest()
        cache_file = self._cache_path / f'{sha1sum}_entropy.json'
        #logger.info('Initial attempt, checking for cached entropy file: %s', cache_file)
        if cache_file.exists():
            #logger.info('Cached entropy exists.')
            with open(cache_file, 'r') as f:
                entropy_by_word = json.load(f)
            #logger.info('Cached entropy loaded.')
        else:
            #logger.info('No cached entropy exists. Recreating.')
            entropy_by_word = calculate_entroy_by_word(words)
            with open(cache_file, 'w') as f:
                json.dump(entropy_by_word, f)
            #logger.info('Entropy cache created.')
        # else:
        #     entropy_by_word = calculate_entroy_by_word(words)

        # print(len(attempt_words), len(self._words), max(self._entropy_by_word, key=self._entropy_by_word.get))
        suggestion = max(entropy_by_word, key=entropy_by_word.get)
        # top_suggestions = heapq.nlargest(5, self._entropy_by_word, key=self._entropy_by_word.get)
        #
        # suggestion = sorted(top_suggestions, key=lambda w: self._word_frequency_map[w], reverse=True)[0]

        return suggestion


class PopularEntropySuggester(Suggester):
    def __init__(self, wordlist, cache_path, word_frequency_map, *args, **kwargs):
        self._words = wordlist
        self._cache_path = cache_path
        self._word_frequency_map = word_frequency_map

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)

        words = tuple(word for word in self._words if re.search(regex, word))

        if len(words) == 1:
            return words[0]

        # if len(attempt_words) == 0:
        json_words = json.dumps(words)
        sha1sum = sha1(json_words.encode()).hexdigest()
        cache_file = self._cache_path / f'{sha1sum}_entropy.json'
        #logger.info('Initial attempt, checking for cached entropy file: %s', cache_file)
        if cache_file.exists():
            #logger.info('Cached entropy exists.')
            with open(cache_file, 'r') as f:
                entropy_by_word = json.load(f)
            #logger.info('Cached entropy loaded.')
        else:
            #logger.info('No cached entropy exists. Recreating.')
            entropy_by_word = calculate_entroy_by_word(words)
            with open(cache_file, 'w') as f:
                json.dump(entropy_by_word, f)
            #logger.info('Entropy cache created.')
        # else:
        #     entropy_by_word = calculate_entroy_by_word(words)

        # print(len(attempt_words), len(self._words), max(self._entropy_by_word, key=self._entropy_by_word.get))
        # suggestion = max(entropy_by_word, key=entropy_by_word.get)
        top_suggestions = heapq.nlargest(20, entropy_by_word, key=entropy_by_word.get)
        #
        suggestion = sorted(top_suggestions, key=lambda w: self._word_frequency_map[w], reverse=True)[0]

        return suggestion


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
            # guess_result = tuple(guess_result)
            if found:
                continue
            if guess_result not in possible_outcomes:
                possible_outcomes[guess_result] = 0
            possible_outcomes[guess_result] += 1

        word_count = len(words)
        entropy = calculate_entropy(word_count, possible_outcomes)
        entropy_by_word[word] = entropy
    return entropy_by_word

# class EntropySuggester(Suggester):
#     def __init__(self, wordlist, wordlist_entropy, word_frequency_map, *args, **kwargs):
#         self._original_words = self._words = wordlist
#         self._original_entropy_by_word = self._entropy_by_word = self._entropy_by_word = wordlist_entropy
#         self._word_frequency_map = word_frequency_map
#         self._initial = True
#
#     def reset(self):
#         self._words = self._original_entropy_by_word
#         self._entropy_by_word = self._original_entropy_by_word
#
#     def get_suggestion(self, attempt, attempt_words, letter_tracker):
#         if len(attempt_words) > 0:
#             regex = generate_regex(attempt_words, letter_tracker)
#             self._words = [word for word in self._words if re.search(regex, word)]
#             self._entropy_by_word = calculate_entroy_by_word(self._words)
#
#         # print(len(attempt_words), len(self._words), max(self._entropy_by_word, key=self._entropy_by_word.get))
#         suggestion = max(self._entropy_by_word, key=self._entropy_by_word.get)
#         # top_suggestions = heapq.nlargest(5, self._entropy_by_word, key=self._entropy_by_word.get)
#         #
#         # suggestion = sorted(top_suggestions, key=lambda w: self._word_frequency_map[w], reverse=True)[0]
#
#         return suggestion

# from json import dump, load

