from dataclasses import dataclass
from logging import getLogger

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


class Solver(object):
    def __init__(self, *args, **kwargs):
        pass

    def solve(self, suggester, fixed_suggestions, wordle, *args, **kwargs):
        attempt_words = []
        attempt_results = []

        letter_tracker = LetterTracker(size=5)

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
                # print(index, code, letter)
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


