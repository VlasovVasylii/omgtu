import unittest

from main import restore_original


class TestRestoreOriginal(unittest.TestCase):
    def test_case_1(self):
        fragments = ["011", "0111", "01110", "111", "0111", "10111"]
        self.assertEqual(restore_original(fragments), "01110111")

    def test_case_2(self):
        fragments = []
        self.assertEqual(restore_original(fragments), "")


if __name__ == "__main__":
    unittest.main()
