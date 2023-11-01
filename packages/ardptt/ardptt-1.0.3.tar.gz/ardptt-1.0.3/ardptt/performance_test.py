# -*- coding: utf-8 -*-
import os
import signal
import time
import ardptt.data_analyse as data_analyse
import ardptt.generate_report as generate_report
import ardptt.data_tool as data_tool


# 自定义信号处理
def my_handler(signum, frame):
    global stop_flag
    stop_flag = True
    print("进程被kill，数据采集分析")
    try:
        # 测试完成，打开usb充电
        print('采集结束，打开充电模式')
        os.system("adb -s {0} shell dumpsys battery set usb 1".format(adb_id))
        os.system("adb -s {0} shell dumpsys battery set ac 1".format(adb_id))
    except Exception as stop_e:
        print(stop_e)

    x_val_int_list = list(range(1, len(memory_list) + 1))
    x_values = [str(i) for i in x_val_int_list]

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    report_dict = {"now_time": now_time,
                   "x_values": x_values,
                   "memory_list": memory_list,
                   "memory_ave": data_tool.get_ave_value(memory_list, 1),
                   "cpu_list": cpu_list,
                   "cpu_ave": data_tool.get_ave_value(cpu_list, 1),
                   "gpu_list": gpu_list,
                   "gpu_ave": data_tool.get_ave_value(gpu_list, 1),
                   "net_cost_list": net_cost_list,
                   "net_cost_ave": data_tool.get_ave_value(net_cost_list, 1),
                   "cpu_temp_list": cpu_temp_list,
                   "cpu_temp_ave": data_tool.get_ave_value(cpu_temp_list, 1),
                   "battery_temp_list": battery_temp_list,
                   "battery_temp_ave": data_tool.get_ave_value(battery_temp_list, 1),
                   "stutter_list": stutter_list,
                   "stutter_ave": data_tool.get_ave_value(stutter_list, 1),
                   "fps_list": fps_list,
                   "fps_ave": data_tool.get_ave_value(fps_list, 1),
                   "battery_cost_list": battery_cost_list,
                   "battery_cost_ave": data_tool.get_ave_value(battery_cost_list, 1),
                   }
    generate_report.generate_android_report(report_dict)


# 设置相应信号处理的handler
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)

stop_flag = False
adb_id = ""

memory_list = []
cpu_list = []
gpu_list = []
cpu_temp_list = []
battery_temp_list = []
net_cost_list = []
stutter_list = []
fps_list = []
battery_cost_list = []


