from dataclasses import dataclass
from json import load
from pathlib import Path
from random import choice
from statistics import mean
from time import time


from wordinfo.solver import (
    Solver, Wordle
)
from wordinfo.suggesters.entropy import EntropySuggester, PopularEntropySuggester
from wordinfo.suggesters.dominance import DominanceSuggester, DominanceEliminationSuggester, \
    DominanceHardmodeSuggester, DominanceModifiedSuggester, DominanceModifiedAltSuggester
from wordinfo.suggesters.rank import RankSuggester, RankModifiedSuggester
from wordinfo.old_solver import NewOne
from wordinfo.utils import load_word_list, WordSource


@dataclass
class BenchmarkResult:
    total_time: float
    average_time: float
    max_attempts: int
    average_attempts: int
    success_percent: float
    failed_words: list


def test_method(words, solver, suggester, fixed_suggestions=[]):
    t1 = time()
    results = []
    failed_words = []
    print(suggester.__class__.__name__)

    for i, target_word in enumerate(words):
        # suggester.reset()
        solved, tried_words, results_array = solver.solve(
            suggester=suggester,
            fixed_suggestions=fixed_suggestions,
            wordle=Wordle(target_word)
        )
        # print(len(tried_words))
        if len(tried_words) > 6:
            failed_words.append(target_word)

        results.append(len(tried_words))
        # if len(tried_words) > 6:
        #     print(target_word, tried_words)
        if i % 200 == 0:
            print(i)
        # suggester.reset()

    total_time = time() - t1
    average_time = total_time / len(results)
    average_attempts = mean(results)
    max_attempts = max(results)
    success_percent = len([r for r in results if r <=6])/len(results)*100

    return BenchmarkResult(
        total_time=total_time,
        average_time=average_time,
        max_attempts=max_attempts,
        average_attempts=average_attempts,
        success_percent=success_percent,
        failed_words=failed_words
    )


def run_benchmarks():
    words = load_word_list(WordSource.SOLUTIONS)
    full_word_list = load_word_list(WordSource.FULL)

    solver = Solver()

    # import pickle
    # with open('wordinfo/full_wordle.pickle', 'rb') as f:
    #     entropy_by_word = pickle.load(f)


    with open('wordinfo/data/word_frequency_map.json', 'r') as f:
        word_frequency_map = load(f)

    # failed_words = [
    #     'paper', 'booby', 'crass', 'start', 'weary', 'foyer', 'trite', 'class', 'dandy', 'catch', 'daddy',
    #     'aging', 'eater', 'tatty', 'bluer', 'joker', 'brass', 'hitch', 'boxer', 'ember', 'grass', 'bound',
    #     'sheer', 'wafer', 'scout', 'merry', 'state', 'batch', 'golly', 'brown', 'staid', 'vaunt', 'willy',
    #     'mercy'
    # ]
    #
    # for word in failed_words:
    #     word_frequency_map[word] += word_frequency_map[word] * 0.05

    results = [
        # ('Rank', test_method(words=words, solver=solver, suggester=RankSuggester(full_word_list))),
        # ('Dominance', test_method(words=words, solver=solver, suggester=DominanceSuggester(full_word_list))),
        # ('Dominance Elimination', test_method(words=words, solver=solver, suggester=DominanceEliminationSuggester(full_word_list))),
        # ('Dominance (hard mode)', test_method(words=words, solver=solver, suggester=DominanceHardmodeSuggester(full_word_list))),
        # ('Entropy', test_method(words=words, solver=solver, suggester=EntropySuggester(full_word_list, Path('./cache')))),
        ('Popular Word Entropy', test_method(words=words, solver=solver, suggester=PopularEntropySuggester(full_word_list, Path('./cache'), word_frequency_map))),



        # ('Rank', test_method(words=words, solver=solver, suggester=NewOne(words))),
        # ('Rank Modified (Stock)' , test_method(words=words, solver=solver, suggester=RankModifiedSuggester(words))),
        # ('Rank Modified (4)', test_method(words=words, solver=solver, suggester=RankModifiedSuggester(words, expand_selection_index=4))),
        # ('Rank Modified (5)', test_method(words=words, solver=solver, suggester=RankModifiedSuggester(words, expand_selection_index=5))),
        #('Dominance', test_method(words=words, solver=solver, suggester=DominanceSuggester(words), fixed_suggestions=['roate', 'linds'])),
        #('Dominance (hard mode)', test_method(words=words, solver=solver, suggester=DominanceHardmodeSuggester(words))),
        #('Entropy', test_method(words=words, solver=solver, suggester=EntropySuggester(full_word_list, entropy_by_word, word_frequency_map))),
        # ('Dominance Modified (Stock)', test_method(words=words, solver=solver, suggester=DominanceModifiedSuggester(words))),
        # ('Dominance Modified (4)', test_method(words=words, solver=solver, suggester=DominanceModifiedSuggester(words, expand_selection_index=4))),
        # ('Dominance Modified (5)', test_method(words=words, solver=solver, suggester=DominanceModifiedSuggester(words, expand_selection_index=5))),
        # ('Dominance Modified Alt (Stock)', test_method(words=words, solver=solver, suggester=DominanceModifiedAltSuggester(words))),
        # ('Dominance Random Start 1-word', test_method(words=words, solver=solver, suggester=DominanceSuggester(words), fixed_suggestions=[choice(words)])),
        # ('Dominance Fixed Start 1-word', test_method(words=words, solver=solver, suggester=DominanceSuggester(words), fixed_suggestions=['arise'])),
        # ('Dominance Fixed Start 1-word inv', test_method(words=words, solver=solver, suggester=DominanceSuggester(words), fixed_suggestions=['doubt'])),
        # ('Dominance Fixed Start 2-word', test_method(words=words, solver=solver, suggester=DominanceSuggester(words), fixed_suggestions=['arise', 'doubt'])),
    ]

    for result in results:
        print(result[0])
        print(f'Success: {result[1].success_percent:.3f}%')
        print(f'Total Time: {result[1].total_time:.3f}s / {result[1].average_time:.6f}s ea')
        print(f'Avg Tries: {result[1].average_attempts:.3f}')
        print(f'Max Tries: {result[1].max_attempts}')
        print(f'Failed Words: {len(result[1].failed_words)} - {result[1].failed_words}')

        print()


if __name__ == '__main__':
    run_benchmarks()