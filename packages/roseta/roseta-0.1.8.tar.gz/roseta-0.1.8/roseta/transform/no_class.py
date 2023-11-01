import re
from typing import Tuple, Union, Optional, Dict

from cn2an import cn2an, an2cn
from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import handle_number_sign, handle_blur_map


cn_num_unit_list = default_conf["cn_num_unit_list"]
an_num_list = default_conf["an_num_list"]
cn_num_list = default_conf["cn_num_list"]


# 零 零点八 八 八十 八十八 负八十八
def _func1(text):
    text = text[0]
    return cn2an(text, "normal")


# 0 0.8 8 80 88 -88
def _func2(text):
    text = text[0]
    if "." in text:
        num = float(text)
    else:
        num = int(text)
    return num


# 80多 80几
def _func3(text):
    text = text[0]
    num_text = an2cn(text[:-1]) + text[-1]
    return cn2an(num_text)


regex_match_list = [
    {
        "rule": re.compile(f"^[{cn_num_unit_list}]+$"),
        "method": _func1
    },
    {
        "rule": re.compile(f"^[{an_num_list}]+$"),
        "method": _func2
    },
    {
        "rule": re.compile(f"^[{an_num_list}]+[{cn_num_list}]$"),
        "method": _func3
    },
]


def trans_no_class(text: str, unit: Optional[str] = None, blur_map: Optional[Dict] = None)\
        -> Tuple[Union[int, float], str]:
    """
    无单位的数据转化

    :param text: 待转化文本
    :param unit: 单位
    :param blur_map: 模糊映射
    :return: 数字, 单位
    """
    if blur_map is None:
        blur_map = default_conf["blur_map"]

    text = preprocess(text)
    text = handle_blur_map(text, blur_map)
    text, sign = handle_number_sign(text)

    num = None
    for regex_item in regex_match_list:
        matched = regex_item["rule"].findall(text)
        if matched:
            num = regex_item["method"](matched)
            break

    if num is None:
        raise ValueError(f"！！trans_no_class 暂时不能处理的文本格式：{text}")

    return sign * num, unit
