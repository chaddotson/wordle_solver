from collections import Counter
from dataclasses import dataclass
from logging import getLogger
import re

from wordinfo.scoring import get_score_by_letter, score_word, get_posititional_dominance, dominance_score_word


logger = getLogger(__name__)

@dataclass(init=False)
class LetterTracker:
    at: list
    not_at: dict
    invalids: set

    def __init__(self, size):
        self._size = size
        self.reset()

    def reset(self):
        self.at = [None] * self._size
        self.not_at = {}
        self.invalids = set()


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


class SuggestionChooser(object):
    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        pass


class Suggester(object):
    def reset(self):
        pass


class RankSuggester(Suggester):
    def __init__(self, wordlist, *args, **kwargs):
        self._score_by_letter = get_score_by_letter(wordlist)
        self._word_score = {word: score_word(self._score_by_letter, set(word)) for word in wordlist}
        self._ranked = sorted([(word, score) for word, score in self._word_score.items()], key=lambda x: x[1], reverse=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        return generate_suggestion_by_ranked(self._ranked, regex)


from math import log2


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

from hashlib import sha1
# from json import dump, load
import json
class EntropySuggester(Suggester):
    def __init__(self, wordlist, cache_path, *args, **kwargs):
        self._words = wordlist
        self._cache_path = cache_path

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


import heapq

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


class DominanceSuggester(RankSuggester):
    def __init__(self, wordlist, *args, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        positional_dominance = get_posititional_dominance(wordlist)
        dominance_word_score = {word: dominance_score_word(positional_dominance, word) for word in wordlist}
        self._dominance_ranked = sorted([(word, score) for word, score in dominance_word_score.items()], key=lambda x: x[1], reverse=True)

        self._dedup_words = [word for word in wordlist if not any(c > 1 for c in Counter(word).values())]
        positional_dominance = get_posititional_dominance(self._dedup_words)
        dedup_dominance_word_score = {word: dominance_score_word(positional_dominance, word) for word in self._dedup_words}
        self._dedup_dominance_ranked = sorted([(word, score) for word, score in dedup_dominance_word_score.items()], key=lambda x: x[1], reverse=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        return generate_suggestion_by_ranked(self._dominance_ranked, regex)


class DominanceEliminationSuggester(DominanceSuggester):
    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        elimination_regex = generate_regex_for_eliminations(attempt_words, letter_tracker)
        regex = generate_regex(attempt_words, letter_tracker)

        try:
            if len(attempt_words) < 5:
                return generate_suggestion_by_ranked(self._dedup_dominance_ranked, elimination_regex)
            # return generate_suggestion_by_ranked(self._dominance_ranked, elimination_regex)
            # if len(attempt_words) < 4:
            else:
                return generate_suggestion_by_ranked(self._dominance_ranked, regex)
            # else:
            #     return generate_suggestion_by_ranked(self._dominance_ranked, regex)
        except StopIteration:
            return generate_suggestion_by_ranked(self._dominance_ranked, regex)


class DominanceHardmodeSuggester(DominanceSuggester):
    # def __init__(self, wordlist, *args, **kwargs):
    #     super().__init__(wordlist, *args, **kwargs)
    #     positional_dominance = get_posititional_dominance(wordlist)
    #     dominance_word_score = {word: dominance_score_word(positional_dominance, word) for word in wordlist}
    #     self._dominance_ranked = sorted([(word, score) for word, score in dominance_word_score.items()], key=lambda x: x[1], reverse=True)

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)

        # suggestion, _ = choice(re.(regex, self._dominance_ranked[0]))

        # suggestion, _ = [pair for pair in self._dominance_ranked if re.search(regex, pair[0])]

        # try:
        #     # if len(attempt_words) <= 2:
        #     #     return generate_suggestion_by_ranked(self._dedup_dominance_ranked[-1:0:-1], regex)
        #     # else:
        #         return generate_suggestion_by_ranked(self._dedup_dominance_ranked, regex)
        # except StopIteration:
        #     return generate_suggestion_by_ranked(self._dominance_ranked, regex)

        return generate_suggestion_by_ranked(self._dominance_ranked, regex)
        # return choice([pair[0] for pair in self._dominance_ranked if re.search(regex, pair[0])])
        #
        #
        # try:
        #     return generate_suggestion_by_ranked(self._dominance_ranked, regex)
        #
        # except StopIteration:
        #     return generate_suggestion_by_ranked(self._dominance_ranked, regex)



class DominanceModifiedSuggester(DominanceSuggester):
    def __init__(self, wordlist, *args, expand_selection_index=3, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        self._expand_selection_index = expand_selection_index

    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        try:
            if attempt < self._expand_selection_index:
                suggestion = generate_suggestion_by_ranked(self._dominance_ranked, regex)
            else:
                suggestion = generate_suggestion_by_ranked(self._ranked, regex)
        except StopIteration:
            suggestion = generate_suggestion_by_ranked(self._ranked, regex)
        return suggestion


class DominanceModifiedAltSuggester(DominanceSuggester, RankModifiedSuggester):
    def __init__(self, wordlist, *args, expand_selection_index=3, **kwargs):
        super().__init__(wordlist, *args, **kwargs)
        self._expand_selection_index = expand_selection_index


    def get_suggestion(self, attempt, attempt_words, letter_tracker):
        regex = generate_regex(attempt_words, letter_tracker)
        try:
            if attempt < self._expand_selection_index:
                suggestion = generate_suggestion_by_ranked(self._dominance_ranked, regex)
            else:
                suggestion = generate_suggestion_by_ranked(self._dedup_ranked, regex)
        except StopIteration:
            suggestion = generate_suggestion_by_ranked(self._ranked, regex)
        return suggestion


class Wordle(object):
    def __init__(self, target_word):
        self._target_word = target_word

    @property
    def target_word(self):
        return self._target_word

    def guess(self, word):
        results = []
        for index, (l, r) in enumerate(zip(word, self._target_word)):
            if l == r:
                results.append(2)
            elif l in self._target_word:
                results.append(1)
            else:
                results.append(0)
        return word == self._target_word, tuple(results)

    #
    # def test_word(self, word, letter_tracker):
    #     results = []
    #     for index, (l, r) in enumerate(zip(word, self._target_word)):
    #         if l == r:
    #             results.append(2)
    #             letter_tracker.at[index] = l
    #         elif l in self._target_word:
    #             results.append(1)
    #             if index not in letter_tracker.not_at:
    #                 letter_tracker.not_at[index] = set()
    #             letter_tracker.not_at[index].add(l)
    #         else:
    #             results.append(0)
    #             letter_tracker.invalids.add(l)
    #     return word == self._target_word, results


class Solver(object):
    def __init__(self, *args, **kwargs):
        pass

    def solve(self, suggester, fixed_suggestions, wordle, *args, **kwargs):
        attempt_words = []
        attempt_results = []

        letter_tracker = LetterTracker(size=5)
        #     at=[None] * 5,
        #     not_at={},
        #     invalids=set()
        # )

        # print('target:', wordle.target_word)

        attempt = 0
        solved = False
        while not solved:
            if attempt < len(fixed_suggestions):
                suggestion = fixed_suggestions[attempt]
            else:
                suggestion = suggester.get_suggestion(attempt, attempt_words, letter_tracker)

            # print('suggestion:', suggestion)

            attempt_words.append(suggestion)
            solved, result = wordle.guess(suggestion)
            attempt_results.append(result)

            for index, (code, letter) in enumerate(zip(result, suggestion)):
                if code == 2:
                    letter_tracker.at[index] = letter
                elif code == 1:
                    if index not in letter_tracker.not_at:
                        letter_tracker.not_at[index] = set()
                    letter_tracker.not_at[index].add(letter)
                else:
                    letter_tracker.invalids.add(letter)

            attempt += 1

        return solved, attempt_words, attempt_results


