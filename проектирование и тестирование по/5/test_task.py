import unittest
import sys
from io import StringIO
from main import main


class TestMazeCycles(unittest.TestCase):
    def setUp(self):
        self.held_stdout = StringIO()
        self.held_stderr = StringIO()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        self.held_stdout.close()
        self.held_stderr.close()

    def run_test(self, input_data, expected_output):
        stdin = StringIO(input_data)
        sys.stdin = stdin
        main()
        sys.stdin = sys.__stdin__
        self.assertEqual(self.held_stdout.getvalue(), expected_output)

    def test_example(self):
        input_data = """6 4
\//\\/
\///\/
//\\/\
\/\///
3 3
///
\\//
\\\
0 0
"""
        expected_output = """Maze #1:
2 Cycles; the longest has length 16.

Maze #2:
There are no cycles.

"""
        self.run_test(input_data, expected_output)

    def test_no_cycles(self):
        input_data = """1 1
/
0 0
"""
        expected_output = """Maze #1:
There are no cycles.

"""
        self.run_test(input_data, expected_output)

    def test_single_cycle(self):
        input_data = """2 2
\\\\
\\\\
0 0
"""
        expected_output = """Maze #1:
1 Cycles; the longest has length 4.

"""
        self.run_test(input_data, expected_output)

    def test_large_input(self):
        input_data = "100 100\n" + "\n".join(
            ["".join(["\\" if (i + j) % 2 == 0 else "/" for i in range(100)]) for j in range(100)]) + "\n0 0"
        expected_output = "Maze #1:\nThere are no cycles.\n\n"
        self.run_test(input_data, expected_output)


if __name__ == '__main__':
    unittest.main()
