from wordinfo.solver import Wordle
from wordinfo.utils import WordSource, load_word_list










words = load_word_list(WordSource.FULL)

from hashlib import md5, sha1
# words = tuple(words)
#
# print(hash(words))

from json import dumps, dump

id = sha1(dumps(words).encode()).hexdigest()[0:8]

print(id)

from wordinfo.suggesters.entropy import calculate_entroy_by_word

entropy_by_word = calculate_entroy_by_word(words)
with open('./test.json', 'w') as f:
    dump(entropy_by_word, f)

exit()
entropy_calc = {}

# for word in words:
#     wordle = Wordle(word)
#     possible_outcomes = {}
#     for w in words:
#         found, guess_result = wordle.guess(w)
#         # guess_result = tuple(guess_result)
#         if found:
#             continue
#         if guess_result not in possible_outcomes:
#             possible_outcomes[guess_result] = 0
#         possible_outcomes[guess_result] += 1
#     entropy_calc[word] = dict(
#         total_outcomes=sum(possible_outcomes.values()),
#         outcomes=possible_outcomes
#     )
#     print(entropy_calc)
#     break
#


# from math import log2
#
# def calc_part(count, word_count):
#     probability = count / word_count
#     return probability * log2(1 / probability)
#
# def calculate_entropy(word_count, outcomes):
#     return sum(calc_part(count, word_count) for count in outcomes.values())
#
# def calculate_entroy_by_word(words):
#     entropy_by_word = {}
#     for word in words:
#         wordle = Wordle(word)
#         possible_outcomes = {}
#         for w in words:
#             found, guess_result = wordle.guess(w)
#             # guess_result = tuple(guess_result)
#             if found:
#                 continue
#             if guess_result not in possible_outcomes:
#                 possible_outcomes[guess_result] = 0
#             possible_outcomes[guess_result] += 1
#
#         word_count = len(words)
#         entropy = calculate_entropy(word_count, possible_outcomes)
#         entropy_by_word[word] = entropy
#     return entropy_by_word
#

import pickle
#
# entropy_by_word = calculate_entroy_by_word(words)
# with open('./full_wordle.pickle', 'wb') as f:
#     pickle.dump(entropy_by_word, f)

# with open('wordinfo/small_list.pickle', 'rb') as f:
#     entropy_by_word = pickle.load(f)
#
# import heapq
#
# highest_entropy = heapq.nlargest(20, entropy_by_word, key=entropy_by_word.get)
#
#
# for word in highest_entropy:
#     print(f'{word} - {entropy_by_word[word]:.4f}')
#

#
#
# max_word = max(entropy_by_word, key=entropy_by_word.get)
# print(max_word, entropy_by_word[max_word])


# entropy_calc[word] = dict(
#     total_outcomes=sum(possible_outcomes.values()),
#     outcomes=possible_outcomes
# )
# print(entropy_calc)
