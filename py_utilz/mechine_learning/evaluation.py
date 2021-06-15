# -*- coding: utf-8 -*-
"""
Created on Sun May  6 21:11:05 2018

@author: zxy
"""
import os
from typing import List

import joblib
import numpy as np
from py_utilz.file_util import write_to_csv
from sklearn.base import clone
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold


def print_classification_result(true_labels: np.ndarray, pre_labels: np.ndarray, legal_labels: set,
                                result_output_path: str = None, print_in_terminal=True):
    """
    打印分类器预测结果
    :param true_labels: 1d array-like 真实类标号
    :param pre_labels: 1d array-like 预测类标号
    :param legal_labels: set 合法类标号的集合
    :param result_output_path: 把结果评估输出到文件中去
    :return:
    """
    if type(legal_labels) is not set:
        raise ValueError('type of legal_labels is not set')
    if set(true_labels) | set(pre_labels) > set(legal_labels):
        raise ValueError('there is illegal label in true_lables or pre_labels')
    sorted_labels = sorted(list(legal_labels))
    confusion_matrix_array = confusion_matrix(true_labels, pre_labels, labels=sorted_labels)
    if print_in_terminal:
        print('————————————————————  print result  ————————————————————')
        print(classification_report(true_labels, pre_labels, digits=4))
        print('confusion matrix (%s)' % str(sorted_labels))
        for row in confusion_matrix_array:
            print(row)
        print(
            '\nNote:Ci,j is equal to the number of observations known'
            ' to be in group i but predicted to be in group j.\n')
    if result_output_path is not None:
        if os.path.exists(result_output_path):
            raise FileExistsError('there is already a file in ' + result_output_path)
        with open(result_output_path, 'w') as f:
            f.write(classification_report(true_labels, pre_labels, digits=4))
            f.write('confusion matrix (%s)\n' % str(sorted_labels))
            for row in confusion_matrix_array:
                f.write('%s\n' % str(row))
            f.write('\nNote:Ci,j is equal to the number of observations known to be in group i'
                    ' but predicted to be in group j.')


def k_fold_cross_validation(clf, train_features: np.ndarray, train_labels: np.ndarray, k_fold: int, shuffle=False,
                            should_print=True, only_print_best=False, model_output_path=None):
    """
    k折交叉验证，打印结果
    :param clf: 分类器模型
    :param train_features: 2d np.array
    :param train_labels: 1d np.array
    :param k_fold: int 指定几折
    :param shuffle: boolean 数据顺序是否打乱
    :param should_print: boolean 结果是否在屏幕输出
    :param model_output_path: str 最优模型输出文件路径，如果为None则不输出，默认为None
    :return: best classification
    """
    str_k_fold = StratifiedKFold(n_splits=k_fold, shuffle=shuffle)
    best_clf = None
    max_score = 0
    k = 1
    for train_index, test_index in str_k_fold.split(train_features, train_labels):
        k_fold_train_features, k_fold_train_labels = train_features[train_index], train_labels[train_index]
        k_fold_test_features, k_fold_test_labels = train_features[test_index], train_labels[test_index]
        clf.fit(k_fold_train_features, k_fold_train_labels)
        k_fold_pre_labels = clf.predict(k_fold_test_features)
        current_score = clf.score(k_fold_test_features, k_fold_test_labels)
        if current_score > max_score:
            max_score = current_score
            best_clf = clone(clf)
            best_clf.fit(k_fold_train_features, k_fold_train_labels)
            best_labels = k_fold_test_labels
            best_pre_labels = k_fold_pre_labels
        if should_print and not only_print_best:
            print('———————————————————— ' + str(k) + ' fold train ————————————————————')
            print_classification_result(k_fold_test_labels, k_fold_pre_labels, set(train_labels))
            print('score:' + str(current_score))
            k += 1
    if should_print and only_print_best:
        print('———————————————————— ' + str(k) + ' fold train ————————————————————')
        print_classification_result(best_labels, best_pre_labels, set(train_labels))
        print('score:' + str(max_score))
    if model_output_path is not None:
        joblib.dump(best_clf, model_output_path)
    return best_clf


