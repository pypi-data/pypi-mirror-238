import unittest

from roseta import trans_age


class TestAge(unittest.TestCase):
    def setUp(self) -> None:
        self.age_data = {
            "一岁": [(1, "year"), (12, "month")],
            "二个月": [(0.2, "year"), (2, "month")],
            "18岁": [(18, "year"), (216, "month")],
            "一岁半": [(1.5, "year"), (18, "month")],
            "1岁8个月": [(1.7, "year"), (20, "month")],
            "一岁八个月": [(1.7, "year"), (20, "month")],
            "一周岁": [(1, "year"), (12, "month")],
            "两岁零3个月": [(2.2, "year"), (27, "month")],
            "7个月": [(0.6, "year"), (7, "month")],
            "9月": [(0.8, "year"), (9, "month")],
            "13个月": [(1.1, "year"), (13, "month")],
            "10个多月": [(0.8, "year"), (10.1, "month")],
            "2岁多": [(2.2, "year"), (26, "month")],
            "10個月": [(0.8, "year"), (10, "month")]
        }

    def test_trans_age(self) -> None:
        for key, value in self.age_data.items():
            self.assertEqual(trans_age(key),  value[0])  # default unit: year
            self.assertEqual(trans_age(key, unit="year"), value[0])
            self.assertEqual(trans_age(key, unit="month"), value[1])


if __name__ == '__main__':
    unittest.main()
