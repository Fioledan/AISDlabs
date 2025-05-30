import re

DIGITS = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
          '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}

with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

numbers = re.findall(r'\b\d+\.\d{1,7}\b', text)
words = re.split(r'\s+', text)

first_num_found = False
for word in words:
    if word in numbers:
        if not first_num_found:
            print(' '.join(DIGITS[d] for d in word if d.isdigit()), end=' ')
            first_num_found = True
        else:
            print(word.replace('.', ','), end=' ')
    else:
        print(word, end=' ')

