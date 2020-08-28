# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:21:03 2017

@author: zxy
"""
import matplotlib

from matplotlib import pyplot as plt
from typing import List
import numpy as np


@DeprecationWarning
def cdf_plot(legends: List[str], data_list: List[List], x_label: str = None, title: str = None, x_lim: List = None,
             file_path: str = None, info_path: str = None, dpi=600, show=False):
    """
    只根据数据中出现过的点绘制cdf
    不咋好用，不建议用了
    :param legends: 与list_2d一一对应
    :param data_list: 其中每一个元素都是一个list，每个list里的数字都会生成1个cdf曲线
    :param x_label:
    :param title:
    :param x_lim:
    :param file_path:
    :param info_path:
    :param dpi:
    :param show:
    :return:
    """
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    curves = []
    for row in data_list:
        sorted_row = sorted(row)
        last_num = None
        count_sum = 0
        data_list, cdfs = list(), list()
        for num in sorted_row:
            if last_num is not None and num != last_num:
                data_list.append(last_num)
                cdfs.append(count_sum / len(row))
            last_num = num
            count_sum += 1
        data_list.append(last_num)
        cdfs.append(count_sum / len(row))
        curves.append([data_list, cdfs])

    plt.figure(figsize=(8, 5))
    for index in range(len(curves)):
        x, y = curves[index]
        plt.plot(x, y, label=legends[index])

    if title is not None:
        plt.title(title, size='x-large')
    plt.xlim(x_lim)
    plt.ylim(0, 1)
    plt.ylabel('CDF', size='x-large')
    x_label = 'count' if x_label is None else x_label
    plt.xlabel(x_label, size='x-large')
    plt.legend(loc=4, fontsize='x-large')
    plt.grid(alpha=0.3)
    if file_path is not None:
        plt.savefig(file_path, dpi=dpi)
    if show:
        plt.show()

    if info_path is not None:
        content = list()
        for index in range(len(curves)):
            x, y = curves[index]
            content.append(['%s-%s' % (legends[index], x_label)] + x)
            content.append(['%s-%s' % (legends[index], 'CDF')] + y)
        from py_utilz.file_tool import write_to_csv
        write_to_csv(info_path, content)


def cdf_y_points(data: np.ndarray, xs: List[float]):
    cdf_y_points = list()
    p_i = 0
    p_data_sorted: np.ndarray = data.copy()
    p_data_sorted.sort()
    xs.sort()
    for x in xs:
        while p_i < len(p_data_sorted) and p_data_sorted[p_i] <= x:
            p_i += 1
        cdf_y_points.append(p_i / len(p_data_sorted))
    return cdf_y_points


def sparse_cdf_plot(legends: List[str], data_list: List[List], xs: List or range or np.ndarray,
                    x_label: str = None, x_ticks: List or range or np.ndarray = None,
                    title: str = None, semi_log: bool = False, file_path: str = None, info_path: str = None, dpi=600,
                    show=False):
    """
    调用示例
    testArgs = [[0, 1, 1, 2, 2, 3, 3, 4, 5],
                [10, 10, 12, 12, 14, 14, 16, 18]]
    sparse_cdf_plot(['B', 'M'], testArgs, xs=range(0, 20), show=True, info_path='../temp/info.txt',
                    file_path='../temp/pic.png')

    testArgs = [[0, 1, 1, 2, 2, 3, 3, 4, 5],
                [10, 10, 12, 12, 14, 14, 16, 18]]
    sparse_cdf_plot(['B', 'M'], testArgs, xs=range(0, 20), x_ticks=range(0, 20, 1), show=True,
                    info_path='../temp/info.txt',
                    file_path='../temp/pic.png')

    testArgs = [[0, 10, 10, 20, 20, 30, 30, 40, 50],
                [10, 100, 120, 120, 350, 450, 500, 800, 900]]
    sparse_cdf_plot(['B', 'M'], testArgs, xs=range(1, 1000, 10), show=True, info_path='../temp/info.txt',
                    file_path='../temp/pic.png', semi_log=True)

    testArgs = [[0.001, 0.003, 0.005, 0.02, 0.03, 0.07, 0.3, 0.5, 0.7],
                [0.01, 0.03, 0.05, 0.08, 0.2, 0.4, 0.6, 0.9, 1.2, 1.5, 3, 6, 9]]
    sparse_cdf_plot(['B', 'M'], testArgs, xs=np.arange(0.1, 10, 0.2), show=True, info_path='../temp/info.txt',
                    file_path='../temp/pic.png', semi_log=True)
    按照给定的标度对数据进行分割
    目前并不支持自选颜色，并且没有参数校验！请自行确定参数正确！懒得写了！
    :param legends: 标签
    :param data_list: 数据列表
    :param xs: 需要打点的横坐标
    :param x_label: 横轴文字
    :param x_ticks: 横轴坐标
    :param title: 图标题
    :param semi_log: 是否半对数表示，如果是半对数表示，要求xs的最小值不能为0，建议为数据中比最小值更小的10的n次方，如0.1，因为半对数坐标中不应该包含0
    :param file_path: 输出文件路径
    :param info_path: 输出二维坐标信息的文件路径
    :param dpi: 图片分辨率
    :param show: 生成图片后是否直接展示 注明：有可能会block住后续程序的执行，如果需要绘制多个图片建议关闭
    :return:
    """
    if type(xs) is range:
        xs = list(xs)

    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    cdf_y_points_list = []
    for data in data_list:
        cdf_y_points_list.append(cdf_y_points(np.array(data), xs))

    plt.figure(figsize=(8, 5))
    for index, ys in enumerate(cdf_y_points_list):
        plt.plot(xs, ys, label=legends[index], marker='o', markersize=6, linewidth=2)

    if title is not None:
        plt.title(title, size='x-large')
    plt.xlim([np.min(xs), np.max(xs)])
    plt.xticks(x_ticks)
    plt.ylim(0, 1)
    plt.ylabel('CDF', size='x-large')
    x_label = 'count' if x_label is None else x_label
    plt.xlabel(x_label, size='x-large')
    plt.legend(loc=4, fontsize='x-large')
    plt.grid(alpha=0.3)
    if semi_log:
        plt.semilogx()
    if file_path is not None:
        plt.savefig(file_path, dpi=dpi)
    if show:
        plt.show()

    if info_path is not None:
        content = list()
        content.append(['xs'] + list(map(lambda x: str(x), xs)))
        for index, ys in enumerate(cdf_y_points_list):
            content.append(['%s-%s' % (legends[index], 'CDF')] + list(map(lambda y: '%.5f' % y, ys)))
        from py_utilz.file_tool import write_to_csv
        write_to_csv(info_path, content, check_exist=False)


def cluster_elbow(x: List[int], err: List[float], title: str, file_path: str = None, x_label='K', y_label='error'):
    """
    聚类肘部法则画图用的
    :param x:
    :param err:
    :param title:
    :param file_path:
    :param x_label:
    :param y_label:
    :return:
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(dpi=300)
    ax = plt.gca()
    ax.plot(x, err)
    ax.set_xlim([0, max(x)])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # pl.ylabel('ERROR',rotation='horizontal')
    plt.title(title)
    if file_path is not None:
        plt.savefig(file_path)
    plt.show()


