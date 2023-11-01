import unittest

from roseta import trans_no_class


class TestNoClass(unittest.TestCase):
    def setUp(self) -> None:
        self.no_cls_data = {
            "零": (0, "no"),
            "零点八": (0.8, "no"),
            "八": (8, "no"),
            "八十": (80, "no"),
            "八十八": (88, "no"),
            "负八十八": (-88, "no")
        }

    def test_trans_no_class(self) -> None:
        for key, value in self.no_cls_data.items():
            self.assertEqual(trans_no_class(key, "no"), value)


if __name__ == '__main__':
    unittest.main()
