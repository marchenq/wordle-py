from collections import defaultdict
from tabulate import tabulate
import re

"""
Получаем частотности символов и определяем "коэффициент частотности" для каждого слова исходя из его букв
"""
def get_frequencies(words):
    symbol_frequencies = {}
    for word in words:
        for letter in list(set(word)):
            if letter in symbol_frequencies:
                symbol_frequencies[letter] += 1
            else:
                symbol_frequencies[letter] = 1

    probabilities = {}
    total_probability = 0
    for word in words:
        total_frequency = 0
        for letter in list(set(word)):
            total_frequency += symbol_frequencies[letter]
        probabilities[word] = total_frequency
        total_probability += total_frequency

    return total_probability, probabilities


"""
Формируем регулярное выражение на основе известных положений символов
"""
def query_builder(positions):
    pattern = ''
    for i, position in enumerate(positions):
        if position == '_':
            """
            На этом положении не могут быть следующие символы
            """
            disallowed = ''.join(thrown_away | impossible_positions[i])
            pattern += '[^' + disallowed + ']'
        else:
            pattern += position
    return pattern


"""
Отфильтровываем слова, которые отвечают паттерну регулярки
"""
def sieve(words, pattern, present):
    matches = []
    for word in list(filter(re.compile(pattern).match, words)):
        """
        Если в слове, отвечающему регулярке, есть символы, которые обязательно должны быть в ответе, берём его
        """
        if present.issubset(set(word)):
            matches.append(word)
    return matches


"""
Известные положения символов:
    present - такие символы в слове точно есть
    thrown_away - таких символов в слове точно нет
    impossible_positions - на такой позиции точно не может стоять такой символ
"""
present = set()
thrown_away = set()
impossible_positions = defaultdict(lambda: set())


print('Попробуйте каждое предложенное слово и введите маску результата, где '
      '<+> - буква в правильной позиции, '
      '<?> - буква в неправильной позиции, '
      '<-> - такой буквы в слове нет: ')

with open('words.txt', 'r', encoding='utf8') as f:
    words = f.read().splitlines()
    f.close()

positions = ['_', '_', '_', '_', '_']
while '_' in positions:
    total_probability, probabilities = get_frequencies(words)

    sort = list(sorted(probabilities.items(), key=lambda x: x[1], reverse=True))
    word, probability = sort[0][0], sort[0][1]

    print(tabulate([[word, 'c вероятностью ' + str(probability/total_probability)]], tablefmt='grid'))

    mask = input('> ')
    for position, value in enumerate(mask):
        letter = word[position]  # соответствующий символ
        if value == '+':
            positions[position] = letter
        elif value == '?':
            present.add(letter)
            impossible_positions[position].add(letter)
        elif value == '-':
            thrown_away.add(letter)

    pattern = query_builder(positions)
    words = sieve(words, pattern, present)
else:
    print('Ура, мы угадали слово', ''.join(positions) + '!')
