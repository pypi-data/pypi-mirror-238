# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: estimator.py
# @Author: MinXin
# @Time: 2021 10 29

from tqdm import tqdm
from collections import defaultdict


class Dialogue(object):
    def __init__(self):
        pass

    ## merge dialogue from jsonl by one key
    def merge_by_key(self, input_data: list, merge_key: [int, str], sort_key: [int, str] = None):
        results = defaultdict(list)
        for i in tqdm(range(len(input_data)), desc="merge dialogue"):
            one_line = input_data[i]
            results[one_line[merge_key]].append(one_line)
        if sort_key:
            for key in tqdm(list(results.keys()), desc="sort dialogue"):
                results[key] = sorted(results[key], key=lambda x: x[sort_key])
        return results


if __name__ == '__main__':
    test_dg = Dialogue()
    input_data = [{"id": 1, "time": 100, "text": "1"}, {"id": 2, "time": 100, "text": "2"},
                  {"id": 3, "time": 100, "text": "3"}, {"id": 2, "time": 102, "text": "21"},
                  {"id": 2, "time": 10200, "text": "22"},{"id":2, "time":10211, "text":"23"}]
    results = test_dg.merge_by_key(input_data, merge_key="id", sort_key="time")
    print(results)
