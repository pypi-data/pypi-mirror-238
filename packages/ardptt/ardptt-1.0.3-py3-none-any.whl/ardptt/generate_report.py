# -*- coding: utf-8 -*-
from pyecharts.charts import Line, Page
import pyecharts.options as opts


# 定义一个Line_charts函数
def line_charts_test(x, y1, y2) -> Line:
    c = Line()
    c.add_xaxis(xaxis_data=x)
    c.add_yaxis(series_name='1', y_axis=y1)
    c.add_yaxis(series_name='2', y_axis=y2)
    return c


# 定义一个Line_charts函数
def line_arr_charts(x, y_arr, name) -> Line:
    c = Line().set_global_opts(title_opts=opts.TitleOpts(title=name))
    c.add_xaxis(xaxis_data=x)
    for tmp in y_arr:
        c.add_yaxis(series_name='', y_axis=tmp)
    return c


# 定义一个Line_charts函数
def line_charts(x, y, name) -> Line:
    c = Line().set_global_opts(title_opts=opts.TitleOpts(title=name))
    c.add_xaxis(xaxis_data=x)
    c.add_yaxis(series_name='', y_axis=y)
    return c


def generate_android_report_test(params: dict):
    # 绘制散点数据
    x = ['seaborn', 'matplotlib', 'plotly', 'pyecharts', 'python']
    y1 = [440, 550, 770, 467, 800]
    y2 = [570, 430, 567, 450, 670]
    # 绘制图表
    c = line_charts(x, y1, y2)
    c2 = line_charts(x, y1, y2)

    page = Page(layout=Page.DraggablePageLayout)
    page.add(c, c2)
    page.render("second_line.html")


def generate_android_report(params: dict):
    page = Page(layout=Page.DraggablePageLayout)
    x = params['x_values']

    memory_list = params.get('memory_list', [])
    if len(memory_list) > 0:
        y = memory_list
        memory_page = line_charts(x, y, '内存占用情况 (平均值：{} MB)'.format(params.get('memory_ave')))
        page.add(memory_page)

    cpu_list = params.get('cpu_list', [])
    if len(cpu_list) > 0:
        y = cpu_list
        cpu_page = line_charts(x, y, 'CPU占用情况 (平均值：{} %)'.format(params.get('cpu_ave')))
        page.add(cpu_page)

    gpu_list = params.get('gpu_list', [])
    if len(gpu_list) > 0:
        y = gpu_list
        gpu_page = line_charts(x, y, 'GPU占用情况 (平均值：{} %)'.format(params.get('gpu_ave')))
        page.add(gpu_page)

    net_cost_list = params.get('net_cost_list', [])
    if len(net_cost_list) > 0:
        y = net_cost_list
        net_cost_page = line_charts(x, y, '流量耗用 (平均值：{} KB/S)'.format(params.get('net_cost_ave')))
        page.add(net_cost_page)

    cpu_temp_list = params.get('cpu_temp_list', [])
    if len(cpu_temp_list) > 0:
        y = cpu_temp_list
        cpu_temp_page = line_charts(x, y, 'CPU温度 (平均值：{} °C)'.format(params.get('cpu_temp_ave')))
        page.add(cpu_temp_page)

    battery_temp_list = params.get('battery_temp_list', [])
    if len(battery_temp_list) > 0:
        y = battery_temp_list
        battery_temp_page = line_charts(x, y, '电池温度 (平均值：{} °C)'.format(params.get('battery_temp_ave')))
        page.add(battery_temp_page)

    stutter_list = params.get('stutter_list', [])
    if len(stutter_list) > 0:
        y = stutter_list
        stutter_page = line_charts(x, y, '卡顿率 (平均值：{} %)'.format(params.get('stutter_ave')))
        page.add(stutter_page)

    fps_list = params.get('fps_list', [])
    if len(fps_list) > 0:
        y = fps_list
        fps_page = line_charts(x, y, '帧率 (平均值：{} FPS)'.format(params.get('fps_ave')))
        page.add(fps_page)

    battery_cost_list = params.get('battery_cost_list', [])
    if len(battery_cost_list) > 0:
        y = battery_cost_list
        battery_cost_page = line_charts(x, y, '耗电量 (平均值：{} mAh/min)'.format(params.get('battery_cost_ave')))
        page.add(battery_cost_page)

    page.render("app_performance_report_{}.html".format(params.get('now_time')))
