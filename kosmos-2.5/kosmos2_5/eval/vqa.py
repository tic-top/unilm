from ned import calculate_ned
import argparse
import json
import os
from multiprocessing import Pool

# model_name = "210"
model_name = "varyvqa"
# model_name = "vary-docvqa-ocr"
json_path = "/home/yilinjia/MambaOCR/sampled/docvqa/test.json"
result_root = f"/home/yilinjia/MambaOCR/outcome/{model_name}/docvqa_result"

def process_item(item):
    qas = item["qas"]
    for qa in qas:
        # print(qa)
        # print(type(qa))
        qid = qa["qid"]
        result_path = os.path.join(result_root, qid + ".txt")
        if not os.path.exists(result_path):
            continue
        with open(result_path, "r") as f:
            pred = f.read()
        max_ned = 0
        while len(pred)>=1 and pred[-1] == ".":
            pred = pred[:-1]
        pred = " ".join(pred.strip().lower().split())

        for gt in qa["answer"]:
            gt_answer = gt["text"]
            gt_answer = " ".join(gt_answer.strip().lower().split())
            ned = calculate_ned(pred, gt_answer)
            max_ned = max(max_ned, ned)

        if max_ned < 0.5:
            max_ned = 0
        json_path = result_path.replace(".txt", ".json")
        with open(json_path, "w") as f:
            json.dump({"anls": max_ned}, f)

items = json.load(open(json_path, "r"))

with Pool(32) as p:
    p.map(process_item, items)

# reduce
anslAcc = 0
cnt = 0
for item in items:
    qas = item["qas"]
    for qa in qas:
        qid = qa["qid"]
        result_path = os.path.join(result_root, qid + ".txt")
        json_path = result_path.replace(".txt", ".json")
        if not os.path.exists(json_path):
            continue
        with open(json_path, "r") as f:
            data = json.load(f)
        anslAcc += data["anls"]
        cnt += 1
        os.remove(json_path)

print(anslAcc/cnt, cnt)
        


    
