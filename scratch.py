# import re
# import requests
#
#
# wordle_url = 'https://www.nytimes.com/games/wordle/index.html'
# js_url = 'https://www.nytimes.com/games/wordle/main.{release_hash}.js'
#
# response = requests.get(wordle_url)
#
#
#
# found = re.findall('window.wordle.hash ?= ?\'(.*)\';', response.text, re.IGNORECASE | re.MULTILINE)
#
#
# print(found)
# release_hash = found[0]
#
#
# response = requests.get(js_url.format(release_hash=release_hash))
#
#
# print(response.text)
import statistics
from difflib import SequenceMatcher
from itertools import combinations

from wordinfo.utils import WordSource, load_word_list

words = load_word_list(WordSource.FULL)

failed_words = ['paper', 'booby', 'crass', 'start', 'weary', 'foyer', 'trite', 'class', 'dandy', 'catch', 'daddy', 'aging', 'eater', 'tatty', 'bluer', 'joker', 'brass', 'hitch', 'boxer', 'ember', 'grass', 'bound', 'sheer', 'wafer', 'scout', 'merry', 'state', 'batch', 'golly', 'brown', 'staid', 'vaunt', 'willy', 'mercy']

for word in failed_words:
    # ifflib.SequenceMatcher(None, word,)
    #similar = [x for x in words if SequenceMatcher(None, word, x).ratio() == (len(word) - 1) / float(len(word))]
    similar = [w for w in words if sum(a != b for a, b in zip(word, w)) == 1]
    print(word, similar)









