from collections import Counter


def get_score_by_letter(words):
    counter = Counter()

    for word in words:
        counter.update(word)

    min_count = min(counter.values())

    score_by_letter = {}
    for letter, count in counter.items():
        score_by_letter[letter] = count/min_count

    return score_by_letter


def get_posititional_dominance(wordle_words):
    raw_dominance_count = {}
    for word in wordle_words:
        for index, letter in enumerate(word):
            if index not in raw_dominance_count:
                raw_dominance_count[index] = {}
            if letter not in raw_dominance_count[index]:
                raw_dominance_count[index][letter] = 0
            raw_dominance_count[index][letter] += 1

    # return raw_dominance_count
    dominance = {}
    for index, counted in raw_dominance_count.items():
        min_count = min(counted.values())

        if index not in dominance:
            dominance[index] = {}

        for letter, count in counted.items():
            # print(count)
            dominance[index][letter] = count / min_count

    return dominance


def score_word(score_by_letter, word):
    value = 0
    for letter in word:
        value += score_by_letter[letter]
    return value
#
# from functools import reduce
# def score_word(score_by_letter, word):
#     return reduce(lambda agg, letter: agg+score_by_letter[letter], word, 0)



def dominance_score_word(dominance_by_index, word):
    value = 0
    # seen_letters = set()
    for index, letter in enumerate(word):
        # if letter in seen_letters:
        #     continue
        # value += dominance_by_index[index][letter]
        value += dominance_by_index[index].get(letter, 0)
        # seen_letters.add(letter)
    return value