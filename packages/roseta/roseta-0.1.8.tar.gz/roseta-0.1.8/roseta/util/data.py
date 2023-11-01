from typing import Tuple, Dict, Set, Union, Any
from re import compile
from collections import defaultdict

from roseta.util.conf import province_city_conf


def get_all_cities() -> Set:
    cities = set()
    for province, p_value in province_city_conf.items():
        cities.add(province)
        for city in p_value:
            cities.add(f"{province}/{city}")
    return cities


def get_city_pattern() -> Tuple[Any, Dict]:
    cities_dict = defaultdict(list)
    convert_map = {}
    for line in get_all_cities():
        if "/" in line:
            province, city = line.split("/")
            if city[-3:] == "自治县":
                item = city
                cities_dict["静态"].append(item)
            elif city[-1] in ["县", "市", "盟"]:
                item, unit = city[:-1], city[-1]
                cities_dict[unit].append(item)
            elif city[-2:] in ["林区", "地区"]:
                item, unit = city[:-2], city[-2:]
                cities_dict[unit].append(item)
            else:
                item = city
                cities_dict["静态"].append(item)

            convert_map[item] = {
                "省": line.replace("/", ""),
                "市": city
            }

            if city not in convert_map.keys():
                convert_map[city] = {
                    "省": line.replace("/", ""),
                    "市": city
                }
        else:
            province = line
            if province[-1] in ["省", "市"]:
                item, unit = province[:-1], province[-1]
                cities_dict[unit].append(item)
            elif province[-3:] in ["自治区"]:
                if province[-4] == "族":
                    item, unit = province[:-5], province[-5:]
                else:
                    item, unit = province[:-3], province[-3:]
                cities_dict[unit].append(item)
            elif province[-5:] in ["特别行政区"]:
                item, unit = province[:-5], province[-5:]
                cities_dict[unit].append(item)
            else:
                raise Exception(province)

            convert_map[item] = {
                "省": province,
                "市": province
            }
            if province not in convert_map.keys():
                convert_map[province] = {
                    "省": province,
                    "市": province
                }

    ptn_list = []
    for unit, city_list in cities_dict.items():
        p_city = "|".join(city_list)
        if unit != "静态":
            ptn_list.append(f"({p_city})({unit})?")
        else:
            ptn_list.append(f"({p_city})")
    ptn_str = "|".join(ptn_list)
    return compile(f"^({ptn_str})"), convert_map


def handle_number_sign(text: str) -> Tuple[str, int]:
    # 确定正负号
    if text[0] in ["负", "-"]:
        text = text[1:]
        sign = -1
    else:
        sign = 1
    return text, sign


def handle_blur_map(text: str, blur_map: Dict) -> str:
    # 处理模糊表示「几、多」
    for k, v in blur_map.items():
        if k in text:
            text = text.replace(k, v)
    return text


def handle_zero_float_to_int(text: Union[float]) -> Union[float, int]:
    # 80.0 to 80
    if text == int(text):
        text = int(text)
    return text