# from statistics import mean
# from random import choice
#
# from wordinfo.solver import Solver, Wordle
# from wordinfo.suggesters.dominance import DominanceSuggester, DominanceModifiedSuggester, \
#     get_posititional_dominance, dominance_score_word
# from wordinfo.suggesters.rank import RankModifiedSuggester, get_score_by_letter, score_word
# from wordinfo.old_solver import SolverMethods, solve_wordle
# from wordinfo.utils import load_word_list, get_result_representation, WordSource
#
# # 🟨🟨⬛🟨⬛
# # ⬛⬛🟨⬛⬛
# # 🟩🟩🟩🟩🟩
#
#
# words = load_word_list(WordSource.WORDLE)
#
# #
# #
# # solver = Solver()
# #
# # # found, tries, results = solver.solve(
# # #     suggester=RankModifiedSuggester(words),
# # #     fixed_suggestions=[],
# # #     word_tester=WordTester('could')
# # # )
# #
# # from time import time
# #
# # t1 = time()
# # results = []
# #
# # suggester = DominanceSuggester(words)
# # for i, target_word in enumerate(words):#range(runs):
# #     #arget_word = words[i]#choice(words)
# #     solved, tried_words, results_array = solver.solve(
# #         suggester=suggester,
# #         fixed_suggestions=[],
# #         wordle=Wordle(target_word)
# #     )
# #
# #     results.append(len(tried_words))
# #     # representation = get_result_representation(results_array)
# #
# #     # print(target_word)
# #     # print(representation)
# #
# # average_tries = mean(results)
# # success_percent = len([r for r in results if r <=6])/len(results)*100
# #
# #
# # print(f'Avg Tries: {average_tries:.2f}')
# # print(f'Success: {success_percent:.2f}%')
# #
# # total_time = time() - t1
# # print(f'Total Time: {total_time:.2f}s / {total_time / len(results):.6f}s ea')
# # exit()
#
#
# from collections import Counter
# from wordinfo.solver import LetterTracker
# from wordinfo.suggesters.utils import generate_regex
#
# from enum import Enum
#
# class LetterVerdict(Enum):
#     INVALID = 0
#     INCORRECT = 1
#     CORRECT = 2
#
# WORDLE_SIZE = 5
# target_word = 'tares'
#
#
#
# possible_outcomes_for_target = []
# for word in words:
#     outcome = [LetterVerdict.INVALID] * WORDLE_SIZE
#     for index, (l, r) in enumerate(zip(word, target_word)):
#         if l == r:
#             outcome[index] = LetterVerdict.CORRECT
#         elif l in target_word:
#             outcome[index] = LetterVerdict.INCORRECT
#     possible_outcomes_for_target.append(outcome)
# print(possible_outcomes_for_target)
#
#
# unique_results = {}
# for entry in possible_outcomes_for_target:
#     if not entry in unique_results:
#         unique_results = 0
#     unique_results[entry] += 1
#
#
# print(unique_results)
#
#
#
# # score_by_letter = get_score_by_letter(words)
# # word_score = {word: score_word(score_by_letter, set(word)) for word in words}
# # ranked = sorted([(word, score) for word, score in word_score.items()], key=lambda x: x[1], reverse=True)
# #
# # score_by_dominance = get_posititional_dominance(words)
# # dominance_word_score = {word: dominance_score_word(score_by_dominance, word) for word in words}
# # dominance_ranked = sorted([(word, score) for word, score in dominance_word_score.items()], key=lambda x: x[1], reverse=True)
# #
# #
# # print(ranked[0:10])
# # print(dominance_ranked[0:10])
# #
# # print(score_word(score_by_letter, 'roate'))
#
# # def get_get_number_of_choices(word, wordlist, letter_tracker):
# #
# # letter_tracker = LetterTracker(5)
# # word = 'arose'
# # letter_tracker.invalids.update(word)
# # regex = generate_regex([word], letter_tracker)
# #
# # import re
# #
# # word_and_possible_candidates = []
# # for word in words:
# #     letter_tracker = LetterTracker(5)
# #     letter_tracker.invalids.update('arise')
# #     letter_tracker.invalids.update(word)
# #     regex = generate_regex(['arise', word], letter_tracker)
# #     candidate_words = [w for w in words if re.search(regex, w)]
# #     # print(word, len(candidate_words))
# #     word_and_possible_candidates.append((word, len(candidate_words)))
# #
# #
# #
# # word_and_possible_candidates = sorted(word_and_possible_candidates, key=lambda x: x[1])
# #
# #
# # test = ['slate', 'surly', 'spill', 'swill', 'skill']
# # for word in test:
# #     print(word, word_score[word], dominance_word_score[word])
# #
#
# # print(word_and_possible_candidates[:5])
# # print([c for c in word_and_possible_candidates if c[1] ==5 ][:20])
# #
# # from wordinfo.solver import RankSuggester, Solver
# #
# # suggester = RankSuggester(words)
# # solver = Solver()
# #
# # results = {}
# #
# # for word in words[:10]:
# #
# #     if word not in results:
# #         results[word] = []
# #
# #     for i, target_word in enumerate(words):
# #         if target_word == word:
# #             continue
# #
# #         suggester.reset()
# #         solved, tried_words, results_array = solver.solve(
# #             suggester=suggester,
# #             fixed_suggestions=[word],
# #             wordle=Wordle(target_word)
# #         )
# #         # print(len(tried_words))
# #         results[word].append(len(tried_words))
# #
# # candidates = [(word, min(attempts)) for word, attempts in results.items()]
# #
# # candidates = sorted(candidates, key=lambda x: x[1])
# # print(candidates)
#
#
# # dedup_words = [word for word in words if not any(c > 1 for c in Counter(word).values())]
# # dedup_word_score = {word: score_word(score_by_letter, word) for word in dedup_words}
# # dedup_ranked = sorted([(word, score) for word, score in dedup_word_score.items()], key=lambda x: x[1], reverse=True)
# #
# # word_score = {word: score_word(score_by_letter, word) for word in words}
# # ranked = sorted([(word, score) for word, score in word_score.items()], key=lambda x: x[1], reverse=True)
# #
# # positional_dominance = get_posititional_dominance(words)
# # dominance_word_score = {word: dominance_score_word(positional_dominance, word) for word in words}
# # dominance_ranked = sorted([(word, score) for word, score in dominance_word_score.items()], key=lambda x: x[1], reverse=True)
# #
# #
# #
# # trials = []
# #
# #
# #
# #
# # selected_word = choice(words)
# #
# # t1 = time()
# # runs = len(words)
# # results = []
# # for i, target_word in enumerate(words):#range(runs):
# #     #arget_word = words[i]#choice(words)
# #     solved, tried_words, results_array = solve_wordle(
# #         target_word=target_word,
# #         fixed_suggestions=[],#['arise', 'could'],
# #         method=SolverMethods.RANK_MODIFIED,
# #         ranked=ranked,
# #         deduped_ranked=dedup_ranked,
# #         dominance_ranked=dominance_ranked,
# #         modifier=5
# #     )
# #
# #     results.append(len(tried_words))
# #     # print(target_word, len(tried_words))
# #
# # average_tries = mean(results)
# # success_percent = len([r for r in results if r <=6 ])/runs*100
# #
# #
# # print(f'Avg Tries: {average_tries:.2f}')
# # print(f'Success: {success_percent:.2f}%')
# # print(time() - t1)
# #
#
#
#
# #
# #
# # attempt_words = []
# # attempt_results = [[0] * 5 for i in range(6)]
# #
# # at = [None] * 5
# # not_at = {}
# # invalids = set()
# #
# #
# # fixed_suggestions = [] #['arise', 'could']
# #
# # attempt = 0
# # solved = False
# # while attempt < 6 and not solved:
# #     if attempt < len(fixed_suggestions):
# #         suggestion = fixed_suggestions[attempt]
# #     else:
# #         regex = generate_regex(attempt_words, at, not_at, invalids)
# #         suggestion = generate_suggestion_by_dominance(dominance_ranked, regex)
# #     attempt_words.append(suggestion)
# #
# #     for index, (l, r) in enumerate(zip(suggestion, selected_word)):
# #         if l == r:
# #             # position found
# #             attempt_results[attempt][index] = 2
# #             at[index] = l
# #         elif l in selected_word:
# #             # letter found
# #             attempt_results[attempt][index] = 1
# #
# #             if index not in not_at:
# #                 not_at[index] = set()
# #                 not_at[index].add(l)
# #         else:
# #             invalids.add(l)
# #
# #     # because I want to be picky and have the data, I don't exit early and I let the above record the attempt
# #     if suggestion == selected_word:
# #         solved = True
# #
# #
# #     attempt += 1
# #
# #
# #     # attempt_words.append((suggestion, score))
# #
# # print('solved', solved, attempt+1)
# # print('selected_word', selected_word)
# # print(attempt_words)
# #
# #
# #
# # print('-', attempt_results)
# # print('at', at)
# # print('not_at', not_at)
# # print('invaliud', invalids)
# #
# # letters_regex = ''.join([f'{"".join(f"(?!{nat})" for nat in not_at.get(index, []))}[a-z]' if at[index] is None else at[index] for index in range(5)])
# # contains_regex = ''.join(f'(?=.*{letter})' for position_not_ats in not_at.values() for letter in position_not_ats)
# # invalids_regex = ''.join(f'(?!.*{invalid})' for invalid in invalids)
# # total_regex = f'^{invalids_regex}{contains_regex}(?:{letters_regex})$'
# #
# #
# #
# #
# # print('letters_regex', letters_regex)
# # print('contains_regex', contains_regex)
# # print('invalids_regex', invalids_regex)
# # print('total_regex', total_regex)
# #
# #
# #
# # word, score = next(pair for pair in ranked if re.search(total_regex ,pair[0]))
# #
# # # for pair in ranked:
# # #     print(pair[0], re.search(total_regex ,pair[0]))
# # #
# # print(word, score)
#
#
# #
# # print(word_score['doubt'], dominance_word_score['doubt'])
# # print(word_score['could'], dominance_word_score['could'])
#
#
# # max_word = ''
# # max_score = 0
# # for word, score in word_score.items():
# #     if score > max_score:
# #         max_score = score
# #         max_word = word
# # print(max_word, max_score)
#
#
#
#
#
#
#
#
# # pprint(ranked[:200])
#
#
# #
# # for index, pair in enumerate(ranked[:50]):
# #     print(f'{index+1:4} {pair[0]} {pair[1]:.3f}')
# #
# #
# #
# # print('----')
# #
# # for index, pair in enumerate(dominance_ranked[:50]):
# #     print(f'{index+1:4} {pair[0]} {pair[1]:.3f}')
#
# # for index, pair in enumerate(ranked[-20:]):
# #     print(f'{index+1:4} {pair[0]} {int(pair[1])}')
#
# #
# #
# # at = []
# # not_at = {}
# # invalids = set()
# # for row in range(6):
# #     for col in range(5):
# #         val = cell_values[row][col].get()
# #         if val == '':
# #             continue
# #         if not val == '':
# #             max_row = row
# #         if cell_states[row][col] == 0:
# #             invalids.add(val)
# #         elif cell_states[row][col] == 1:
# #             if col not in not_at:
# #                 not_at[col] = set()
# #             not_at[col].add()
# #         else:
# #             data[val]['at'] = col
# #
# #
# # index = 0
# # for i in range(6):
# #     print(f'Try:', ranked[index])
# #     performance = input('How did it do (x=bad, !=used, $=right):')
# #
# #     print(performance)
# #
#
# # from itertools import groupby
#
#
# # grouped = {}
# # for group, data in groupby(ranked, lambda x: x[1]):
# #     grouped[group] = list(data)
#
#
# # print(grouped)
#
#
#
# # temp = re.compile('[w..]{3}ce')
#
# # temp = re.compile('^(?=.*w)(?=.*c)(?=.*i)(?:(?!c)[a-z][a-z](?!i)[a-z][a-z])e$')
# # temp = re.compile('^(?=.*o)(?!.*s)(?!.*b)(?!.*n)(?!.*k)(?!.*t)(?!.*u)(?!.*f)(?!.*a)(?!.*e)(?!.*g)(?!.*l)(?:cri[a-z]p)$')
#
# # temp = re.compile('^(?=.*o)(?=.*l)(?=.*k)(?!.*a)(?!.*r)(?!.*i)(?!.*s)(?!.*e)(?!.*d)(?!.*u)(?!.*b)(?!.*t)(?:[a-z](?!l)[a-z]o[a-z](?!k)[a-z])$')
# #
# #
# # print('----', len(words))
# # for word in words:
# #     if temp.search(word):
# #         print(word, word_score[word])
#
#
#
# # # ^(?=.*?i.*?)(?:[a-z][a-z](?!i)[a-z])ce$
#
#
# # # a!r!o!s!e$
# # # c@h!i@d!e$
#
#
# # from tkinter import *
#
# # from functools import partial
#
# # def handle_click(event, cell_states, state_row, state_column):
# #     if cell_states[state_row][state_column] == 0:
# #         cell_states[state_row][state_column] = 1
# #         event.widget.configure(bg='yellow')
# #     elif cell_states[state_row][state_column] == 1:
# #         cell_states[state_row][state_column] = 2
# #         event.widget.configure(bg='green')
# #     else:
# #         cell_states[state_row][state_column] = 0
# #         # event.widget.configure(bg='systemTextBackgroundColor')
# #         event.widget.configure(bg='white')
#
#
# # def character_limit(*args, **kwargs): #widget, max_len):
# #     print(args, kwargs)
# #     # print(widget.get())
# #     # if len(widget.get()) > max_len:
# #     #     widget.set(widget.get()[0:max_len])
#
#
#
# # def maxlen_validation(input):
# #     return len(input) < 2
#
#
#
# # window = Tk()
#
# # registered_maxlen_validator = window.register(maxlen_validation)
#
#
# # cell_states = [[0] * 5 for _ in range(6)]
# # cell_values = []
# # for i in range(6):
# #     cell_values.append([])
# #     for j in range(5):
# #         var = StringVar()
# #         var.trace("w", partial(character_limit, max_len=1))
# #         cell_values[i].append(var)
#
# # print(cell_states)
#
#
# # info = {
# #     'a': {
# #         'at': 0,
# #         'not_at': 2,
# #         'invalid': False
# #     }
# # }
#
#
#
# # window.title("Wordle Helper")
#
# # tester = 'x'
#
# # guess_grid = []
#
#
# # guess_pane = Frame(window)
# # guess_pane.pack(side=LEFT, anchor=NW, padx=15, pady=15)
# # for i in range(6):
# #     guess_grid.append([])
# #     row_pane = Frame(guess_pane)
# #     row_pane.pack(side=TOP)
# #     row_label = Label(row_pane, text=f'{i+1}', width=2)
# #     row_label.pack(side=LEFT)
# #     # row_label.grid(column=0, row=i)
#
# #     for j in range(5):
# #         tmp = Entry(row_pane, width=1, textvariable=cell_values[i][j], fg='black', bg='white')
# #         # tmp.grid(column=j+1, row=i)
# #         tmp.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=i, state_column=j))
# #         tmp.config(validate ="key", validatecommand =(registered_maxlen_validator, '%P'))
# #         tmp.pack(side=LEFT)
# #         guess_grid.append(tmp)
#
#
#
# # def clear():
# #     for row in range(6):
# #         for col in range(5):
# #             cell_values[row][col].set('')
# #     suggestions_area.delete(1.0, END)
#
# # def suggest():
# #     data = {}
#
# #     at = []
# #     not_at = {}
# #     invalids = {}
# #     for row in range(6):
# #         for col in range(5):
# #             val = cell_values[row][col].get()
# #             if val == '':
# #                 continue
# #             if not val == '':
# #                 max_row = row
# #             if cell_states[row][col] == 0:
# #                 invalids.add(val)
# #             elif cell_states[row][col] == 1:
# #                 if col not in not_at:
# #                     not_at[col] = set()
# #                 not_at[col].add()
# #             else:
# #                 data[val]['at'] = col
#
#
# #             # if val not in data:
# #             #     data[val] = dict(
# #             #         at=None,
# #             #         not_at=set(),
# #             #         invalid=False
# #             #     )
# #             # # if val == '':
# #             # #     print(row, col)
# #             # if cell_states[row][col] == 0:
# #             #     data[val]['invalid'] = True
# #             # elif cell_states[row][col] == 1:
# #             #     data[val]['not_at'].add(col)
# #             # else:
# #             #     data[val]['at'] = col
#
#
# #     print('data', data)
#
# #     suggestions_area.delete(1.0, END)
#
# # clear_button = Button(guess_pane, text='Clear', command=clear)
# # clear_button.pack(side=LEFT)
#
# # generate_button = Button(guess_pane, text='Suggest', command=suggest)
# # generate_button.pack(side=LEFT)
#
# # test = """
# # a
# # b
# # c
# # d
# # e
# # f
# # g
# # h
# # i
# # j
# # k
# # l
# # m
# # n
# # o
# # p
# # q
# # r
# # s
# # t
# # u
# # v
# # """
#
#
# # from tkinter.scrolledtext import ScrolledText
# # from tkinter.font import Font
#
#
# # Label(window, text='Suggestions').pack(side=TOP, anchor=NW)
# # suggestions_area = ScrolledText(window, width=27, height=17)
# # suggestions_area.pack(side=LEFT, anchor=NW)
#
#
# # myFont = Font(family="mono", size=20)#, weight="bold", slant="italic")
# # suggestions_area.config(font=myFont)
#
# # suggestions_area.delete(1.0, END)
#
# # suggestions_area.insert(INSERT, test)
#
#
#
# # # generate_button.grid(column=1, row=7)
#
# # # row1letter1=Entry(window, width=1, textvariable=cell_values[0][0], fg='black', bg='white')
# # # row1letter2=Entry(window, width=1, textvariable=cell_values[0][1], fg='black', bg='white')
#
# # # row1letter1.grid(column=1, row=1)
# # # row1letter2.grid(column=2, row=1)
#
# # # row1letter1.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=0, state_column=0))
# # # row1letter2.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=0, state_column=0))
#
# # # row1letter1.config(validate ="key", validatecommand =(registered_maxlen_validator, '%P'))
#
#
#
#
# # # row2letter1=Entry(window, width=1, text='')
# # # row2letter2=Entry(window, width=1, text='')
#
# # # row2letter1.grid(column=1, row=2)
# # # row2letter2.grid(column=2, row=2)
#
# # window.geometry("550x450+50+50")
# # window.mainloop()
#
# # print(cell_values[0][0].get())
# # print(cell_states)