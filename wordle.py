import random
from art import text2art
from colorama import init, Fore, Back, Style

def play(guess, word):
    guess = guess.upper()
    word = word.upper()

    if guess == word:
        return 'Won', [(guess[i], 'GREEN') for i in range(0, len(guess))]
    else:
        result = ['_', '_', '_', '_', '_']
        wrong_indexes = []
        wrong_letters = []

        for i in range(0, len(guess)):
            if guess[i] == word[i]:
                result[i] = (word[i], 'GREEN')
            else:
                wrong_indexes.append(i)
                wrong_letters.append(word[i])

        for i in wrong_indexes:
            if guess[i] in wrong_letters:
                result[i] = (guess[i], 'YELLOW')
                wrong_letters.remove(guess[i])
            else:
                result[i] = (guess[i], 'LIGHTBLACK_EX')

        return 'Lost', result


init()
print(text2art("Wordle"))

with open('words.txt', 'r', encoding='utf8') as f:
    words = f.read().splitlines()
    word = words[random.randint(0, len(words))]
    f.close()

print('Попробуйте угадать слово: \n')

state = 'Lost'
history = []
while len(history) < 6:
    guess = input('> ')
    if len(guess) != len(word):
        print('Неправильное слово, попробуйте ещё раз\n')
        continue
    print('- - - - -')
    state, result = play(guess, word)
    history.append(result)
    for n in history:
        for letter in n:
            print(Fore.LIGHTWHITE_EX + Style.BRIGHT +
                  eval('Back.' + letter[1]) + letter[0] +
                  Back.BLACK + '' + Style.RESET_ALL,
                  end=' ')
        print('\n- - - - -')
    if state == 'Won':
        print('Вы победили!')
        break
else:
    print('Вы проиграли :( Мы загадывали слово', word)
