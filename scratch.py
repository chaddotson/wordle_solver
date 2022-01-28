from cgitb import text
from collections import Counter
from pprint import pprint
import re
from tkinter import scrolledtext
from turtle import right


def get_score_by_letter(words):
    counter = Counter()

    for word in words:
        counter.update(word)

    min_count = min(counter.values())

    score_by_letter = {}
    for letter, count in counter.items():
        score_by_letter[letter] = count/min_count

    return score_by_letter


def score_word(score_by_letter, word):
    value = 0
    for letter in word:
        value += score_by_letter[letter]
    return value




regex = re.compile('[A-Z\d/\.&!\'\-()\x03\x07\x08]')

with open('./wordinfo/data/wordle.txt', 'r') as f:
    words = [l.strip('\n').lower() for l in f.readlines() if not regex.search(l) and len(l) == 6]








score_by_letter = get_score_by_letter(words)
print(score_by_letter)





# words = [word for word in words if not any(c > 1 for c in Counter(word).values())]

word_score = {word: score_word(score_by_letter, word) for word in words}


# max_word = ''
# max_score = 0
# for word, score in word_score.items():
#     if score > max_score:
#         max_score = score
#         max_word = word
# print(max_word, max_score)



ranked = sorted([(word, score) for word, score in word_score.items()], key=lambda x: x[1], reverse=True)


# pprint(ranked[:200])



for index, pair in enumerate(ranked):
    print(f'{index+1:4} {pair[0]} {pair[1]:.3f}')

# for index, pair in enumerate(ranked[-20:]):
#     print(f'{index+1:4} {pair[0]} {int(pair[1])}')



# from itertools import groupby


# grouped = {}
# for group, data in groupby(ranked, lambda x: x[1]):
#     grouped[group] = list(data)


# print(grouped)



# temp = re.compile('[w..]{3}ce')

# temp = re.compile('^(?=.*w)(?=.*c)(?=.*i)(?:(?!c)[a-z][a-z](?!i)[a-z][a-z])e$')
# temp = re.compile('^(?=.*o)(?!.*s)(?!.*b)(?!.*n)(?!.*k)(?!.*t)(?!.*u)(?!.*f)(?!.*a)(?!.*e)(?!.*g)(?!.*l)(?:cri[a-z]p)$')

temp = re.compile('^(?=.*o)(?=.*l)(?=.*k)(?!.*a)(?!.*r)(?!.*i)(?!.*s)(?!.*e)(?!.*d)(?!.*u)(?!.*b)(?!.*t)(?:[a-z](?!l)[a-z]o[a-z](?!k)[a-z])$')


print('----', len(words))
for word in words:
    if temp.search(word):
        print(word, word_score[word])



# # ^(?=.*?i.*?)(?:[a-z][a-z](?!i)[a-z])ce$


# # a!r!o!s!e$
# # c@h!i@d!e$


# from tkinter import *

# from functools import partial

# def handle_click(event, cell_states, state_row, state_column):
#     if cell_states[state_row][state_column] == 0:
#         cell_states[state_row][state_column] = 1
#         event.widget.configure(bg='yellow')
#     elif cell_states[state_row][state_column] == 1:
#         cell_states[state_row][state_column] = 2
#         event.widget.configure(bg='green')
#     else:
#         cell_states[state_row][state_column] = 0
#         # event.widget.configure(bg='systemTextBackgroundColor')
#         event.widget.configure(bg='white')


# def character_limit(*args, **kwargs): #widget, max_len):
#     print(args, kwargs)
#     # print(widget.get())
#     # if len(widget.get()) > max_len:
#     #     widget.set(widget.get()[0:max_len])



# def maxlen_validation(input):
#     return len(input) < 2



# window = Tk()

# registered_maxlen_validator = window.register(maxlen_validation)


# cell_states = [[0] * 5 for _ in range(6)]
# cell_values = []
# for i in range(6):
#     cell_values.append([])
#     for j in range(5):
#         var = StringVar()
#         var.trace("w", partial(character_limit, max_len=1))
#         cell_values[i].append(var)

# print(cell_states)


