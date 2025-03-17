"""
Читаем входные данные:

Последовательно обрабатываем каждое число n.
Игровая логика:

Игра начинается с p = 1.
Игроки (Стен и Олли) по очереди умножают p на число от 2 до 9.
Первый, кто достигнет p ≥ n, выигрывает.
Они играют идеально, то есть всегда выбирают оптимальный множитель.
Определяем победителя:

Если p достигает n на ходе Стэна → Stan wins.
Если на ходе Олли → Ollie wins.
Выводим результат:

Печатаем победителя для каждого n.
"""

import sys


def determine_winner(n):
    p = 1
    turn = True  # True for Stan, False for Ollie

    while p < n:
        if turn:
            p *= 9  # Stan tries to maximize the growth
        else:
            p *= 2  # Ollie tries to slow down the growth
        turn = not turn

    return "Stan wins" if not turn else "Ollie wins"


def main():
    for line in sys.stdin:
        n = int(line.strip())
        print(determine_winner(n))


if __name__ == "__main__":
    main()
