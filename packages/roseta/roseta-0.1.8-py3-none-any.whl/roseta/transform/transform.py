from typing import Tuple, Union, Optional, Dict

from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.log import get_logger
from roseta.util.data import handle_zero_float_to_int
from roseta.transform.no_class import trans_no_class
from roseta.transform.length import trans_length
from roseta.transform.weight import trans_weight
from roseta.transform.city import trans_city
from roseta.transform.age import trans_age
from roseta.transform.cup import trans_cup

logger = get_logger("roseta.transform", "debug")


def transform(text: str, cls: Optional[str] = None, unit: Optional[str] = None, blur_map: Optional[Dict] = None) \
        -> Tuple[Union[int, float, str], str]:
    """
    从非结构化数据到结构化的转化

    :param text: 待转化文本
    :param cls: 类别
    :param unit: 单位
    :param blur_map: 模糊映射
    :return: 文本, 单位
    """
    text = preprocess(text)

    if cls is None:
        for key, values in default_conf["cn_unit_check_dict"].items():
            for value in values:
                if value in text:
                    cls = key
                    logger.debug(f"「{text}」自动识别 cls 为 {cls}。")
                    break
        if cls is None:
            cls = "no"

    if unit is None:
        if cls == "no":
            unit = "no"
        else:
            unit = default_conf["std_unit_check_dict"][cls][0]
            logger.debug(f"「{text}」使用默认 unit 为 {unit}。")
    else:
        if cls != "no" and unit not in default_conf["std_unit_check_dict"][cls]:
            raise Exception(f"数据和单位不匹配：{text} | {unit}。")

    if cls == "no":
        text, unit = trans_no_class(text, unit, blur_map)
    elif cls == "length":
        text, unit = trans_length(text, unit, blur_map)
    elif cls == "weight":
        text, unit = trans_weight(text, unit, blur_map)
    elif cls == "city":
        text, unit = trans_city(text, unit)
    elif cls == "age":
        text, unit = trans_age(text, unit, blur_map)
    elif cls == "cup":
        text, unit = trans_cup(text, unit, blur_map)
    else:
        raise Exception(f"unknown class: {cls}")

    if isinstance(text, float):
        text = handle_zero_float_to_int(text)

    return text, unit