# info = {
#     'a': {
#         'at': 0,
#         'not_at': 2,
#         'invalid': False
#     }
# }



# window.title("Wordle Helper")

# tester = 'x'

# guess_grid = []


# guess_pane = Frame(window)
# guess_pane.pack(side=LEFT, anchor=NW, padx=15, pady=15)
# for i in range(6):
#     guess_grid.append([])
#     row_pane = Frame(guess_pane)
#     row_pane.pack(side=TOP)
#     row_label = Label(row_pane, text=f'{i+1}', width=2)
#     row_label.pack(side=LEFT)
#     # row_label.grid(column=0, row=i)

#     for j in range(5):
#         tmp = Entry(row_pane, width=1, textvariable=cell_values[i][j], fg='black', bg='white')
#         # tmp.grid(column=j+1, row=i)
#         tmp.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=i, state_column=j))
#         tmp.config(validate ="key", validatecommand =(registered_maxlen_validator, '%P'))
#         tmp.pack(side=LEFT)
#         guess_grid.append(tmp)



# def clear():
#     for row in range(6):
#         for col in range(5):
#             cell_values[row][col].set('')
#     suggestions_area.delete(1.0, END)

# def suggest():
#     data = {}
    
#     at = []
#     not_at = {}
#     invalids = {}
#     for row in range(6):
#         for col in range(5):
#             val = cell_values[row][col].get()
#             if val == '':
#                 continue
#             if not val == '':
#                 max_row = row
#             if cell_states[row][col] == 0:
#                 invalids.add(val)
#             elif cell_states[row][col] == 1:
#                 if col not in not_at:
#                     not_at[col] = set()
#                 not_at[col].add()
#             else:
#                 data[val]['at'] = col


#             # if val not in data:
#             #     data[val] = dict(
#             #         at=None,
#             #         not_at=set(),
#             #         invalid=False
#             #     )
#             # # if val == '':
#             # #     print(row, col)
#             # if cell_states[row][col] == 0:
#             #     data[val]['invalid'] = True
#             # elif cell_states[row][col] == 1:
#             #     data[val]['not_at'].add(col)
#             # else:
#             #     data[val]['at'] = col
            
            
#     print('data', data)
    
#     suggestions_area.delete(1.0, END)

# clear_button = Button(guess_pane, text='Clear', command=clear)
# clear_button.pack(side=LEFT)

# generate_button = Button(guess_pane, text='Suggest', command=suggest)
# generate_button.pack(side=LEFT)

# test = """
# a
# b
# c
# d
# e
# f
# g
# h
# i
# j
# k
# l
# m
# n
# o
# p
# q
# r
# s
# t
# u
# v
# """


# from tkinter.scrolledtext import ScrolledText
# from tkinter.font import Font


# Label(window, text='Suggestions').pack(side=TOP, anchor=NW)
# suggestions_area = ScrolledText(window, width=27, height=17)
# suggestions_area.pack(side=LEFT, anchor=NW)


# myFont = Font(family="mono", size=20)#, weight="bold", slant="italic")
# suggestions_area.config(font=myFont)

# suggestions_area.delete(1.0, END)

# suggestions_area.insert(INSERT, test)



# # generate_button.grid(column=1, row=7)

# # row1letter1=Entry(window, width=1, textvariable=cell_values[0][0], fg='black', bg='white')
# # row1letter2=Entry(window, width=1, textvariable=cell_values[0][1], fg='black', bg='white')

# # row1letter1.grid(column=1, row=1)
# # row1letter2.grid(column=2, row=1)

# # row1letter1.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=0, state_column=0))
# # row1letter2.bind("<Double-Button-1>", partial(handle_click, cell_states=cell_states, state_row=0, state_column=0))

# # row1letter1.config(validate ="key", validatecommand =(registered_maxlen_validator, '%P'))




# # row2letter1=Entry(window, width=1, text='')
# # row2letter2=Entry(window, width=1, text='')

# # row2letter1.grid(column=1, row=2)
# # row2letter2.grid(column=2, row=2)

# window.geometry("550x450+50+50")
# window.mainloop()

# print(cell_values[0][0].get())
# print(cell_states)