def plot_rocs(y_true: np.ndarray, y_scores: List[np.ndarray], pos_label=None, legends: List[str] = None,
              fig_file_path: str = None, roc_info_path=None):
    """
    对于两类问题画ROC曲线，y_scores之中有几个np.ndarray就会产生几个ROC曲线，狗日的pylab和pyplot接口还是有点差别的
    :param y_true: 1d-array 实际类标号，如果类标号是{-1, 1} or {0, 1}，则1将会被当做正例类，如果不是，那么要基于pos_label指定正例类
    :param y_scores: 评分，即将样本预测为pos_label的可信度，可以是后验概率、可信度指标、decision_function等等，每一个元素都是一些评分
    :param pos_label: 指定将什么类视为正例类，需要与y_score中的分数含义对应
    :param legends: 每条曲线的label
    :param fig_file_path: 图输出路径
    :param roc_info_path: fpr和tpr信息输出到文件中
    :return:
    """
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc
    from math import sqrt, pow
    plt.figure(dpi=300)
    lw = 2
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    if len(colors) < len(y_scores):
        print('Warning:len(colors):%d, but len(y_scores):%d' % (len(colors), len(y_scores)))
    if legends is not None and len(legends) != len(y_scores):
        raise ValueError('len(labels)=%d, but len(y_scores)=%d' % (len(legends), len(y_scores)))
    roc_info = list()
    for i in range(len(y_scores)):
        y_score = y_scores[i]
        color = colors[i % len(colors)]
        label = legends[i] if legends is not None else str(i)
        fprs, tprs, _ = roc_curve(y_true, y_score, pos_label=pos_label)
        best_point, min_distance = (0, 0), 1
        for j in range(len(fprs)):
            fpr, tpr = fprs[j], tprs[j]
            distance = sqrt(pow(fpr, 2) + pow(1 - tpr, 2))
            if distance < min_distance:
                best_point = (fpr, tpr)
                min_distance = distance
        roc_auc = auc(fprs, tprs)
        roc_info.append(['fprs-' + label] + fprs.tolist())
        roc_info.append(['tprs-' + label] + tprs.tolist())
        roc_info.append(['best point-' + label, '%f,%f' % best_point])
        roc_info.append(['roc-' + label, roc_auc])
        plt.plot(fprs, tprs, color=color, lw=lw, label='y_scores[%s]:ROC curve (area = %0.3f)' % (label, roc_auc))

    if roc_info_path is not None:
        write_to_csv(roc_info_path, roc_info)

    # plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right", fontsize='small')
    plt.show()
    if fig_file_path is not None:
        plt.savefig(fig_file_path)


def roc_best_points(y_true: np.ndarray, y_scores: List[np.ndarray], pos_label=None):
    """
    计算roc曲线中最优的点，即举例0,1最近的点，
    :param y_true:
    :param y_scores: 把样本预测为pos_label的概率
    :param pos_label: 将什么类记为pos_label
    :return: 返回一个List[Tuple(BestPoint,threshold)]列表，每个元素是一个最优点与阈值的tuple，即大于该阈值会被预测为pos_label
    """
    from sklearn.metrics import roc_curve
    from math import sqrt, pow

    best_points = []
    for i in range(len(y_scores)):
        fprs, tprs, thresholds = roc_curve(y_true, y_scores[i], pos_label=pos_label)
        best_point, min_distance, best_threshold = (0, 0), 1, 0
        for j in range(len(fprs)):
            fpr, tpr = fprs[j], tprs[j]
            distance = sqrt(pow(fpr, 2) + pow(1 - tpr, 2))
            if distance < min_distance:
                best_point = (fpr, tpr)
                min_distance = distance
                best_threshold = thresholds[j]
        best_points.append((best_point, best_threshold))
    return best_points
