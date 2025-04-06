from typing import List, Tuple, Set

# Направления для движения между клетками по сторонам
# (dy, dx, from_part, to_part)
DIRS = [
    (-1, 0, 0, 2),  # верх
    (0, 1, 1, 3),  # право
    (1, 0, 2, 0),  # низ
    (0, -1, 3, 1),  # влево
]


class MazeSolver:
    def __init__(self, w: int, h: int, grid: List[str]):
        self.w = w
        self.h = h
        self.grid = grid
        self.visited = [[[False] * 4 for _ in range(w)] for _ in range(h)]
        self.cycles = 0
        self.max_len = 0

    def _dfs(self, y: int, x: int, part: int) -> Tuple[int, bool]:
        stack = [(y, x, part)]
        self.visited[y][x][part] = True
        visited_parts: Set[Tuple[int, int, int]] = set()
        visited_cells: Set[Tuple[int, int]] = set()
        is_cycle = True

        while stack:
            cy, cx, cp = stack.pop()
            visited_parts.add((cy, cx, cp))
            visited_cells.add((cy, cx))

            ch = self.grid[cy][cx]

            # Внутренние переходы внутри клетки
            if ch == '/':
                if cp == 0 and not self.visited[cy][cx][3]:
                    self.visited[cy][cx][3] = True
                    stack.append((cy, cx, 3))
                elif cp == 3 and not self.visited[cy][cx][0]:
                    self.visited[cy][cx][0] = True
                    stack.append((cy, cx, 0))
                elif cp == 1 and not self.visited[cy][cx][2]:
                    self.visited[cy][cx][2] = True
                    stack.append((cy, cx, 2))
                elif cp == 2 and not self.visited[cy][cx][1]:
                    self.visited[cy][cx][1] = True
                    stack.append((cy, cx, 1))

            elif ch == '\\':
                if cp == 0 and not self.visited[cy][cx][1]:
                    self.visited[cy][cx][1] = True
                    stack.append((cy, cx, 1))
                elif cp == 1 and not self.visited[cy][cx][0]:
                    self.visited[cy][cx][0] = True
                    stack.append((cy, cx, 0))
                elif cp == 2 and not self.visited[cy][cx][3]:
                    self.visited[cy][cx][3] = True
                    stack.append((cy, cx, 3))
                elif cp == 3 and not self.visited[cy][cx][2]:
                    self.visited[cy][cx][2] = True
                    stack.append((cy, cx, 2))

            # Переходы к соседним клеткам
            for dy, dx, from_p, to_p in DIRS:
                if cp == from_p:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < self.h and 0 <= nx < self.w:
                        if not self.visited[ny][nx][to_p]:
                            self.visited[ny][nx][to_p] = True
                            stack.append((ny, nx, to_p))
                    else:
                        is_cycle = False

        return len(visited_cells), is_cycle

    def solve(self) -> Tuple[int, int]:
        for y in range(self.h):
            for x in range(self.w):
                for p in range(4):
                    if not self.visited[y][x][p]:
                        length, is_cycle = self._dfs(y, x, p)
                        if is_cycle:
                            self.cycles += 1
                            self.max_len = max(self.max_len, length)
        return self.cycles, self.max_len


if __name__ == "__main__":
    idx = 1
    while True:
        w, h = map(int, input().split())
        if w == 0 and h == 0:
            break
        grid = []
        for _ in range(h):
            grid.append(input())
        solver = MazeSolver(w, h, grid)
        count, longest = solver.solve()
        if count == 0:
            print(f"Maze #{idx}:\nThere are no cycles.\n")
        else:
            print(f"Maze #{idx}:\n{count} Cycles; the longest has length {longest}.\n")
        idx += 1