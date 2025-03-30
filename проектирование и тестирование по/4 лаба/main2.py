"""
Алгоритм
Сортировка слонов: Сортируем слонов по возрастанию веса.
При одинаковых весах сортируем по убыванию IQ.

Поиск наибольшей последовательности: Используем динамическое программирование
для поиска наибольшей последовательности, где вес строго возрастает, а IQ строго убывает.

Восстановление последовательности: После нахождения максимальной длины восстанавливаем последовательность слонов.
"""

import sys


class Elephant:
    def __init__(self, weight, iq, index):
        self.weight = weight
        self.iq = iq
        self.index = index


def main():
    elephants = []
    idx = 1
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        weight = int(parts[0])
        iq = int(parts[1])
        elephants.append(Elephant(weight, iq, idx))
        idx += 1

    # Сортируем по возрастанию веса, а при одинаковом весе - по убыванию IQ
    elephants.sort(key=lambda x: (x.weight, -x.iq))

    n = len(elephants)
    dp = [1] * n
    prev = [-1] * n

    for i in range(n):
        for j in range(i):
            if elephants[j].weight < elephants[i].weight and elephants[j].iq > elephants[i].iq:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j

    max_length = max(dp)
    max_index = -1
    # Ищем слона с максимальной длиной и максимальным IQ
    for i in range(n):
        if dp[i] == max_length:
            if max_index == -1 or elephants[i].iq > elephants[max_index].iq:
                max_index = i

    sequence = []
    current = max_index
    while current != -1:
        sequence.append(elephants[current].index)
        current = prev[current]

    sequence.reverse()

    print(max_length)
    for num in sequence:
        print(num)


if __name__ == "__main__":
    main()
