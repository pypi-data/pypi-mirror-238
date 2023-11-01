import re
from typing import Tuple, Union, Optional, Dict

from cn2an import cn2an, an2cn
from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import handle_number_sign, handle_blur_map, handle_zero_float_to_int


default_unit = default_conf["std_unit_check_dict"]["weight"][0]
cn_num_unit_list = default_conf["cn_num_unit_list"]
an_num_list = default_conf["an_num_list"]
cn_num_list = default_conf["cn_num_list"]


def trans_weight(text: str, unit: Optional[str] = default_unit, blur_map: Optional[Dict] = None) \
        -> Tuple[Union[int, float], str]:
    """
    体重数据转化

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

    # 八十 八十斤 八十公斤 八十克 八十千克 八十八斤 八十八公斤 八十八克 八十八千克 八十八g 八十八kg
    result = re.search(f"^[{cn_num_unit_list}]+(斤|公斤|克|千克|g|kg)?$", text)
    if result:
        if text[-2:] in ["公斤", "千克", "kg"]:
            num_text = text[:-2]
            cur_unit = "kg"
        elif text[-1] in ["克", "g"]:
            num_text = text[:-1]
            cur_unit = "g"
        elif text[-1] == "斤":
            num_text = text[:-1]
            cur_unit = "jin"
        else:
            num_text = text
            cur_unit = unit

        num = cn2an(num_text, "normal")
    else:
        # 8 80 180 8斤 8公斤 8克 8千克 80斤 80公斤 80克 80千克 80g 80kg
        result = re.search(f"^[{an_num_list}]+(斤|公斤|克|千克|g|kg)?$", text)
        if result:
            if text[-2:] in ["公斤", "千克", "kg"]:
                num_text = text[:-2]
                cur_unit = "kg"
            elif text[-1] in ["克", "g"]:
                num_text = text[:-1]
                cur_unit = "g"
            elif text[-1] == "斤":
                num_text = text[:-1]
                cur_unit = "jin"
            else:
                num_text = text
                cur_unit = unit

            if "." in num_text:
                num = float(num_text)
            else:
                num = int(num_text)
        else:
            # 一斤八 一斤8 1斤八 1斤8
            result = re.search(f"^[{cn_num_list}{an_num_list}]斤[{cn_num_list}{an_num_list}]$", text)
            if result:
                num_text_hundred, num_text_other = text.split("斤")
                # 处理斤位
                if num_text_hundred in cn_num_list:
                    num = cn2an(num_text_hundred, "normal") * 500
                else:
                    num = int(num_text_hundred) * 500
                # 处理两位
                if num_text_other in cn_num_list:
                    num = num + cn2an(num_text_other, "normal") * 50
                else:
                    num = num + int(num_text_other) * 50

                cur_unit = "g"
            else:
                # 80多 80多斤 80多公斤 80多克 80多千克 80多g 80多kg 80几...
                result = re.search(f"^[{an_num_list}]+[{cn_num_list}](斤|公斤|克|千克|g|kg)?$", text)
                if result:
                    if text[-2:] in ["公斤", "千克", "kg"]:
                        num_text = text[:-2]
                        cur_unit = "kg"
                    elif text[-1] in ["克", "g"]:
                        num_text = text[:-1]
                        cur_unit = "g"
                    elif text[-1] == "斤":
                        num_text = text[:-1]
                        cur_unit = "jin"
                    else:
                        num_text = text
                        cur_unit = unit

                    num_text = an2cn(num_text[:-1]) + num_text[-1]
                    num = cn2an(num_text)
                else:
                    raise Exception(f"！！trans_weight 暂时不能处理的文本格式：{text}")

    # 单位规范化
    # 处理 斤
    if cur_unit == "jin":
        num = num * 500
        cur_unit = "g"

    if unit == "g" and cur_unit == "kg":
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num * 1000, decimal_len - 3)
        else:
            num = num * 1000
    elif unit == "kg" and cur_unit == "g":
        # 处理 0.18 / 1000 = 0.00017999999999999998
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num / 1000, decimal_len + 3)
        else:
            num = num / 1000
    else:
        num = num

    if isinstance(num, float):
        num = handle_zero_float_to_int(num)

    return sign * num, unit
