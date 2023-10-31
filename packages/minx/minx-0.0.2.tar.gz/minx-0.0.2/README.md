#### 1.Estimator

```
功能：计算分类结果的precision,recall,f1,auc,mAP,(precision=recall)'s threshold
用法示例：
    from minx import Estimator
    labels_name = ['label1', 'label2', 'label3']
    est = estimator(labels_name)
    pred_scores = [[0.1,0.3,0.6],[0.2,0.7,0.1],[0.5,0.8,0.1]]
    true_labels = [2,1,0]
    result, values = est.estimate(pred_scores, true_labels)
其中,result={"report":report, "auc_text":auc_text, "mAP_text":mAP_text, "p_r_equal_text":p_r_equal_text}，里面所有value均为格式化后的string，可直接打印
而values与result格式基本一致，但字典中的value为list，保存了每个标签具体的值
```
#### 2.Dialogue

```
功能：对话文本处理
用法示例：
    from minx import Dialogue
    test_dg = Dialogue()
    input_data = [{"id": 1, "time": 100, "text": "1"}, {"id": 2, "time": 100, "text": "2"},
                  {"id": 3, "time": 100, "text": "3"}, {"id": 2, "time": 102, "text": "21"},
                  {"id": 2, "time": 10200, "text": "22"},{"id":2, "time":10211, "text":"23"}]
    ## 按某一关键字从jsonl中聚合对话，支持jsonl中的item为dict或list
    results = test_dg.merge_by_key(input_data, merge_key="id", sort_key="time")
```
