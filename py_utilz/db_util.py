# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:33:55 2017
sql工具
@author: zxy
"""

from functools import reduce
from typing import List

import pymysql


class Configuration:
    _default_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'defualt',
        'password': '404notfound',
        'db': 'default_db',
        'charset': 'utf8'}

    def __init__(self):
        self.configuration = self._default_config.copy()

    def get_configuration(self):
        """
        获取config字典
        :return:
        """
        return self.configuration

    def set_configuration(self, k, v):
        if k not in self.configuration:
            raise KeyError(str(k), 'has not been in current configuration')
        self.configuration[k] = v

    def add_configuration(self, k, v):
        if k in self.configuration:
            raise KeyError(str(k), 'has been in current configuration')
        self.configuration[k] = v


def _percent_s(num):
    s = ['%s'] * num
    return '(' + reduce(lambda x, y: x + ',' + y, s) + ')'


def structuring_create(config: Configuration, table_name: str, column_names: List[str], type_list: List[str],
                       other_property: str = '', engine: str = 'MyISAM', charset: str = 'utf8'):
    """
    create语句
    :param config: 参数对象
    :param table_name: 指明表名
    :param column_names: 列表名的的列表
    :param type_list: 列数据类型
    :param other_property: 其他数据要求
    :param engine: 引擎
    :param charset: 知名所用字符集
    :return:
    """
    configuration = config.get_configuration()
    con = pymysql.connect(**config.get_configuration())
    try:
        with con.cursor() as curs:
            other_property = '' if other_property == '' else ',' + other_property
            sql = 'CREATE TABLE ' + configuration['db'] + '.' + table_name + \
                  ' (' + reduce(lambda x, y: x + ',' + y,
                                [column_names[i] + ' ' + type_list[i] for i in range(len(column_names))]) + \
                  other_property + ')' + 'ENGINE=' + engine + ' DEFAULT CHARACTER SET = ' + charset
            print(sql)
            curs.execute(sql)
        con.commit()
    finally:
        con.close()


def structuring_select(config: Configuration, table_name: str, column_names: List[str], where: str = '',
                       other: str = ''):
    """
    select语句
    :param config: 参数对象
    :param table_name: 指明哪个数据库
    :param column_names: 要取哪些列的列表
    :param where: 要求
    :param other: 其他要求
    :return:
    """
    configuration = config.get_configuration()
    con = pymysql.connect(**configuration)
    try:
        with con.cursor() as curs:
            sql = 'SELECT ' + reduce(lambda x, y: x + ',' + y, column_names) + \
                  ' FROM ' + table_name + ' ' + where + ' ' + other
            curs.execute(sql)
            result = curs.fetchall()
    finally:
        con.close()
    return result


def structuring_insert(config: Configuration, table_name: str, column_names: List[str], insert_rows: list,
                       buffer_size=10000):
    """
    新来的数据插入数据库
    :param config: 参数对象
    :param table_name: 指明插入哪个数据库
    :param column_names: 列名列表
    :param insert_rows: 要插入信息的列表，其中每一个元素也都是一个列表，按着columnNameList的顺序存储数据
    :param buffer_size: 缓存大小
    :return:
    """
    configuration = config.get_configuration()
    con = pymysql.connect(**configuration)
    try:
        with con.cursor() as curs:
            sql = 'INSERT INTO ' + table_name + '(' + reduce(lambda x, y: str(x) + ',' + str(y),
                                                             column_names) + ') VALUES ' + _percent_s(len(column_names))

            for start_point in range(0, len(insert_rows), buffer_size):
                end_point = start_point + buffer_size
                curs.executemany(sql, insert_rows[start_point:end_point])
                con.commit()

            curs.executemany(sql, insert_rows[end_point:])
    finally:
        con.close()


def structuring_drop(config: Configuration, table_name: str):
    configs = config.get_configuration()
    con = pymysql.connect(**configs)
    try:
        with con.cursor() as curs:
            sql = 'DROP TABLE ' + configs['db'] + '.' + table_name
            curs.execute(sql)
        con.commit()
    finally:
        con.close()


if __name__ == '__main__':
    structuring_drop('test')
    print('done')
