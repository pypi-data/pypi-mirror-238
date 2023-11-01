# -*- coding: utf-8 -*-


def get_ave_value(data_list: list, data_type=0):
    result = 0
    total_val = 0
    len_list = len(data_list)
    if len_list == 0:
        return 0

    for i in range(len_list):
        total_val = total_val + data_list[i]

    if data_type == 0:
        result = int(total_val/len_list)
    elif data_type == 1:
        result = round(float(total_val/len_list), 2)  # 保留两位小数
    return result
