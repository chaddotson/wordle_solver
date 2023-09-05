from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from logging import INFO, basicConfig, getLogger
from pathlib import Path
from statistics import mean
from time import time

from wordinfo.solver import Solver, Wordle
from wordinfo.suggesters.base import Suggester
from wordinfo.suggesters.hybrid import DominananceEntropyEliminationSuggester, RankEntropyEliminationSuggester
from wordinfo.suggesters.dominance import DominanceDedupSuggester, DominanceEliminationSuggester, DominanceSuggester
from wordinfo.suggesters.entropy import EntropySuggester, PopularEntropySuggester, PopularEntropyEliminationSuggester
from wordinfo.suggesters.rank import RankDedupSuggester, RankSuggester, RankEliminationSuggester
from wordinfo.utils import WordSource, load_word_frequency_list, load_word_list

logger = getLogger(__name__)


@dataclass
class BenchmarkResult:
    """
    Container for the benchmark results.
    """
    suggester: Suggester
    total_time: float
    average_time: float
    max_attempts: int
    average_attempts: int
    success_percent: float
    failed_words: list


def benchmark_method(words, suggester, fixed_suggestions=None):
    """
    Benchmark the specified word suggester vs the list of words.
    :param words: List of words to test the suggester on.
    :param suggester: The algorithm to use for suggesting words.
    :param fixed_suggestions: A list of fixed words to use first.
    :return: Benchmark results containing how well the suggester did.
    """
    fixed_suggestions = [] if fixed_suggestions is None else fixed_suggestions

    t1 = time()
    results = []
    failed_words = []
    solver = Solver()
    print(f'Benchmarking {suggester.name}')

    for i, target_word in enumerate(words):
        solved, tried_words, results_array = solver.solve(
            suggester=suggester,
            fixed_suggestions=fixed_suggestions,
            wordle=Wordle(target_word)
        )
        if len(tried_words) > 6:
            failed_words.append(target_word)

        results.append(len(tried_words))

        if i % 200 == 0:
            print(f'{suggester.name} - {i} / {len(words)}')

    total_time = time() - t1
    average_time = total_time / len(results)
    average_attempts = mean(results)
    max_attempts = max(results)
    success_percent = len([r for r in results if r <= 6])/len(results)*100

    print(f'Complete {suggester.name}')

    return BenchmarkResult(
        suggester=suggester,
        total_time=total_time,
        average_time=average_time,
        max_attempts=max_attempts,
        average_attempts=average_attempts,
        success_percent=success_percent,
        failed_words=failed_words
    )


def run_benchmarks():
    """
    Run all benchmarks.
    """
    words = load_word_list(WordSource.SOLUTIONS)
    full_word_list = load_word_list(WordSource.FULL)
    word_frequency_map = load_word_frequency_list()
    cache = Path('./cache')

    suggesters = [
        RankSuggester(full_word_list),
        RankEliminationSuggester(full_word_list, elimination_attempts=2),
        RankEliminationSuggester(full_word_list, elimination_attempts=3),
        RankEliminationSuggester(full_word_list, elimination_attempts=4),
        RankEliminationSuggester(full_word_list, elimination_attempts=5),
        RankDedupSuggester(full_word_list),
        DominanceSuggester(full_word_list),
        DominanceDedupSuggester(full_word_list),
        DominanceEliminationSuggester(full_word_list, elimination_attempts=2),
        DominanceEliminationSuggester(full_word_list, elimination_attempts=3),
        DominanceEliminationSuggester(full_word_list, elimination_attempts=4),
        DominanceEliminationSuggester(full_word_list, elimination_attempts=5),
        EntropySuggester(full_word_list, cache),
        PopularEntropySuggester(full_word_list, cache, word_frequency_map),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
    ]

    with ProcessPoolExecutor() as ex:
        promises = [ex.submit(benchmark_method, words, suggester=suggester) for suggester in suggesters]

    results = [result.result() for result in as_completed(promises)]
    results.sort(key=lambda x: (-x.success_percent, x.average_attempts, x.average_time))

    format_header = '{:>35} {:>15} {:>15} {:>15} {:>15} {:>15}'
    format_row = '{:>35} {:>15.3f} {:>15.3f} {:>15.6f} {:>15.3f} {:>15}'

    print(format_header.format('Method', 'Success %', 'Total Seconds', 'Avg Seconds', 'Avg Tries', 'Max Tries'))
    for result in results:
        print(format_row.format(
            result.suggester.name,
            result.success_percent,
            result.total_time,
            result.average_time,
            result.average_attempts,
            result.max_attempts
        ))

# def print_results(result):
#     print(f"""
# Method: {result[0]}
# Success: {result[1].success_percent:.3f}%
# Total Time: {result[1].total_time:.3f}s / {result[1].average_time:.6f}s ea'
# Avg Tries: {result[1].average_attempts:.3f}
# Max Tries: {result[1].max_attempts}
# Failed Words: {len(result[1].failed_words)} - {result[1].failed_words}
#     """)


if __name__ == '__main__':
    logging_config = dict(
        level=INFO,
        format='%(asctime)s %(message)s'
        # format='[%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s] %(message)s'
    )

    basicConfig(**logging_config)

    run_benchmarks()
