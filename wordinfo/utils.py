from datetime import date
from enum import Enum
from pathlib import Path
import re

DATA_PATH = Path(__file__).parent / 'data'


class WordSource(Enum):
    WORDLE_SOLUTIONS = DATA_PATH / 'wordle_solutions.txt'
    WORDLE_FULL = DATA_PATH / 'wordle_full.txt'
    NYT_WORDLE_SOLUTIONS = DATA_PATH / 'new_nyt_wordle_solutions.txt'
    NYT_WORDLE_FULL = DATA_PATH / 'new_nyt_wordle_full.txt'


def load_word_list(wordset=WordSource.NYT_WORDLE_SOLUTIONS):
    regex = re.compile('[A-Z\d/\.&!\'\-()\x03\x07\x08]')
    with open(wordset.value, 'r') as f:
        return [l.strip('\n').lower() for l in f.readlines() if not regex.search(l) and len(l) == 6]



def get_word_of_day(wordlist):
    start_date = date(year=2021, month=6, day=19)
    today = date.today()
    index = (today - start_date).days
    return index, wordlist[index]


REPRESENTATION_MAP = {
    2: '🟩',
    1: '🟨',
    0: '⬛'
}


def get_result_representation(results):
    representation = ''
    for r in results:
        for i in r:
            representation += REPRESENTATION_MAP[i]
        representation += '\r\n'
    return representation
