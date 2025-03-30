"""
Алгоритм
Построение графа переходов:

Каждая клетка лабиринта обрабатывается для определения переходов
между направлениями входа и выхода в зависимости от символа ('/' или '').

Для каждой клетки и каждого направления входа (север, восток, юг, запад)
определяется направление выхода и следующая клетка.

Обход графа:

Для каждого узла (позиция и направление) запускается поиск
циклов с использованием обхода в глубину (DFS).

При обнаружении цикла подсчитывается количество уникальных клеток,
через которые он проходит, что определяет длину цикла.

Сбор результатов:

После обхода всех узлов подсчитывается количество циклов
и определяется максимальная длина.
"""

import sys


def main():
    maze_num = 0
    while True:
        w, h = map(int, sys.stdin.readline().split())
        if w == 0 and h == 0:
            break
        maze_num += 1
        maze = []

        for _ in range(h):
            line = sys.stdin.readline().strip()
            maze.append(line)

        # Строим граф переходов
        graph = dict()
        directions = ['N', 'E', 'S', 'W']
        for y in range(h):
            for x in range(w):
                cell = maze[y][x]
                for dir_in in directions:
                    key = (x, y, dir_in)
                    if cell == '/':
                        if dir_in == 'N':
                            next_dir_in = 'W'
                            next_x, next_y = x + 1, y
                        elif dir_in == 'E':
                            next_dir_in = 'S'
                            next_x, next_y = x, y - 1
                        elif dir_in == 'S':
                            next_dir_in = 'E'
                            next_x, next_y = x - 1, y
                        elif dir_in == 'W':
                            next_dir_in = 'N'
                            next_x, next_y = x, y + 1
                    else:
                        if dir_in == 'N':
                            next_dir_in = 'E'
                            next_x, next_y = x - 1, y
                        elif dir_in == 'E':
                            next_dir_in = 'N'
                            next_x, next_y = x, y + 1
                        elif dir_in == 'S':
                            next_dir_in = 'W'
                            next_x, next_y = x + 1, y
                        elif dir_in == 'W':
                            next_dir_in = 'S'
                            next_x, next_y = x, y - 1
                    # Проверяем границы
                    if 0 <= next_x < w and 0 <= next_y < h:
                        graph[key] = (next_x, next_y, next_dir_in)
                    else:
                        graph[key] = None

        # Поиск циклов
        visited = set()
        cycles = []

        for y in range(h):
            for x in range(w):
                for dir_in in directions:
                    start_node = (x, y, dir_in)
                    if start_node not in visited and start_node in graph:
                        current_node = start_node
                        path = []
                        cells = set()
                        is_cycle = False
                        local_visited = set()
                        while True:
                            if current_node is None:
                                break
                            if current_node in local_visited:
                                if current_node == start_node and len(path) > 0:
                                    is_cycle = True
                                break
                            if current_node in visited:
                                break
                            local_visited.add(current_node)
                            path.append(current_node)
                            cx, cy, _ = current_node
                            cells.add((cx, cy))
                            current_node = graph.get(current_node, None)

                        if is_cycle:
                            cycles.append(len(cells))
                            visited.update(local_visited)
                        else:
                            visited.update(local_visited)

        # Подготовка результата
        print(f"Maze #{maze_num}:")
        if not cycles:
            print("There are no cycles.")
        else:
            num_cycles = len(cycles)
            max_len = max(cycles)
            print(f"{num_cycles} Cycles; the longest has length {max_len}.")
        print()


if __name__ == "__main__":
    main()
