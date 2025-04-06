"""
Используем алгоритм Дейкстры
для вычисления кратчайших расстояний между всеми парами перекрестков.

Для каждого потенциального нового депо вычисляем, как
изменится максимальное расстояние до ближайшего депо.

Выбираем перекресток с наименьшим максимальным расстоянием и
наименьшим номером.
"""

import sys
import heapq
from collections import defaultdict


def main():
    input = sys.stdin.read().split('\n')
    ptr = 0
    T = int(input[ptr])
    ptr += 1
    for case in range(T):
        # Skip empty lines
        while ptr < len(input) and input[ptr].strip() == '':
            ptr += 1
        if ptr >= len(input):
            break

        # Read f and i
        f, i = map(int, input[ptr].split())
        ptr += 1

        # Read depots
        depots = []
        for _ in range(f):
            while ptr < len(input) and input[ptr].strip() == '':
                ptr += 1
            if ptr >= len(input):
                break
            depots.append(int(input[ptr]))
            ptr += 1

        # Build graph
        graph = defaultdict(list)
        while ptr < len(input):
            line = input[ptr].strip()
            if line == '':
                ptr += 1
                continue
            if not all(x.isdigit() for x in line.split()):
                break
            u, v, w = map(int, line.split())
            graph[u].append((v, w))
            graph[v].append((u, w))
            ptr += 1

        # Compute all pairs shortest paths using Dijkstra
        INF = float('inf')
        dist = [[INF] * (i + 1) for _ in range(i + 1)]
        for s in range(1, i + 1):
            dist[s][s] = 0
            heap = [(0, s)]
            while heap:
                d, u = heapq.heappop(heap)
                if d > dist[s][u]:
                    continue
                for v, w in graph[u]:
                    if dist[s][v] > d + w:
                        dist[s][v] = d + w
                        heapq.heappush(heap, (dist[s][v], v))

        # Compute current min distances
        min_dist = [INF] * (i + 1)
        for u in range(1, i + 1):
            for d in depots:
                if dist[d][u] < min_dist[u]:
                    min_dist[u] = dist[d][u]

        # Find best new depot
        best_max = INF
        best_k = 1
        for k in range(1, i + 1):
            temp_min = min_dist.copy()
            for u in range(1, i + 1):
                if dist[k][u] < temp_min[u]:
                    temp_min[u] = dist[k][u]
            current_max = max(temp_min[1:i + 1])
            if current_max < best_max or (current_max == best_max and k < best_k):
                best_max = current_max
                best_k = k

        print(best_k)
        if case < T - 1:
            print()


if __name__ == "__main__":
    main()
