import unittest
from main2 import process_block


class TestTollBilling(unittest.TestCase):
    def test_case_1(self):
        fees = [10] * 6 + [20] * 3 + [15] * 9 + [20, 30, 20, 15, 15, 10, 10, 10]
        records = [
            "ABCD123 01:01:06:01 enter 17",
            "765DEF 01:01:07:00 exit 95",
            "ABCD123 01:01:08:03 exit 95",
            "765DEF 01:01:05:59 enter 17"
        ]
        expected_output = [("765DEF", 10.80), ("ABCD123", 18.60)]
        self.assertEqual(process_block(fees, records), expected_output)

    def test_no_trips(self):
        fees = [10] * 24
        records = ["ABCD123 01:01:06:01 enter 17"]  # No exit record
        expected_output = []
        self.assertEqual(process_block(fees, records), expected_output)

    def test_multiple_trips(self):
        fees = [10] * 24
        records = [
            "XYZ789 01:01:06:01 enter 10",
            "XYZ789 01:01:08:03 exit 20",
            "XYZ789 01:01:10:10 enter 30",
            "XYZ789 01:01:12:20 exit 50"
        ]
        expected_output = [
            ("XYZ789", round(1 + (10 * 10 / 100) + 1 + (20 * 10 / 100) + 2, 2))]  # Two trips + $2 bill fee
        self.assertEqual(process_block(fees, records), expected_output)


if __name__ == '__main__':
    unittest.main()
