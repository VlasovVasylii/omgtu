import unittest
from main import determine_winner


class TestStanOllieGame(unittest.TestCase):
    def test_small_values(self):
        self.assertEqual(determine_winner(2), "Stan wins")
        self.assertEqual(determine_winner(10), "Ollie wins")
        self.assertEqual(determine_winner(17), "Ollie wins")

    def test_medium_values(self):
        self.assertEqual(determine_winner(162), "Stan wins")
        self.assertEqual(determine_winner(1000), "Stan wins")
        self.assertEqual(determine_winner(5000), "Ollie wins")

    def test_large_values(self):
        self.assertEqual(determine_winner(34012226), "Stan wins")
        self.assertEqual(determine_winner(1000000000), "Stan wins")
        self.assertEqual(determine_winner(4294967294), "Stan wins")

    def test_edge_cases(self):
        self.assertEqual(determine_winner(3), "Stan wins")
        self.assertEqual(determine_winner(9), "Stan wins")
        self.assertEqual(determine_winner(18), "Ollie wins")

    def test_stress_cases(self):
        self.assertEqual(determine_winner(2147483647), "Stan wins")
        self.assertEqual(determine_winner(4294967295), "Stan wins")
        self.assertEqual(determine_winner(999999999), "Stan wins")


if __name__ == "__main__":
    unittest.main()
