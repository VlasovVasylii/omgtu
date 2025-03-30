"""
Описание алгоритма:

Чтение входных данных и построение графа.
Для каждого тестового блока читаются количество уже существующих пожарных депо
и количество перекрёстков. Затем считываются номера перекрёстков с пожарными депо и список рёбер (дорог) графа.
Граф хранится в виде списка смежности, где для каждого перекрёстка фиксируются все его соседние перекрёстки с весами рёбер.

Вычисление расстояний до ближайшего депо.
Сначала с помощью модифицированного алгоритма Дейкстры (мульти-источников)
 вычисляются кратчайшие расстояния d[i] от каждого перекрёстка до ближайшего уже существующего пожарного депо.

Перебор кандидатов для нового депо.
Для каждого перекрёстка (от 1 до i) считаем, что на нём можно построить новый депо.
Снова с помощью алгоритма Дейкстры вычисляем кратчайшие расстояния от этого кандидата до всех перекрёстков.
Для каждого перекрёстка берём минимум из двух значений: расстояния до ближайшего существующего депо и расстояния
до кандидата. Тогда максимальное из таких минимальных расстояний по всем перекрёсткам
будет характеризовать качество выбранного кандидата.

Выбор лучшего кандидата.
Среди всех кандидатов выбирается тот, у которого значение максимального расстояния минимально.
 При равенстве выбирается кандидат с наименьшим номером перекрёстка.

Формирование вывода.
Для каждого тестового блока выводится номер перекрёстка, на котором нужно построить депо,
при этом блоки разделяются пустой строкой.
"""

import sys
import heapq


def dijkstra(graph, start, n):
    """
    Алгоритм Дейкстры для нахождения кратчайших расстояний от вершины start до всех остальных.
    graph: список смежности.
    """
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[start] = 0
    hq = [(0, start)]
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(hq, (nd, v))
    return dist


def multi_source_dijkstra(graph, sources, n):
    """
    Мульти-источниковая Дейкстра.
    sources: список вершин-источников.
    Возвращает список dist, где dist[u] – расстояние от ближайшего источника до u.
    """
    INF = float('inf')
    dist = [INF] * (n + 1)
    hq = []
    for src in sources:
        dist[src] = 0
        heapq.heappush(hq, (0, src))
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(hq, (nd, v))
    return dist


def solve_problem(input_str):
    """
    Основная функция решения задачи.
    Принимает строку с входными данными, возвращает строку с результатом.
    """
    lines = input_str.strip().splitlines()
    lines = [line.strip() for line in lines if line.strip() != '']

    t = int(lines[0])
    index = 1
    outputs = []

    for _ in range(t):
        f, i = map(int, lines[index].split())
        index += 1
        fire_stations = []

        for _ in range(f):
            fire_stations.append(int(lines[index]))
            index += 1

        graph = [[] for _ in range(i + 1)]
        while index < len(lines) and len(lines[index].split()) == 3:
            u, v, w = map(int, lines[index].split())
            graph[u].append((v, w))
            graph[v].append((u, w))
            index += 1

        # Шаг 1: вычисляем расстояния до ближайшего уже существующего депо.
        base_dist = multi_source_dijkstra(graph, fire_stations, i)

        best_candidate = None
        best_max = float('inf')

        # Шаг 2: перебираем все перекрёстки как кандидаты для нового депо
        for cand in range(1, i + 1):
            # Считаем расстояния от кандидата до всех других вершин
            cand_dist = dijkstra(graph, cand, i)
            current_max = 0
            # Для каждого перекрёстка рассматриваем минимальное расстояние до депо (существующего или кандидата)
            for u in range(1, i + 1):
                current_max = max(current_max, min(base_dist[u], cand_dist[u]))

            # Выбираем кандидата с минимальным максимальным расстоянием
            if current_max < best_max or (current_max == best_max and cand < best_candidate):
                best_max = current_max
                best_candidate = cand

        outputs.append(str(best_candidate))

    return "\n\n".join(outputs)


def main():
    input_str = sys.stdin.read()
    output_str = solve_problem(input_str)
    sys.stdout.write(output_str)


if __name__ == '__main__':
    main()
