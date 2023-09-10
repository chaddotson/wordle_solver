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
    fixed_suggestions = []

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
        PopularEntropySuggester(full_word_list, cache, word_frequency_map, cull=5),
        PopularEntropySuggester(full_word_list, cache, word_frequency_map, cull=10),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        PopularEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=3),    # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=4),    # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=5),    # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=6),    # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=10),   # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=20),   # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=100),  # noqa: E501
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        DominananceEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=2),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=3),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=4),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=5),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=6),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=3, cull=10),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=4),
        RankEntropyEliminationSuggester(full_word_list, cache, word_frequency_map, elimination_attempts=5),
    ]

    with ProcessPoolExecutor(max_workers=6) as ex:
        promises = [ex.submit(benchmark_method, words, suggester=suggester, fixed_suggestions=fixed_suggestions) for suggester in suggesters]  # noqa: E501

    results = [result.result() for result in as_completed(promises)]
    results.sort(key=lambda x: (-x.success_percent, x.average_attempts, x.average_time))

    format_header = '{:>45} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}'
    format_row = '{:>45} {:>15.3f} {:>15.3f} {:>15.6f} {:>15.3f} {:>15} {:>15}'

    print(format_header.format('Method', 'Success %', 'Total Seconds', 'Avg Seconds', 'Avg Tries', 'Max Tries', 'Failed'))  # noqa: E501
    for result in results:
        print(format_row.format(
            result.suggester.name,
            result.success_percent,
            result.total_time,
            result.average_time,
            result.average_attempts,
            result.max_attempts,
            len(result.failed_words)
        ))
        # if result.max_attempts > 6:
        #     print(result.failed_words)


if __name__ == '__main__':
    logging_config = dict(
        level=INFO,
        format='%(asctime)s %(message)s'
        # format='[%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s] %(message)s'
    )

    basicConfig(**logging_config)

    run_benchmarks()
