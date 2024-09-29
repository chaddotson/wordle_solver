
from wordinfo.utils import (
    WordSource, get_result_representation, get_word_of_day, load_word_frequency_list, load_word_list
)


words = load_word_list(WordSource.FULL)


similar_words = {}

for i, word1 in enumerate(words):
    if i % 1000 == 0:
        print(i)
    for j in range(i + 1, len(words)):
        word2 = words[j]

        letter_diff_pattern = ''.join(a if a == b else '_' for a, b in zip(word1, word2))

        if letter_diff_pattern.count('_') == 1:

            if letter_diff_pattern not in similar_words:
                similar_words[letter_diff_pattern] = set()

            similar_words[letter_diff_pattern].add(word1)
            similar_words[letter_diff_pattern].add(word2)


print(similar_words)

from json import dump

#
# for key in similar_words:
#     similar_words[key] = list(similar_words[key])

similar_words = {k: list(v) for k, v in similar_words.items()}


with open('similar_words.json', 'w') as f:
    dump(similar_words, f)

['pound', 'parry', 'goner', 'hatch', 'craze', 'cater', 'foyer', 'wacky', 'cling', 'booze', 'mound', 'embed',
 'savvy', 'eater', 'clink', 'stung', 'tatty', 'hitch', 'stint', 'stunt', 'boxer', 'bitty', 'saucy', 'gassy',
 'latch', 'mover', 'piper', 'maize', 'shale', 'ninny', 'tripe', 'kinky', 'filer', 'munch', 'moose', 'batch',
 'golly', 'stash', 'roger', 'rower']

['hatch', 'jaunt', 'cater', 'cinch', 'graze', 'racer', 'cider', 'wight', 'shale', 'ninny', 'waver', 'stave', 'greed', 'fizzy', 'kinky', 'roger']

