from collections import Counter

from wordinfo.suggesters.utils import generate_regex, generate_suggestion_by_ranked, generate_regex_for_eliminations
from wordinfo.suggesters.rank import RankSuggester, RankModifiedSuggester


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


def get_posititional_dominance(wordle_words):
    raw_dominance_count = {}
    for word in wordle_words:
        for index, letter in enumerate(word):
            if index not in raw_dominance_count:
                raw_dominance_count[index] = {}
            if letter not in raw_dominance_count[index]:
                raw_dominance_count[index][letter] = 0
            raw_dominance_count[index][letter] += 1

    # return raw_dominance_count
    dominance = {}
    for index, counted in raw_dominance_count.items():
        min_count = min(counted.values())

        if index not in dominance:
            dominance[index] = {}

        for letter, count in counted.items():
            # print(count)
            dominance[index][letter] = count / min_count

    return dominance


def dominance_score_word(dominance_by_index, word):
    value = 0
    # seen_letters = set()
    for index, letter in enumerate(word):
        # if letter in seen_letters:
        #     continue
        # value += dominance_by_index[index][letter]
        value += dominance_by_index[index].get(letter, 0)
        # seen_letters.add(letter)
    return value
