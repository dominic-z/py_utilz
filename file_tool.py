# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:55:05 2017

row : a list of one line
line : a string of the line

@author: zxy
"""
import re
import csv
from typing import List, Iterable


def print_some_line(file_path: str, num=1, start_row_index=0, encoding='utf8'):
    """
    打印file_path文件的前count行
    :param file_path: str 文件路径
    :param num: int 打印多少行
    :param start_row_index: int 从第几行开始打印（包括），行号从0开始计数
    :param encoding: str 制定字符集
    :return:
    """
    with open(file_path, 'r', encoding=encoding) as file:
        for row_index in range(start_row_index + num):
            if row_index < start_row_index:
                next(file)
            else:
                print(repr(next(file)))


def read_from_csv(file_path: str, start_row_index=0, end_row_index=None, encoding='utf8'):
    """
    从CSV文件之中读取信息
    :param file_path: str 文件路径
    :param start_row_index: int 从第几行开始打印（包括），行号从0开始计数
    :param end_row_index: int 从读取到几行（不包括），行号从0开始计数
    :param encoding: str 制定字符集
    :return: list 每个元素也是一个列表，代表一行
    """
    csv.field_size_limit(1000000)
    with open(file_path, 'r', newline='', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        rows: List[List[str]] = list()
        for row_index in range(start_row_index):
            next(csv_reader)
        row_index = start_row_index
        for row in csv_reader:
            if end_row_index is not None and row_index >= end_row_index:
                break
            rows.append(row)
            row_index += 1

    return rows


def yield_read_from_csv(file_path: str, start_row_index=0, end_row_index=None, encoding='utf8'):
    """
    yield算法
    从CSV文件之中读取信息
    :param file_path: str 文件路径
    :param start_row_index: int 从第几行开始打印（包括），行号从0开始计数
    :param end_row_index: int 从读取到几行（不包括），行号从0开始计数
    :param encoding: str 制定字符集
    :return: list 代表一行
    """
    csv.field_size_limit(1000000)
    with open(file_path, 'r', newline='', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        for row_index in range(start_row_index):
            csv_reader.__next__()
        row_index = start_row_index
        for row in csv_reader:
            if end_row_index is not None and row_index >= end_row_index:
                break
            row: List[str] = row
            yield row
            row_index += 1


def read_from_char_file(file_path: str, start_row_index=0, end_row_index=None, encoding='utf8'):
    """
    从CSV文件之中读取信息
    :param file_path: str 文件路径
    :param start_row_index: int 从第几行开始打印（包括），行号从0开始计数
    :param end_row_index: int 从读取到几行（不包括），行号从0开始计数
    :param encoding: str 制定字符集
    :return: list 每个元素也是一个列表，代表一行
    """

    with open(file_path, 'r', encoding=encoding) as file:
        lines: List[str] = list()
        for row_index in range(start_row_index):
            file.__next__()
        row_index = start_row_index
        for row in file:
            if end_row_index is not None and row_index >= end_row_index:
                break
            row = re.sub("\n$", "", row)
            lines.append(row)
            row_index += 1
    return lines


def yield_read_from_char_file(file_path: str, start_row_index=0, end_row_index=None, encoding='utf8'):
    """
    yield算法
    从CSV文件之中读取信息
    :param file_path: str 文件路径
    :param start_row_index: int 从第几行开始打印（包括），行号从0开始计数
    :param end_row_index: int 从读取到几行（不包括），行号从0开始计数
    :param encoding: str 制定字符集
    :return: list 代表一行
    """
    with open(file_path, 'r', encoding=encoding) as file:
        for line_index in range(start_row_index):
            file.__next__()
        line_index = start_row_index
        for line in file:
            if end_row_index is not None and line_index >= end_row_index:
                break
            yield re.sub("\n$", "", line)
            line_index += 1


def write_to_char_file(file_path: str, lines: List, encoding='utf8', buffer_size=50000, check_exist=True):
    """
    向字符文件中写入row_list内容
    :param file_path: string,output file path
    :param lines: list,every item is a string object and takes up one line
    :param encoding: str charset
    :param buffer_size:
    :param check_exist: 是否检查文件是否存在，如果检查，且文件已经存在，则抛出异常；如果不检查，无论存在与否，都会创建或覆盖新文件
    :return:
    """
    import os
    if check_exist and os.path.exists(file_path):
        raise FileExistsError('there is already a file in' + file_path)
    with open(file_path, 'w', encoding=encoding) as writer:
        buffer = ""
        for i, line in enumerate(lines):
            buffer += line + '\n'
            if i % buffer_size == 0:
                writer.write(buffer)
                buffer = ""
        writer.write(buffer)


def write_to_csv(file_path: str, rows: List[Iterable], encoding='utf8', buffer_size=50000, check_exist=True):
    """
    向CSV文件之中写入信息
    :param file_path: string,output file path
    :param rows: list,every item is a string object and takes up one line
    :param encoding: str charset
    :param buffer_size: int buffer_size
    :param check_exist: 是否检查文件是否存在，如果检查，且文件已经存在，则抛出异常；如果不检查，无论存在与否，都会创建或覆盖新文件
    :return:
    """
    import os
    if check_exist and os.path.exists(file_path):
        raise FileExistsError('there is already a file in ' + file_path)
    with open(file_path, 'w', newline='', encoding=encoding) as file:
        csv_writer = csv.writer(file)
        buffer_list = list()
        for row in rows:
            buffer_list.append(row)
            if len(buffer_list) % buffer_size == 0:
                csv_writer.writerows(buffer_list)
                buffer_list.clear()
        csv_writer.writerows(buffer_list)


def add_to_char_file(file_path: str, lines: List, encoding='utf8', buffer_size=50000, check_exist=False):
    """
    向已存在的CSV文件的尾行信息
    :param file_path: string,output file path
    :param lines: list,every item is a string object and takes up one line
    :param encoding: str charset
    :param buffer_size: int buffer_size
    :param check_exist: boolean 是否要检查文件是否存在
    :return:
    """
    import os
    if check_exist and not os.path.exists(file_path):
        raise FileNotFoundError(file_path + ' does not exist')
    with open(file_path, 'a', newline='', encoding=encoding) as writer:
        buffer = ""
        for i, line in enumerate(lines):
            buffer += line + '\n'
            if i % buffer_size == 0:
                writer.write(buffer)
                buffer = ""
        writer.write(buffer)


def add_to_csv(file_path: str, rows: List[Iterable], encoding='utf8', buffer_size=50000, check_exist=False):
    """
    向已存在的CSV文件的尾行信息
    :param file_path: string,output file path
    :param rows: list,every item is a string object and takes up one line
    :param encoding: str charset
    :param buffer_size: int buffer_size
    :param check_exist: boolean 是否要检查文件是否存在
    :return:
    """
    import os
    if check_exist and not os.path.exists(file_path):
        raise FileNotFoundError(file_path + ' does not exist')
    with open(file_path, 'a', newline='', encoding=encoding) as file:
        csv_writer = csv.writer(file)
        buffer_list = list()
        for row in rows:
            buffer_list.append(row)
            if len(buffer_list) % buffer_size == 0:
                csv_writer.writerows(buffer_list)
                buffer_list.clear()
        csv_writer.writerows(buffer_list)


if __name__ == '__main__':
    # done
    print('done')
