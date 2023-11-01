import re
from typing import Tuple, Optional, Dict, Union, List

from cn2an import cn2an
from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import get_city_pattern
from roseta.util.data import handle_blur_map, handle_zero_float_to_int


city_ptn, city_map = get_city_pattern()
default_unit = default_conf["std_unit_check_dict"]["cup"][0]

cup_map = {
    "a": 12,
    "b": 14,
    "c": 16,
    "d": 18,
    "e": 20,
    "f": 22,
    "g": 24,
    "h": 26,
}


def _func1(matched):
    n1, n2 = matched[0]
    if n1.isnumeric():
        lower_num = int(cn2an(n1, mode="smart"))
        cup = n2
    else:
        lower_num = int(cn2an(n2, mode="smart"))
        cup = n1

    # 美码 32A-48H
    if 32 <= lower_num <= 48:
        # 美码 转 欧码
        lower_num = int(lower_num * 2.5 - 10)
    # 欧码 65A-110H
    elif 65 <= lower_num <= 110:
        pass
    else:
        raise Exception(f"num 不在有效范围内 [32, 48] [65, 110]：{lower_num}")

    if cup in cup_map.keys():
        upper_num = lower_num + cup_map[cup]
    else:
        raise Exception(f"cup 不在有效范围内 {list(cup_map.keys())}：{cup}")
    return upper_num, lower_num


regex_match_list = [
    {
        # 美码 36C 三十六C 三六C 四十C
        "rule": re.compile(r"^([3三叁仨][十拾]?[2468二贰两四肆六陆八捌]|"
                           r"[4四肆][十拾]?[02468零二贰两四肆六陆八捌]|"
                           r"[4四肆][十拾])"
                           r"([a-hA-H])$"),
        "method": _func1
    },
    {
        # 美码 C36 C三十六 C三六 C四十
        "rule": re.compile(r"^([a-hA-H])"
                           r"([3三叁仨][十拾]?[2468二贰两四肆六陆八捌]|"
                           r"[4四肆][十拾]?[02468零二贰两四肆六陆八捌]|"
                           r"[4四肆][十拾])$"),
        "method": _func1
    },
    {
        # 欧码 85C 八十五C 八五C 八十C 一百零五C 一百一十C
        "rule": re.compile(r"^((?:[6-9六陆七柒八捌九玖]|[1一壹幺][百佰]?[01零一壹幺])[十拾]?[05零五伍]|"
                           r"[6-9六陆七柒八捌九玖][十拾]|"
                           r"[1一壹幺][百佰][01零一壹幺][十拾])"
                           r"([a-hA-H])$"),
        "method": _func1
    },
    {
        # 欧码 C85 C八十五 C八五 C八十 C一百零五 C一百一十
        "rule": re.compile(r"^([a-hA-H])"
                           r"((?:[6-9六陆七柒八捌九玖]|[1一壹幺][百佰]?[01零一壹幺])[十拾]?[05零五伍]|"
                           r"[6-9六陆七柒八捌九玖][十拾]|"
                           r"[1一壹幺][百佰][01零一壹幺][十拾])$"),
        "method": _func1
    }
]


def trans_cup(text: str, unit: Optional[str] = default_unit, blur_map: Optional[Dict] = None) \
        -> Tuple[List[Union[int, float]], str]:
    """
    罩杯数据转化

    :param text: 待转化文本
    :param unit: 单位
    :param blur_map: 模糊映射
    :return: 数字, 单位
    """
    if blur_map is None:
        blur_map = default_conf["blur_map"]

    text = preprocess(text)
    text = handle_blur_map(text, blur_map)

    temp_nums = []
    for regex_item in regex_match_list:
        matched = regex_item["rule"].findall(text)
        if matched:
            temp_nums = regex_item["method"](matched)
            break

    if len(temp_nums) == 0:
        raise Exception(f"！！trans_cup 暂时不能处理的文本格式：{text}")

    result = []
    for num in temp_nums:
        # 单位规范化
        if unit == "m":
            # 处理 0.018 / 100 = 0.00017999999999999998
            if type(num) == float:
                decimal_len = len(str(num).split(".")[1])
                num = round(num / 100, decimal_len + 2)
            else:
                num = num / 100

        if isinstance(num, float):
            num = handle_zero_float_to_int(num)

        result.append(num)

    return result, unit
