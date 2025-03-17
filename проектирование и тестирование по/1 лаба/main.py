"""
Читаем входные данные, представляющие собой несколько полей.
Для каждого поля:
Создаем матрицу, заменяя . на 0 и * оставляя как есть.
Обходим поле и увеличиваем счетчики соседних ячеек, если текущая ячейка — мина (*).
Выводим результат в требуемом формате.
Повторяем процесс для всех входных полей, пока не встретим 0 0, что означает конец ввода.
"""
idx = 1
while True:
    n, m = map(int, input().split())
    if n == m == 0:
        break
    field = []
    for i in range(n):
        field.append([])
        for j in input():
            field[i].append(0 if j == "." else "*")
    for i in range(n):
        for j in range(m):
            if field[i][j] == "*":
                for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m and field[ni][nj] != "*":
                        field[ni][nj] += 1

    if idx > 1:
        print()  # Пустая строка между полями
    print(f"Field #{idx}:")

    for i in range(n):
        print(''.join(map(str, field[i])))

    idx += 1
