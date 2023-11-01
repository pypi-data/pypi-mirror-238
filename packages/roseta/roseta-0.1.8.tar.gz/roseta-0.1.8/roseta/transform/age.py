import re
from typing import Tuple, Optional, Dict, Union

from cn2an import cn2an
from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import get_city_pattern
from roseta.util.data import handle_blur_map, handle_zero_float_to_int


city_ptn, city_map = get_city_pattern()
default_unit = default_conf["std_unit_check_dict"]["age"][0]
an_num_list = default_conf["an_num_list"]
cn_num_list = default_conf["cn_num_list"]
all_num = an_num_list + cn_num_list

# 单位转化
up_unit_map = {
    "year2month": 12,
    "year2week": 52.1,
    "year2day": 365,
    "month2week": 4.3,
    "month2day": 30,
    "week2day": 7
}


# 1岁多 1岁8个月
def _func1(matched):
    n1, n2 = matched[0]
    n1 = cn2an(n1, mode="smart")
    if len(n2) > 0:
        n2 = cn2an(n2, mode="smart")
        num = int(n1) * up_unit_map["year2month"] + float(n2)
    else:
        num = int(n1) * up_unit_map["year2month"]
    return num


# 2岁半 三岁半
def _func2(matched):
    n1 = matched[0]
    n1 = cn2an(n1, mode="smart")
    num = int(n1) * up_unit_map["year2month"] + 6
    return num


# 2个月 5月 10个多月
def _func3(matched):
    n1, n2 = matched[0]
    n1 = cn2an(n1, mode="smart")
    if len(n2) > 0:
        n2 = cn2an(n2, mode="smart")
        num = int(n1) + round(float(n2) / up_unit_map["month2day"], 1)
    else:
        num = int(n1)
    return num


regex_match_list = [
    {
        "rule": re.compile(f"^([{all_num}]" + "{1,3})" + f"周?岁([{all_num}]"+"{0,2})个?月?$"),
        "method": _func1
    },
    {
        "rule": re.compile(f"^([{all_num}]" + "{1,3})" + f"周?岁半$"),
        "method": _func2
    },
    {
        "rule": re.compile(f"^([{all_num}]" + "{1,2})" + f"个?([{all_num}]?)月$"),
        "method": _func3
    },
]


def trans_age(text: str, unit: Optional[str] = default_unit, blur_map: Optional[Dict] = None) \
        -> Tuple[Union[int, float], str]:
    """
    年龄数据转化

    :param text: 待转化文本
    :param unit: 单位
    :param blur_map: 模糊映射
    :return: 数字, 单位
    """
    if blur_map is None:
        blur_map = default_conf["blur_map"]

    text = preprocess(text)
    text = handle_blur_map(text, blur_map)

    num = None
    for regex_item in regex_match_list:
        matched = regex_item["rule"].findall(text)
        if matched:
            num = regex_item["method"](matched)
            break

    if num is None:
        raise Exception(f"！！trans_age 暂时不能处理的文本格式：{text}")

    if unit == "year":
        num = round(num/up_unit_map["year2month"], 1)

    if isinstance(num, float):
        num = handle_zero_float_to_int(num)

    return num, unit
