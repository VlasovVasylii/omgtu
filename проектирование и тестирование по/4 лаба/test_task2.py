import unittest
from io import StringIO
import sys
from main2 import main


class TestElephants(unittest.TestCase):
    def run_program(self, input_data):
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO(input_data)
        sys.stdout = StringIO()
        try:
            main()
            output = sys.stdout.getvalue().strip().split('\n')
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
        return output

    def test_example(self):
        input_data = """6008 1300
6000 2100
500 2000
1000 4000
1100 3000
6000 2000
8000 1400
6000 1200
2000 1900"""
        output = self.run_program(input_data)
        self.assertEqual(output[0], '4')
        self.assertEqual(output[1], '4')
        self.assertEqual(output[2], '5')
        self.assertEqual(output[3], '9')
        self.assertEqual(output[4], '7')

    def test_single_elephant(self):
        input_data = "1000 2000"
        output = self.run_program(input_data)
        self.assertEqual(output[0], '1')
        self.assertEqual(output[1], '1')

    def test_two_elephants_valid(self):
        input_data = "100 200\n200 100"
        output = self.run_program(input_data)
        self.assertEqual(output[0], '2')
        self.assertEqual(output[1], '1')
        self.assertEqual(output[2], '2')

    def test_two_elephants_invalid(self):
        input_data = "100 100\n200 200"
        output = self.run_program(input_data)
        self.assertEqual(output[0], '1')

    def test_three_elephants(self):
        input_data = "100 300\n200 200\n300 100"
        output = self.run_program(input_data)
        self.assertEqual(output[0], '3')

    def test_same_weight_different_iq(self):
        input_data = "100 300\n100 200\n200 250\n200 150"
        output = self.run_program(input_data)
        self.assertEqual(output[0], '2')

    def test_load_test(self):
        input_data = '\n'.join(f"{i} {10000 - i}" for i in range(1, 1001))
        output = self.run_program(input_data)
        self.assertEqual(output[0], '1000')
        self.assertEqual(len(output[1:]), 1000)


if __name__ == '__main__':
    unittest.main()
