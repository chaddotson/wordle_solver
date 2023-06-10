from logging import INFO, basicConfig
from pathlib import Path
from time import time
from typing import List

from wordinfo.solver import Solver, Wordle
from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.dominance import DominanceDedupSuggester, DominanceEliminationSuggester, DominanceSuggester
from wordinfo.suggesters.entropy import EntropySuggester, PopularEntropySuggester
from wordinfo.utils import (
    WordSource, get_result_representation, get_word_of_day, load_word_frequency_list, load_word_list
)


def solve_with_method(suggester: Suggester, wordle: Wordle, fixed_suggestions: List[str] = None):
    """
    Solve the specified wordle using the specified suggester algorithm.
    :param suggester: A class instance that implements get_suggestion.
    :param wordle: The instance of the target word implements target_word and guess.
    :param fixed_suggestions: A list of fixed suggestions to select before using the specified suggester.
    :return: None
    """
    if fixed_suggestions is None:
        fixed_suggestions = []

    solver = Solver()

    start_time = time()
    solved, tried_words, results_array = solver.solve(
        suggester=suggester,
        fixed_suggestions=fixed_suggestions,
        wordle=wordle
    )
    total_time = time() - start_time

    print_results(results_array, suggester, total_time, tried_words, wordle)


def print_results(results_array: List[List[str]], suggester: Suggester, total_time: float, tried_words: List[str], wordle: Wordle):  # noqa: E501
    """
    Print the results of a solve attempt to the console.
    :param results_array:
    :param suggester: A class instance that implements get_suggestion.
    :param total_time: Total time in seconds to solve.
    :param tried_words: The list of words attempted.
    :param wordle: The instance of the target word implements target_word and guess.
    :return: None
    """
    print(f"""
Method: {suggester.__class__.__name__}
Wordle: {wordle.target_word}
attempts: {len(tried_words)} - {tried_words}
time: {total_time:.6f}s
Results:
{get_result_representation(results_array)}
   """)


def solve_todays_wordle():
    """
    Attempt to solve today's wordle with various methods.
    :return: None
    """
    index, word_of_the_day = get_word_of_day()
    words = load_word_list(WordSource.FULL)

    wordle = Wordle(word_of_the_day)
    word_frequency_map = load_word_frequency_list()

    solve_with_method(DominanceSuggester(words), wordle)
    solve_with_method(DominanceDedupSuggester(words), wordle)
    solve_with_method(DominanceEliminationSuggester(words), wordle)

    cache_path = Path('./cache')
    solve_with_method(EntropySuggester(words, cache_path), wordle)
    solve_with_method(PopularEntropySuggester(words, cache_path, word_frequency_map), wordle)


if __name__ == '__main__':
    logging_config = dict(
        level=INFO,
        format='%(asctime)s %(message)s'
        # format='[%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s] %(message)s'
    )

    basicConfig(**logging_config)

    solve_todays_wordle()
