import unittest
from io import StringIO
import sys

from main import solve


class TestSolution(unittest.TestCase):
    def test_single_person(self):
        input_data = "1\n1 1 1\n"
        expected = "1\n"
        self.run_test(input_data, expected)

    def test_example1(self):
        input_data = "3\n10 4 4\n11 3 1\n3 1 2\n"
        expected = "90720\n1026576\n1\n"
        self.run_test(input_data, expected)

    def test_case2(self):
        input_data = "1\n2 2 1\n"
        expected = "1\n"
        self.run_test(input_data, expected)

    def test_edge_case_zero(self):
        input_data = "1\n5 0 3\n"
        expected = "0\n"
        self.run_test(input_data, expected)

    def test_edge_case_max(self):
        input_data = "1\n13 13 1\n"
        expected = "1\n"
        self.run_test(input_data, expected)

    def test_edge_case_invalid(self):
        input_data = "1\n5 3 3\n"
        expected = "6\n"
        self.run_test(input_data, expected)

    def test_load_max_n(self):
        input_data = "1\n13 7 7\n"
        expected = "924\n"
        self.run_test(input_data, expected)

    def test_random_case(self):
        input_data = "1\n8 4 3\n"
        expected = "1750\n"
        self.run_test(input_data, expected)

    def run_test(self, input_data, expected):
        original_stdin = sys.stdin
        sys.stdin = StringIO(input_data)
        sys.stdout = StringIO()
        solve()
        output = sys.stdout.getvalue()
        sys.stdin = original_stdin
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
