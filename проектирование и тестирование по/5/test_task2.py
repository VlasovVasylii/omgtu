import unittest
import random
from io import StringIO
import sys
from main2 import main


class TestFireDepot(unittest.TestCase):
    def run_test(self, input_data, expected_output):
        sys.stdin = StringIO(input_data)
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, expected_output.strip())

    def test_example(self):
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
        expected_output = "5"
        self.run_test(input_data, expected_output)

    def test_edge_case_single_depot(self):
        input_data = """1

1 1
1
"""
        expected_output = "1"
        self.run_test(input_data, expected_output)

    def test_edge_case_all_depots(self):
        input_data = """1

3 3
1
2
3
1 2 1
2 3 1
3 1 1
"""
        expected_output = "1"
        self.run_test(input_data, expected_output)

    def test_large_case(self):
        # Generate large test case with f=90, i=480
        input_data = ["1", "", "90 480"]

        # Generate 90 random depots
        depots = random.sample(range(1, 481), 90)
        input_data.extend(map(str, depots))

        # Generate a connected graph
        # First create a spanning tree to ensure connectivity
        edges = set()
        for u in range(2, 481):
            v = random.randint(1, u - 1)
            w = random.randint(1, 100)
            edges.add((u, v, w))

        # Add additional random edges (about 20 per node)
        for u in range(1, 481):
            for _ in range(20):
                v = random.randint(1, 480)
                if v != u:
                    w = random.randint(1, 100)
                    edges.add((u, v, w))

        # Add edges to input
        for u, v, w in edges:
            input_data.append(f"{u} {v} {w}")

        # Join input lines
        input_data = "\n".join(map(str, input_data))

        # Expected output is unknown, but we just want to verify it runs
        # without errors and produces some output
        sys.stdin = StringIO(input_data)
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue().strip()
        self.assertTrue(output.isdigit() and 1 <= int(output) <= 480)


if __name__ == '__main__':
    unittest.main()
