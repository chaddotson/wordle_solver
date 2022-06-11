from time import time
from logging import basicConfig, getLogger, INFO


from wordinfo.solver import Solver, Wordle
from wordinfo.suggesters.entropy import EntropySuggester, PopularEntropySuggester
from wordinfo.suggesters.dominance import DominanceSuggester, DominanceEliminationSuggester, \
    DominanceHardmodeSuggester
from wordinfo.suggesters.rank import RankModifiedSuggester
from wordinfo.utils import load_word_list, get_word_of_day, get_result_representation, WordSource


logging_config = dict(
    level=INFO,
    format='%(asctime)s %(message)s'
    # format='[%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s] %(message)s'
)

basicConfig(**logging_config)



def solve_todays_wordle():
    words = load_word_list()
    index, word_of_the_day = get_word_of_day(wordlist=words)
    # word_of_the_day = 'paper'
    words = load_word_list(WordSource.FULL)
    # word_of_the_day='shape'
    # word_of_the_day = 'shake'

    solver = Solver()

    suggester = DominanceHardmodeSuggester(words)
    start_time = time()
    solved, tried_words, results_array = solver.solve(
        suggester=suggester,
        fixed_suggestions=[],
        wordle=Wordle(word_of_the_day)
    )
    total_time = time() - start_time

    print(f"""
Wordle: {word_of_the_day}
Wordle#: {index}
Results:
{get_result_representation(results_array)}

Method: {suggester.__class__.__name__}
attempts: {tried_words}
time: {total_time:.6f}s
    """)

    # import pickle
    # with open('wordinfo/full_wordle.pickle', 'rb') as f:
    #     entropy_by_word = pickle.load(f)
    # from json import load
    # with open('wordinfo/data/word_frequency_map.json', 'r') as f:
    #     word_frequency_map = load(f)
    from pathlib import Path
    suggester = EntropySuggester(words, Path('./cache'))
    start_time = time()
    solved, tried_words, results_array = solver.solve(
        suggester=suggester,
        fixed_suggestions=[],
        wordle=Wordle(word_of_the_day)
    )
    total_time = time() - start_time

    print(f"""
Wordle: {word_of_the_day}
Wordle#: {index}
Results:
{get_result_representation(results_array)}

Method: {suggester.__class__.__name__}
attempts: {tried_words}
time: {total_time:.6f}s
    """)
    from json import load
    with open('wordinfo/data/word_frequency_map.json', 'r') as f:
        word_frequency_map = load(f)

    suggester = PopularEntropySuggester(words, Path('./cache'), word_frequency_map)
    start_time = time()
    solved, tried_words, results_array = solver.solve(
        suggester=suggester,
        fixed_suggestions=[],
        wordle=Wordle(word_of_the_day)
    )
    total_time = time() - start_time

    print(f"""
Wordle: {word_of_the_day}
Wordle#: {index}
Results:
{get_result_representation(results_array)}

Method: {suggester.__class__.__name__}
attempts: {tried_words}
time: {total_time:.6f}s
    """)



if __name__ == '__main__':
    solve_todays_wordle()