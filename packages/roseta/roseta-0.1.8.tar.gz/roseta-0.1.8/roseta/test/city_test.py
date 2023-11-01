import unittest

from roseta import trans_city


class TestCity(unittest.TestCase):
    def setUp(self) -> None:
        self.city_data = {
            # pattern1
            "杭州": [("杭州市", "市"), ("浙江省杭州市", "省")],
            "杭州市": [("杭州市", "市"), ("浙江省杭州市", "省")],
            "阿拉善": [("阿拉善盟", "市"), ("内蒙古自治区阿拉善盟", "省")],
            # pattern2
            "浙江省": [("浙江省", "市"), ("浙江省", "省")],
            "浙江": [("浙江省", "市"), ("浙江省", "省")],
            "天津": [("天津市", "市"), ("天津市", "省")],
            "天津市": [("天津市", "市"), ("天津市", "省")],
            "广西": [("广西壮族自治区", "市"), ("广西壮族自治区", "省")],
            "广西壮族自治区": [("广西壮族自治区", "市"), ("广西壮族自治区", "省")],
        }

    def test_trans_city(self) -> None:
        for key, value in self.city_data.items():
            self.assertEqual(trans_city(key), value[0])  # default unit: 市
            self.assertEqual(trans_city(key, unit="市"), value[0])
            self.assertEqual(trans_city(key, unit="省"), value[1])


if __name__ == '__main__':
    unittest.main()
