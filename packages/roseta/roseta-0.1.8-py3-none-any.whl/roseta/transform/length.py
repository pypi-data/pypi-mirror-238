import re
from typing import Tuple, Union, Optional, Dict

from cn2an import cn2an, an2cn
from proces import preprocess

from roseta.util.conf import default_conf
from roseta.util.data import handle_number_sign, handle_blur_map, handle_zero_float_to_int

default_unit = default_conf["std_unit_check_dict"]["length"][0]
cn_num_unit_list = default_conf["cn_num_unit_list"]
an_num_list = default_conf["an_num_list"]
cn_num_list = default_conf["cn_num_list"]
all_num = an_num_list + cn_num_list


def trans_length(text: str, unit: Optional[str] = default_unit, blur_map: Optional[Dict] = None) \
        -> Tuple[Union[int, float], str]:
    """
    长度数据转化

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

    # 二尺 两尺 一尺八
    result = re.findall(f"^([{all_num}]" + "{1,3})" + f"尺([{all_num}]"+"{0,2})寸?$", text)
    if result:
        cur_unit = "cm"
        n1, n2 = result[0]
        n1 = cn2an(n1, mode="smart")
        if len(n2) > 0:
            n2 = cn2an(n2, mode="smart")
            chi = float(n1) + float(n2) * (10 ** (-1*len(str(int(n2)))))
        else:
            chi = float(n1)

        num = round(chi*33.3333, 2)
    else:
        # 八 八十 八十七 八厘米 八十厘米 八十七厘米 八米 八十米 八十七米
        result = re.search(f"^[{cn_num_unit_list}]+(厘米|米|cm|m)?$", text)
        if result:
            if text[-2:] in ["厘米", "cm"]:
                num_text = text[:-2]
                cur_unit = "cm"
            elif text[-1] in ["米", "m"]:
                num_text = text[:-1]
                cur_unit = "m"
            else:
                num_text = text
                cur_unit = unit

            num = cn2an(num_text, "normal")
        else:
            # 8 80 180 8厘米 80厘米 180厘米 8米 80米 180米
            result = re.search(f"^[{an_num_list}]+(厘米|米|cm|m)?$", text)
            if result:
                if text[-2:] in ["厘米", "cm"]:
                    num_text = text[:-2]
                    cur_unit = "cm"
                elif text[-1] in ["米", "m"]:
                    num_text = text[:-1]
                    cur_unit = "m"
                else:
                    num_text = text
                    cur_unit = unit

                if "." in num_text:
                    num = float(num_text)
                else:
                    num = int(num_text)
            else:
                # 一米八 一米八七 一米8 一米87 1米八 1米八七 1米8 1米87
                result = re.search(f"^[{cn_num_list}{an_num_list}]米[{cn_num_list}{an_num_list}]" + "{1,2}$", text)
                if result:
                    num_text_hundred, num_text_other = text.split("米")
                    # 处理百位
                    if num_text_hundred in cn_num_list:
                        num = cn2an(num_text_hundred, "normal") * 100
                    else:
                        num = int(num_text_hundred) * 100
                    # 处理十位个位
                    if num_text_other[-1] in cn_num_list:
                        if len(num_text_other) == 2:
                            num = num + cn2an(num_text_other, "normal")
                        else:
                            num = num + cn2an(num_text_other, "normal") * 10
                    else:
                        if len(num_text_other) == 2:
                            num = num + int(num_text_other)
                        else:
                            num = num + int(num_text_other) * 10
                    cur_unit = "cm"
                else:
                    # 80多 80多米 80多厘米 80几 80几米 80几厘米
                    result = re.search(f"^[{an_num_list}]+[{cn_num_list}](厘米|米|cm|m)?$", text)
                    if result:
                        if text[-2:] in ["厘米", "cm"]:
                            num_text = text[:-2]
                            cur_unit = "cm"
                        elif text[-1] in ["米", "m"]:
                            num_text = text[:-1]
                            cur_unit = "m"
                        else:
                            num_text = text
                            cur_unit = unit

                        num = cn2an(an2cn(num_text[:-1]) + num_text[-1])
                    else:
                        raise Exception(f"！！trans_length 暂时不能处理的文本格式：{text}")

    # 单位规范化
    if unit == "cm" and cur_unit == "m":
        # 处理 1.11 * 100 =  111.00000000000001
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num * 100, decimal_len - 2)
        else:
            num = num * 100
    elif unit == "m" and cur_unit == "cm":
        # 处理 0.018 / 100 = 0.00017999999999999998
        if type(num) == float:
            decimal_len = len(str(num).split(".")[1])
            num = round(num / 100, decimal_len + 2)
        else:
            num = num / 100
    else:
        num = num

    if isinstance(num, float):
        num = handle_zero_float_to_int(num)

    return sign * num, unit