def scatter(legend_list: List[str], xs_list: List[List], ys_list: [List], marker_list: List[str],
            color_list: List[str or tuple],
            title: str = None, x_label: str = None, y_label: str = None, x_lim: list = None,
            ylim: list = None, file_path: str = None, dpi=1500):
    """
    绘制散点图
    示例
    scatter(legend_list=["a", "b"], xs_list=[[1, 2, 3], [1.1, 2.2, 3.3]], ys_list=[[1, 4, 6], [2.1, 2.2, 2.3]],
            marker_list=["x", "o"], color_list=[(0.1, 0.2, 0.5), "b"])
    :param legend_list: 标签列表，顺序需要与x_list,y_list中的数据对应
    :param xs_list: 横坐标列表
    :param ys_list: 纵坐标列表
    :param marker_list: 打点的符号类型，具体可用的请查阅https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
    :param color_list: 颜色列表，可用的包括rgb元组，16进制rgb，以及单字符等等，具体请查阅https://matplotlib.org/api/colors_api.html?highlight=color#module-matplotlib.colors
    :param title:
    :param x_label:
    :param y_label:
    :param x_lim:
    :param ylim:
    :param file_path:
    :param dpi:
    :return:
    """
    plt.figure(figsize=(8, 5))
    for index in range(len(legend_list)):
        plt.scatter(xs_list[index], ys_list[index], marker=marker_list[index], c=color_list[index])

    plt.xlim(x_lim)
    plt.ylim(ylim)
    plt.ylabel('y_label' if y_label is None else y_label, size='x-large', rotation='horizontal')
    plt.xlabel('x_label' if x_label is None else x_label, size='x-large')
    plt.title('title' if title is None else title, size='x-large')
    plt.legend(legend_list, loc=4, fontsize='x-large')
    plt.grid(alpha=0.3)
    if not file_path is None:
        plt.savefig(file_path, dpi=dpi)

    plt.show()


if __name__ == '__main__':
    # testArgs = [[0, 1, 1, 2, 2, 3, 3, 4, 5],
    #             [10, 10, 12, 12, 14, 14, 16, 18]]
    # sparse_cdf_plot(['B', 'M'], testArgs, xs=range(0, 20), show=True, info_path='../temp/info.txt',
    #                 file_path='../temp/pic.png')
    #
    # testArgs = [[0, 1, 1, 2, 2, 3, 3, 4, 5],
    #             [10, 10, 12, 12, 14, 14, 16, 18]]
    # sparse_cdf_plot(['B', 'M'], testArgs, xs=range(0, 20), x_ticks=range(0, 20, 1), show=True,
    #                 info_path='../temp/info.txt',
    #                 file_path='../temp/pic.png')
    #
    # testArgs = [[0, 10, 10, 20, 20, 30, 30, 40, 50],
    #             [10, 100, 120, 120, 350, 450, 500, 800, 900]]
    # sparse_cdf_plot(['B', 'M'], testArgs, xs=range(1, 1000, 10), show=True, info_path='../temp/info.txt',
    #                 file_path='../temp/pic.png', semi_log=True)
    #
    # testArgs = [[0.001, 0.003, 0.005, 0.02, 0.03, 0.07, 0.3, 0.5, 0.7],
    #             [0.01, 0.03, 0.05, 0.08, 0.2, 0.4, 0.6, 0.9, 1.2, 1.5, 3, 6, 9]]
    # sparse_cdf_plot(['B', 'M'], testArgs, xs=np.arange(0.1, 10, 0.2), show=True, info_path='../temp/info.txt',
    #                 file_path='../temp/pic.png', semi_log=True)

    # scatter(legend_list=["a", "b"], xs_list=[[1, 2, 3], [1.1, 2.2, 3.3]], ys_list=[[1, 4, 6], [2.1, 2.2, 2.3]],
    #         marker_list=["x", "o"], color_list=[(0.1, 0.2, 0.5), "b"])
    print('done')
