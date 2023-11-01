# -*- coding: utf-8 -*-
import os


def get_cpu_data(device_id: str, uid: str) -> float:
    # 一般取$9,但是有一些特殊情况$9取出来的值为R,S,D, 这时候要取$10
    result = os.popen("adb -s {0} shell top -n 1 | grep {1} | head -n 1 | awk '{{{2}}}'".format(
        device_id, uid, 'print $9,$10')).read().strip()
    result_arr = result.split()
    try:
        if result_arr[0] in ['R', 'S', 'D']:
            result = float(result_arr[1])
        else:
            result = float(result_arr[0])
    except Exception as e:
        print(e)
        result = 0
    return result


def get_net_cost_data(device_id: str, app_pid: str) -> float:

    # wifi流量
    download_net_cost_wifi = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep -v swlan0 | grep wlan0 | awk "
                                      "'{{{2}}}'".format(device_id, app_pid, 'print $2')).read().strip()
    print('download_net_cost_wifi: {}'.format(download_net_cost_wifi))
    download_net_cost_wifi = int(download_net_cost_wifi) if download_net_cost_wifi != "" else 0
    upload_net_cost_wifi = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep -v swlan0 | grep wlan0 | awk "
                                    "'{{{2}}}'".format(device_id, app_pid, 'print $10')).read().strip()
    upload_net_cost_wifi = int(upload_net_cost_wifi) if upload_net_cost_wifi != "" else 0
    print('upload_net_cost_wifi: {}'.format(upload_net_cost_wifi))

    # 移动流量
    download_net_cost_card = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep -v r_rmnet_data0 | "
                                      "grep rmnet_data0 | "
                                      "awk '{{{2}}}'".format(device_id, app_pid, 'print $2')).read().strip()
    if download_net_cost_card == "":
        download_net_cost_card = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep rmnet0 | "
                                          "awk '{{{2}}}'".format(device_id, app_pid, 'print $2')).read().strip()
    print('download_net_cost_card: {}'.format(download_net_cost_card))
    download_net_cost_card = int(download_net_cost_card) if download_net_cost_card != "" else 0

    upload_net_cost_card = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep -v r_rmnet_data0 | "
                                    "grep rmnet_data0 | "
                                    "awk '{{{2}}}'".format(device_id, app_pid, 'print $10')).read().strip()
    if upload_net_cost_card == "":
        upload_net_cost_card = os.popen("adb -s {0} shell cat /proc/{1}/net/dev | grep rmnet0 | "
                                        "awk '{{{2}}}'".format(device_id, app_pid, 'print $10')).read().strip()
    print('upload_net_cost_card: {}'.format(upload_net_cost_card))
    upload_net_cost_card = int(upload_net_cost_card) if upload_net_cost_card != "" else 0

    net_total = download_net_cost_wifi + upload_net_cost_wifi + download_net_cost_card + upload_net_cost_card

    net_cost_data = round(float(net_total / 1000), 2)  # 保留两位小数, 单位KB

    return net_cost_data
