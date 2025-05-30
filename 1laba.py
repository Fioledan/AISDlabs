DIGITS = {'0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре', 
          '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'}

with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read().split()
    
first_num_found = False
for word in text:
    if word.replace('.', '', 1).isdigit():  
        if '.' in word and len(word.split('.')[1]) <= 7:  
            if not first_num_found:
                print(' '.join(DIGITS[d] for d in word if d.isdigit()), end=' ')
                first_num_found = True
            else:
                print(word.replace('.', ','), end=' ')
        else:
            print(word, end=' ')
    else:
        print(word, end=' ')