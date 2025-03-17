import io
import sys
import unittest
from main2 import solve


class TestTollCalculation(unittest.TestCase):
    def run_test(self, input_data, expected_output):
        # Перенаправляем стандартный ввод/вывод
        sys.stdin = io.StringIO(input_data)
        sys.stdout = io.StringIO()

        # Запускаем решение
        solve()

        # Получаем результат
        actual_output = sys.stdout.getvalue().strip()

        # Сравниваем с ожидаемым результатом
        self.assertEqual(actual_output, expected_output.strip())

    def test_basic_case(self):
        input_data = """1

10 10 10 10 10 10 20 20 20 15 15 15 15 15 15 15 20 30 20 15 15 10 10 10
ABCD123 01:01:06:01 enter 17
765DEF 01:01:07:00 exit 95
ABCD123 01:01:08:03 exit 95
765DEF 01:01:05:59 enter 17"""
        expected_output = """765DEF $10.80
ABCD123 $18.60"""
        self.run_test(input_data, expected_output)

    def test_multiple_trips(self):
        input_data = """1

5 5 5 5 5 5 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 5 5 5
CAR1 01:01:00:00 enter 10
CAR1 01:01:01:00 exit 20
CAR2 01:01:12:00 enter 30
CAR2 01:01:13:30 exit 50"""
        expected_output = """CAR1 $6.00
CAR2 $22.00"""
        self.run_test(input_data, expected_output)

    def test_single_car(self):
        input_data = """1

2 2 2 2 2 2 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2 2 2
X123 01:01:02:00 enter 5
X123 01:01:02:30 exit 10"""
        expected_output = """X123 $3.00"""
        self.run_test(input_data, expected_output)

    def test_multiple_test_cases(self):
        input_data = """2

10 10 10 10 10 10 20 20 20 15 15 15 15 15 15 15 20 30 20 15 15 10 10 10
CAR1 01:01:06:01 enter 17
CAR1 01:01:08:03 exit 95

5 5 5 5 5 5 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 5 5 5
CAR2 01:01:00:00 enter 10
CAR2 01:01:01:00 exit 20"""
        expected_output = """CAR1 $18.60

CAR2 $6.00"""
        self.run_test(input_data, expected_output)


if __name__ == '__main__':
    unittest.main()