def start(adb_device_id="", app_package_name="", interval=5):
    global adb_id
    adb_id = adb_device_id

    adb_state = os.popen("adb devices | grep {} | grep device".format(adb_device_id)).read().strip()
    print("adb_state:{}".format(adb_state))
    adb_on_flag = True
    if adb_state == "":
        adb_on_flag = False

    if adb_on_flag is False:
        print("设备掉线，请确保设备在线！")
        return

    if app_package_name == "":
        app_package_name = os.popen("adb -s {0} shell dumpsys window | grep mCurrentFocus | "
                                    "awk -F '/' '{{{1}}}' | awk '{{{2}}}'".format(adb_device_id,
                                                                                  'print $1',
                                                                                  'print $NF'
                                                                                  )).read().strip()
    print("current app_package_name : {}".format(app_package_name))

    # 关闭usb充电，避免电量/温度等信息采集不准确，采集完成后打开
    os.system("adb -s {0} shell dumpsys battery set usb 0".format(adb_device_id))
    os.system("adb -s {0} shell dumpsys battery set ac 0".format(adb_device_id))

    # 重置gfx信息
    os.system("adb -s {} shell dumpsys gfxinfo {} framestats reset".format(adb_device_id, app_package_name))

    # 重置电量信息
    os.system("adb -s {} shell dumpsys batterystats --reset".format(adb_device_id))

    # 获取app_id
    app_pid = int(os.popen("adb -s {0} shell ps | grep {1} | head -n 1 | awk '{{{2}}}'"
                           "".format(adb_device_id, app_package_name[0:13], 'print $2')).read().strip())
    print('app_id:{}'.format(app_pid))

    # 获取uid
    uid = os.popen("adb -s {0} shell ps | grep {1} | tail -n 1 | awk '{{{2}}}'".format(adb_device_id,
                                                                                       app_package_name,
                                                                                       'print $1'
                                                                                       )).read().strip()
    uid_origin = uid
    uid = uid.replace("_", "").strip()  # e.g. u0_a705 -> u0a705
    print('app_uid:{}'.format(uid))
    battery_cost_cmd = "adb -s {0} shell dumpsys batterystats | " \
                       "grep \"Uid {1}:\" | tail -n 1 | " \
                       "awk -F \"(\" '{{{2}}}' | " \
                       "awk -F \":\" '{{{3}}}'".format(adb_device_id,
                                                       uid,
                                                       'print $1',
                                                       'print $2'
                                                       )
    battery_cost_cmd_for_mi_13 = "adb -s {0} shell dumpsys batterystats | " \
                                 "grep \"UID {1}:\" | tail -n 1 | " \
                                 "awk -F \"fg:\" '{{{2}}}' | " \
                                 "awk -F \":\" '{{{3}}}'".format(adb_device_id,
                                                                 uid,
                                                                 'print $1',
                                                                 'print $2'
                                                                 )
    battery_cost_cmd_hw = "adb -s {0} shell dumpsys batterystats | " \
                          "grep \"UID {1}:\" | tail -n 1 | " \
                          "awk -F \"(\" '{{{2}}}' | " \
                          "awk -F \":\" '{{{3}}}'".format(adb_device_id,
                                                          uid,
                                                          'print $1',
                                                          'print $2'
                                                          )
    old_net_cost = data_analyse.get_net_cost_data(device_id=adb_device_id, app_pid=str(app_pid))
    old_battery_cost = 0
    start_scan_time = int(round(time.time() * 1000))  # 开始节点，当前毫秒数
    old_time = int(start_scan_time)  # 用于计算流量
    old_time_2 = old_time  # 用于计算耗电量

    print('start app performance test ...')
    index = 0
    while True:
        try:
            if stop_flag:
                break

            # 具体采集流程
            time.sleep(interval)  # 每隔X秒采集一次

            # 内存采集
            memory = os.popen("adb -s {0} shell dumpsys meminfo {1} | grep 'TOTAL SWAP PSS:' | head -n 1 | "
                              "awk -F 'TOTAL SWAP PSS:' '{{{2}}}' | "
                              "awk -F 'TOTAL:' '{{{3}}}'".format(adb_device_id,
                                                                 app_package_name,
                                                                 'print $1',
                                                                 'print $2')).read().strip()
            if memory == "":
                # 适配小米13新结构
                memory = os.popen("adb -s {0} shell dumpsys meminfo {1} | grep 'TOTAL SWAP PSS:' | head -n 1 | "
                                  "awk -F 'TOTAL RSS:' '{{{2}}}' | "
                                  "awk -F 'TOTAL PSS:' '{{{3}}}'".format(adb_device_id,
                                                                         app_package_name,
                                                                         'print $1',
                                                                         'print $2')).read().strip()

            memory = int(memory) if memory != "" else 0
            print('memory data: {}'.format(memory))
            memory_list.append(int(memory/1024))

            # CPU采集
            cpu = data_analyse.get_cpu_data(device_id=adb_device_id, uid=uid_origin)
            print('cpu data: {}'.format(cpu))
            cpu_list.append(cpu)

            # GPU采集
            try:
                gpu_info = os.popen("adb -s {0} shell "
                                    "cat /sys/class/kgsl/kgsl-3d0/gpubusy".format(adb_device_id)).read().strip()
                gpu_used = int(gpu_info.split(" ")[0].strip()) if gpu_info != "" else 0
                gpu_total = int(gpu_info.split(" ")[1].strip()) if gpu_info != "" else 0
                gpu = round(float(gpu_used / gpu_total) * 100, 2) if gpu_total != 0 else 0
                print('gpu data: {}'.format(gpu))
                gpu_list.append(gpu)
            except Exception as gpu_e:
                print(gpu_e)
                print("GPU信息采集失败")
                gpu_list.append(0)

            # cpu温度采集
            cpu_temp = os.popen("adb -s {0} shell "
                                "cat /sys/class/thermal/thermal_zone0/temp".format(adb_device_id)).read().strip()
            cpu_temp = round(float(cpu_temp) / 1000, 2) if cpu_temp != "" else 0
            print('cpu temperature data: {}'.format(cpu_temp))
            cpu_temp_list.append(cpu_temp)

            # 电池温度采集
            battery_temp = os.popen("adb -s {0} shell dumpsys battery | grep temperature | "
                                    "awk -F \":\" '{{{1}}}'".format(adb_device_id, 'print $2')).read().strip()
            battery_temp = round(float(battery_temp) / 10, 2) if battery_temp != "" else 0
            print('battery temperature data: {}'.format(battery_temp))
            battery_temp_list.append(battery_temp)

            # 卡顿率/帧率采集
            total_frames = 0
            janky_frames = 0
            loss_rate = 0
            for line in os.popen("adb -s {0} shell dumpsys gfxinfo {1} framestats | grep "
                                 "'Janky frames\\|Total frames rendered'".format(adb_device_id, app_package_name)):
                print(line)
                if line.startswith("Total frames rendered:"):
                    total_frames = int(line.replace("Total frames rendered:", "").strip())
                elif line.startswith("Janky frames:"):
                    janky_frames = int(line.replace("Janky frames:", "").split('(')[0])
                    loss_rate = round(float(line.split('(')[1].split('%)')[0]), 2)
            stutter_list.append(loss_rate)
            fps = round(float(total_frames * 60 / (total_frames + janky_frames)), 2) if total_frames != 0 else 0
            fps_list.append(fps)
            print('stutter data: {}'.format(loss_rate))
            print('fps data: {}'.format(fps))

            # 重置gfx
            os.system("adb -s {} shell dumpsys gfxinfo {} framestats reset".format(adb_device_id, app_package_name))

            # 流量采集
            current_time = int(round(time.time() * 1000))
            time_cost_this_step = round(float(current_time - old_time) / 1000, 2)
            current_net_cost = data_analyse.get_net_cost_data(device_id=adb_device_id, app_pid=str(app_pid))
            net_cost_this_step = current_net_cost - old_net_cost
            print('before_get net_cost data: {}'.format(old_net_cost))
            print('current net_cost data: {}'.format(current_net_cost))
            print('this step net_cost data: {}'.format(net_cost_this_step))
            print('this step time_cost data: {}'.format(time_cost_this_step))
            net_cost = round(float(net_cost_this_step / time_cost_this_step), 2)
            net_cost_list.append(net_cost)
            old_time = current_time
            old_net_cost = current_net_cost

            # 耗电量采集
            battery_cost_current = os.popen(battery_cost_cmd).read().strip()
            if battery_cost_current == "" or battery_cost_current.__contains__("("):
                battery_cost_current = os.popen(battery_cost_cmd_for_mi_13).read().strip()
            if battery_cost_current == "" or battery_cost_current.__contains__("("):
                battery_cost_current = os.popen(battery_cost_cmd_hw).read().strip()
            battery_cost_current = round(float(battery_cost_current), 2) if battery_cost_current != "" else 0
            print('battery_cost current: {}'.format(battery_cost_current))
            current_time_2 = int(round(time.time() * 1000))
            time_cost_this_step_2 = round(float(current_time_2 - old_time_2) / 1000, 2)

            battery_cost = battery_cost_current - old_battery_cost
            print('battery_cost data: {}'.format(battery_cost))
            minutes = round(float(time_cost_this_step_2 / 60), 5)
            print('battery_cost seconds data: {}'.format(time_cost_this_step_2))
            print('battery_cost minutes data: {}'.format(minutes))
            battery_cost_per_minutes = round(float(battery_cost / minutes), 2)  # 单位mAh/min
            print('battery_cost_per_minutes data: {}'.format(battery_cost_per_minutes))
            battery_cost_list.append(battery_cost_per_minutes)
            old_time_2 = current_time_2
            old_battery_cost = battery_cost_current

            index = index + 1

        except Exception as e:
            print(str(e))
            break
