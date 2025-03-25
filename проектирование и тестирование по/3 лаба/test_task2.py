import unittest
from main2 import max_land_pieces


class TestMaxLandPieces(unittest.TestCase):
    def test_known_values(self):
        test_cases = [
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 4),
            (4, 8),
            (5, 16),
            (6, 31),
            (2 ** 31 - 1, 886151993063477126682488902248300547)
        ]
        for n, expected in test_cases:
            with self.subTest(n=n):
                self.assertEqual(max_land_pieces(n), expected)


if __name__ == '__main__':
    unittest.main()
