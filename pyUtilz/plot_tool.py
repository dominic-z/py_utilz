# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:21:03 2017

@author: zxy
"""
import matplotlib

from matplotlib import pyplot as plt
from typing import List
import numpy as np


def cdf_points(data: np.ndarray, xs: np.ndarray):
    cdf_y_points = list()
    p_i, n_i = 0, 0
    p_data_sorted: np.ndarray = data.copy()
    p_data_sorted.sort()
    for x in xs:
        while p_i < len(p_data_sorted) and p_data_sorted[p_i] <= x:
            p_i += 1
        cdf_y_points.append(p_i / len(p_data_sorted))
    return cdf_y_points


def cdf_plot(legends: List[str], nums: List[List], x_label: str = None, title: str = None, x_lim: List = None,
             file_path: str = None, info_path: str = None, dpi=600, show=False):
    """
    :param legends: 与list_2d一一对应
    :param nums: 其中每一个元素都是一个list，每个list里的数字都会生成1个cdf曲线
    :param x_label:
    :param title:
    :param x_lim:
    :param file_path:
    :param dpi:
    :return:
    """
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    curves = []
    for row in nums:
        sorted_row = sorted(row)
        last_num = None
        count_sum = 0
        nums, cdfs = list(), list()
        for num in sorted_row:
            if last_num is not None and num != last_num:
                nums.append(last_num)
                cdfs.append(count_sum / len(row))
            last_num = num
            count_sum += 1
        nums.append(last_num)
        cdfs.append(count_sum / len(row))
        curves.append([nums, cdfs])

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
        from utilz.file_tool import write_to_csv
        write_to_csv(info_path, content)


def sparse_cdf_plot(legends: List[str], data_list: List[List], xs: List[float], x_label: str = None,
                    title: str = None, file_path: str = None, info_path: str = None, dpi=600, show=False):
    """
    按照特定的标度对数据进行分割

    """
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    curves = []
    for data in data_list:
        sorted_row = sorted(data)
        count_sum = 0
        i, cdfs = 0, list()
        for point in xs:
            while i < len(sorted_row) and point >= sorted_row[i]:
                count_sum += 1
                i += 1
            cdfs.append(count_sum / len(sorted_row))
        curves.append([xs, cdfs])

    plt.figure(figsize=(8, 5))
    for index in range(len(curves)):
        x, y = curves[index]
        plt.plot(x, y, label=legends[index], marker='o', markersize=6, linewidth=2)

    if title is not None:
        plt.title(title, size='x-large')
    plt.xlim([np.min(xs), np.max(xs)])
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
        from utilz.file_tool import write_to_csv
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


def scatter(legend_list: List[str], x_list: list, y_list: list, marker_list: List[str], color_list: List[str],
            title: str = None, x_label: str = None, y_label: str = None, x_lim: list = None,
            ylim: list = None, file_path: str = None, dpi=1500):
    plt.figure(figsize=(8, 5))
    for index in range(len(legend_list)):
        plt.scatter(x_list[index], y_list[index], marker=marker_list[index], c=color_list[index])

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
    #    testArgs=[[0,1,1,2,2,3,3,4,5],
    #          [10,10,12,12,14,14,16,18]]
    # cdfPlot(['B','M'],testArgs[0],testArgs[1])
    print('done')
