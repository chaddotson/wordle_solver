from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass(init=False)
class LetterTracker:
    """
    Stores the current status of a sequence of guesses.
    at: list of known positions
    not_at: dict of known bad placements
    invalids: set of known invalid letters
    """
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
    """Stores the current target word (wordle)"""
    def __init__(self, target_word):
        self._target_word = target_word

    @property
    def target_word(self):
        """Get the target word"""
        return self._target_word

    def guess(self, word):
        """Check a word to see how it compares to the target word."""
        results = []
        for index, (left_char, right_char) in enumerate(zip(word, self._target_word)):
            if left_char == right_char:
                results.append(2)
            elif left_char in self._target_word:
                results.append(1)
            else:
                results.append(0)
        return word == self._target_word, tuple(results)


class Solver(object):
    """Wordle puzzle solver"""
    def solve(self, suggester, fixed_suggestions, wordle, *args, **kwargs):
        """
        Solve the wordle with the specified suggester algorithm
        :param suggester: The object responsible for generating word guesses.
        :param fixed_suggestions: A fixed set of suggestions to start with.
        :param wordle: The object responsible for holding and testing guesses.
        :returns: a tuple containing if it was solved, the words attempted and the results.
        """
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
