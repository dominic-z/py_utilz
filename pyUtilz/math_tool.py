# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 12:20:51 2018

@author: zxy
"""


def divide(dividend, divisor, zero_default=0) -> float:
    """
    除法，如果分母为零
    :param dividend: num 被除数
    :param divisor: num 除数
    :param zero_default: 如果除数为0的默认返回值
    :return:
    """
    return dividend / divisor if divisor != 0 else zero_default
