import unittest

from main2 import solve_problem


class TestFireStationProblem(unittest.TestCase):
    def test_example(self):
        # Пример из условия задачи:
        input_data = """1

1 6
2
1 2 10
2 3 10
3 4 10
4 5 10
5 6 10
6 1 10
"""
        expected_output = "6"
        self.assertEqual(solve_problem(input_data).strip(), expected_output)

    def test_single_intersection(self):
        # Краевой случай: 1 перекресток, уже есть депо.
        input_data = """1

1 1
1
"""
        expected_output = "1"
        self.assertEqual(solve_problem(input_data).strip(), expected_output)

    def test_no_existing_improvement(self):
        # Сценарий, когда добавление нового депо не улучшает ситуацию, т.к. оно ставится там, где уже есть депо.
        input_data = """1

2 4
1
3
1 2 5
2 3 5
3 4 5
4 1 5
"""
        expected_output = "1"
        self.assertEqual(solve_problem(input_data).strip(), expected_output)

    def test_stress(self):
        # Нагрузочный тест: генерируем плотный граф для 50 перекрёстков (для ускорения теста, а не 500) с случайными весами.
        # Здесь мы тестируем работоспособность алгоритма на более крупном входе.
        n = 50
        # Формируем f = 5 депо: на первых 5 перекрёстках.
        f = 5
        lines = []
        lines.append("1")
        lines.append("")
        lines.append(f"{f} {n}")
        for j in range(1, f + 1):
            lines.append(str(j))
        # Формируем цикл между всеми парами подряд, чтобы граф был связным
        for j in range(1, n):
            lines.append(f"{j} {j + 1} 1")
        # Замыкаем цикл
        lines.append(f"{n} 1 1")
        input_data = "\n".join(lines)
        # Просто проверяем, что функция отработает и выведет число от 1 до n
        result = solve_problem(input_data).strip()
        self.assertTrue(result.isdigit())
        self.assertTrue(1 <= int(result) <= n)

    def test_multiple_blocks(self):
        # Тест с несколькими блоками.
        input_data = """2

1 3
2
1 2 5
2 3 5
3 1 5

1 4
3
1 2 3
2 3 3
3 4 3
4 1 3
"""
        # Первый блок: депо на 2, второй блок: депо на 3.
        # Выбираем оптимальные кандидаты для каждого блока.
        output = solve_problem(input_data).split("\n\n")
        self.assertEqual(len(output), 2)
        # Проверяем, что результат для каждого блока является числом в нужном диапазоне
        self.assertTrue(1 <= int(output[0]) <= 3)
        self.assertTrue(1 <= int(output[1]) <= 4)
