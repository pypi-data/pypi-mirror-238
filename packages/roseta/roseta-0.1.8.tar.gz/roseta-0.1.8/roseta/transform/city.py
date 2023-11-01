from typing import Tuple, Optional

from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import get_city_pattern


default_unit = default_conf["std_unit_check_dict"]["city"][0]
city_ptn, city_map = get_city_pattern()


def trans_city(text: str, unit: Optional[str] = default_unit) -> Tuple[str, str]:
    """
    城市数据转化

    :param text: 待转化文本
    :param unit: 单位
    :return: 文本, 单位
    """
    text = preprocess(text)

    result = city_ptn.search(text)
    if result:
        text = city_map[text][unit]
    else:
        raise Exception(f"！！trans_city 暂时不能处理的文本格式：{text}")

    return text, unit
