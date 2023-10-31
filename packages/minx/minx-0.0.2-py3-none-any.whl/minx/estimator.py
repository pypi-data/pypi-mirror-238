# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: estimator.py
# @Author: MinXin
# @Time: 2021 10 29
import numpy as np
from collections import defaultdict
from sklearn.metrics import accuracy_score, classification_report, precision_recall_curve, roc_auc_score, \
    average_precision_score

"""
用法示例：
    labels_name = ['label1', 'label2', 'label3']
    est = estimator(labels_name)
    pred_scores = [[0.1,0.3,0.6],[0.2,0.7,0.1],[0.5,0.8,0.1]]
    true_labels = [2,1,0]
    result, values = est.estimate(pred_scores, true_labels)
其中,result={"report":report, "auc_text":auc_text, "mAP_text":mAP_text, "p_r_equal_text":p_r_equal_text}，里面所有value均为格式化后的string，可直接打印
而values与result格式基本一致，但字典中的value为list，保存了每个标签具体的值
"""


class Estimator(object):
    def __init__(self, labels_name: list):
        self.labels_name = labels_name
        self.label_number = len(labels_name)

    def get_label_argmax(self, score: list):
        return score.index(max(score))

    def get_label_threshold(self, score: list, threshold: list):
        for i in range(len(threshold)):
            t = threshold[i]
            if t == -1:
                continue
            elif score[i] >= t:
                return i
        return 0

    def estimate(self, pred_scores: list, true_labels: list):
        '''
        返回相关统计指标
        return: result为可直接打印的string, values为相关统计值
        '''
        true_bin_labels = defaultdict(list)
        for label in true_labels:
            for i in range(self.label_number):
                if label == i:
                    true_bin_labels[i].append(1)
                else:
                    true_bin_labels[i].append(0)

        pred_labels = []
        pred_bin_scores = defaultdict(list)
        for score in pred_scores:
            label = self.get_label_argmax(score)
            pred_labels.append(label)
            for i in range(self.label_number):
                pred_bin_scores[i].append(score[i])

        values = {}

        mean_auc = 0.0
        auc_text = ''
        values['auc'] = []
        for i in range(self.label_number):
            # 忽略normal标签
            #if i == 0:
            #    continue
            auc = roc_auc_score(true_bin_labels[i], pred_bin_scores[i])
            #print("%s auc:%.4f" % (self.labels_name[i], auc), end=' | ')
            auc_text += "%s auc:%.4f | " % (self.labels_name[i], auc)
            mean_auc += auc
            values['auc'].append(auc)
        #print("\nmean_AUC:%.4f" % (mean_auc / (self.label_number - 1)))
        mean_auc = mean_auc / len(values['auc'])
        auc_text += "\nmean_AUC:%.4f" % (mean_auc)
        values['auc'].append(mean_auc)

        mean_mAP = 0.0
        mAP_text = ''
        values['mAP'] = []
        for i in range(self.label_number):
            # 忽略normal标签
            #if i == 0:
            #    continue
            AP = average_precision_score(true_bin_labels[i], pred_bin_scores[i], average='macro')
            #print("%s mAP:%.4f" % (self.labels_name[i], mAP), end=' | ')
            mAP_text += "%s AP:%.4f | " % (self.labels_name[i], AP)
            mean_mAP += AP
            values['mAP'].append(AP)
        #print("\nmean_mAP:%.4f" % (mean_mAP / (self.label_number - 1)))
        mean_mAP = mean_mAP / len(values['mAP'])
        mAP_text += "\nmAP:%.4f" % (mean_mAP)
        values['mAP'].append(mean_mAP)

        p_r_equal_text = ''
        values['p_r_equal'] = []
        for i in range(self.label_number):
            precision, recall, thresholds = precision_recall_curve(true_bin_labels[i], pred_bin_scores[i])
            m_ids = np.argmin(abs(precision - recall))
            #print("%s\t[p=r]\t%.4f\tthreshold:%.4f" % (
            #    self.labels_name[i], recall[m_ids], thresholds[m_ids]))
            p_r_equal_text += "%s\t[p=r]\t%.4f\tthreshold:%.4f\n" % (self.labels_name[i], recall[m_ids], thresholds[m_ids])
            values['p_r_equal'].append([recall[m_ids], thresholds[m_ids]])

        report = classification_report(true_labels, pred_labels, target_names=self.labels_name, digits=4)
        #print(report)

        result = {'report':report, 'auc_text':auc_text, 'mAP_text':mAP_text, 'p_r_equal_text':p_r_equal_text}

        return result, values


if __name__ == '__main__':
    pred_scores = [[0.1,0.3,0.6],[0.2,0.7,0.1],[0.5,0.8,0.1]]
    true_labels = [2,1,0]
    labels_name = ['label1', 'label2', 'label3']
    est = estimator(labels_name)
    result, values = est.estimate(pred_scores, true_labels)
    for k in result.keys():
        print(result[k])
    print(values)
