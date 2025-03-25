"""
Предварительный расчет чисел Стирлинга первого рода:

Числа Стирлинга s(n, k) представляют количество перестановок из n элементов с
k рекордами (элементами, которые являются максимальными на момент их добавления).

Используем рекуррентное соотношение: s(n, k) = s(n-1, k-1) + (n-1)*s(n-1, k).

Обработка каждого тестового случая:

Для перестановки длины N с P рекордами слева и R рекордами справа разбиваем задачу на подзадачи,
учитывая позицию максимального элемента.

Максимальный элемент разделяет перестановку на левую и правую части. Количество способов
для левой части с P-1 рекордами и правой части с R-1 рекордами умножается на биномиальный коэффициент
выбора позиции максимума.

Суммирование по всем возможным позициям максимума:

Для каждой позиции максимума k вычисляем количество перестановок, комбинируя результаты для левой
и правой частей с использованием предварительно рассчитанных чисел Стирлинга.
"""

import math


def precompute_stirling(max_n):
    max_k = max_n
    stirling = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    stirling[0][0] = 1
    for n in range(1, max_n + 1):
        for k in range(1, n + 1):
            stirling[n][k] = stirling[n - 1][k - 1] + (n - 1) * stirling[n - 1][k]
    return stirling


max_n_stirling = 13
stirling = precompute_stirling(max_n_stirling)


def solve():
    idx = 0
    T = int(input())
    idx += 1
    for _ in range(T):
        N, P, R = map(int, input().split())
        idx += 3
        if N == 1:
            print(1 if P == 1 and R == 1 else 0)
            continue
        if P < 1 or R < 1:
            print(0)
            continue
        total = 0
        for k in range(1, N + 1):
            left_n = k - 1
            left_p = P - 1
            right_n = N - k
            right_r = R - 1

            c = math.comb(N - 1, k - 1)

            s_left = 0
            if left_n >= 0 and left_p >= 0 and left_n >= left_p:
                if left_n <= max_n_stirling:
                    s_left = stirling[left_n][left_p]

            s_right = 0
            if right_n >= 0 and right_r >= 0 and right_n >= right_r:
                if right_n <= max_n_stirling:
                    s_right = stirling[right_n][right_r]

            total += c * s_left * s_right
        print(total)


if __name__ == "__main__":
    solve()
