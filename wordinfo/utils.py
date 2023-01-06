from datetime import date
from enum import Enum
from pathlib import Path
import re
import requests

DATA_PATH = Path(__file__).parent / 'data'


class WordSource(Enum):
    SOLUTIONS = DATA_PATH / 'solutions.txt'
    FULL = DATA_PATH / 'full.txt'


def load_word_list(wordset=WordSource.FULL):
    regex = re.compile('[A-Z\d/\.&!\'\-()\x03\x07\x08]')
    with open(wordset.value, 'r') as f:
        return [l.strip('\n').lower() for l in f.readlines() if not regex.search(l) and len(l) == 6]


def get_word_of_day():
    today_url = f'https://www.nytimes.com/svc/wordle/v2/{date.today():%Y-%m-%d}.json'

    response = requests.get(today_url)

    if not response.ok:
        raise RuntimeError(f'Failed to get today\'s wordle information. URL {today_url}')

    todays_data = response.json()

    return todays_data['id'], todays_data['solution']


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
