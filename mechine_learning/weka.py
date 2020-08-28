# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:33:11 2018

@author: zxy
"""

from py_utilz import file_tool
from typing import Dict
import numpy as np
import pandas as pd


class ARFF:
    """
    arff文件对象，除了可以储存arff数据，包含一些arff文件处理的工具方法
    """

    def __init__(self, relation: str, data: pd.DataFrame, attribute_types: np.ndarray = None):
        self.relation = relation
        self.data = data
        self.attribute_types: np.ndarray = attribute_types

    @classmethod
    def read_arff(cls, file_path: str, titile_seperator: str = ' ', data_seperator: str = ','):
        """
        读取arff文件
        :param titile_seperator:@attribute或@relation与名字之间的分隔符
        :param data_seperator: 数据间的分隔符
        :param file_path:
        :return: 一个arff对象
        """
        content = file_tool.read_from_char_file(file_path)
        relation = ''
        attribute_names = list()
        attribute_types = list()
        data_start_index = 0
        name_type = dict()
        for index in range(len(content)):
            line = content[index]
            if line.startswith('%'):
                continue
            if line.lower().startswith('@relation'):
                relation = line.split(titile_seperator, maxsplit=1)[1]
            if line.lower().startswith('@attribute'):
                fields = line.split(titile_seperator, maxsplit=2)
                if len(fields) != 3:
                    raise ValueError('bad title,check the parameter or the file:' + repr(line))
                attribute_name, attribute_type = fields[1], fields[2]
                attribute_names.append(attribute_name)
                attribute_types.append(attribute_type)
                name_type[attribute_name] = np.float64 if attribute_type.lower() in {'real', 'numeric'} else np.str_
            if line.lower().startswith('@data'):
                data_start_index = index + 1
                break

        attribute_matrix = list()
        for line in content[data_start_index:]:
            fields = line.split(data_seperator)
            if line.startswith('%') or len(fields) != len(attribute_names):
                print('warning:bad data line:' + line)
                continue
            temp = list()
            for index in range(len(fields)):
                if attribute_types[index].lower() in {'real', 'numeric'}:
                    temp.append(float(fields[index]))
                else:
                    temp.append(fields[index])
            attribute_matrix.append(temp)
        data = pd.DataFrame(attribute_matrix, columns=attribute_names)
        data: pd.DataFrame = data.astype(name_type)

        return cls(relation, data, np.array(attribute_types))


def csv_to_arff(input_file_path: str, output_file_path: str, relation='data', type_dict: Dict[str, str] = None):
    """
    将csv文件转换为arff文件格式
    :param input_file_path:
    :param output_file_path:
    :param relation:
    :param type_dict:
    :return:
    """
    csv_input_file = file_tool.readFromCsv(input_file_path)
    title_list = [['@relation\t' + relation]]
    for index in range(len(csv_input_file[0])):
        attribute = csv_input_file[0][index]
        if type_dict is None:
            row = '@attribute\t' + attribute + '\tNumeric'
        elif attribute in type_dict:
            row = '@attribute\t' + attribute + '\t' + type_dict[attribute]
        else:
            row = '@attribute\t' + attribute + '\tNumeric'

        title_list.append(row.split(','))
    title_list.append(['@DATA'])
    file_tool.writeToCsv(output_file_path, title_list + csv_input_file[1:])


if __name__ == '__main__':
    # arff = ARFF.read_arff('G:\\auto-update ensemble\python_code\\temp\weka test data\\ionosphere.arff')
    # print(arff.data.dtypes)
    # print(arff.data)
    pass
