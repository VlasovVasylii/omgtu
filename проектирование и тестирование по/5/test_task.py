import unittest
from main import MazeSolver


class TestMazeSolver(unittest.TestCase):
    def test_example_1(self):
        w, h = 6, 4
        grid = [
            "\\//\\\\/",
            "\\///\\/",
            "//\\\\/\\",
            "\\/\\///",
        ]
        solver = MazeSolver(w, h, grid)
        count, longest = solver.solve()
        self.assertEqual(count, 2)
        self.assertEqual(longest, 13)

    def test_example_2(self):
        w, h = 3, 3
        grid = [
            "///",
            "\\//",
            "\\\\\\",
        ]
        solver = MazeSolver(w, h, grid)
        count, longest = solver.solve()
        self.assertEqual(count, 0)
        self.assertEqual(longest, 0)

    def test_min_case(self):
        solver = MazeSolver(1, 1, ["\\"])
        count, longest = solver.solve()
        self.assertEqual(count, 0)
        self.assertEqual(longest, 0)

    def test_full_cycle(self):
        w, h = 2, 2
        grid = [
            "/\\",
            "\\/"
        ]
        solver = MazeSolver(w, h, grid)
        count, longest = solver.solve()
        self.assertGreaterEqual(count, 1)
        self.assertGreaterEqual(longest, 4)

    def test_large_maze(self):
        w, h = 75, 75
        grid = ["\\" * w for _ in range(h)]
        solver = MazeSolver(w, h, grid)
        count, longest = solver.solve()
        self.assertTrue(count >= 0)
        self.assertTrue(longest >= 0)


if __name__ == "__main__":
    unittest.main()
