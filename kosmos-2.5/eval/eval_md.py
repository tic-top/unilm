import os
import json
import argparse
from multiprocessing import Pool
from tqdm import tqdm

from utils import calculate_ned, calculate_nted


def calculate(gt_path, pred_path):
    try:
        gt, pred = open(gt_path, "r").read(), open(pred_path, "r").read()
    except Exception as e:
        print(e)
        print(pred_path)
        return 1, 1
    pred = pred.replace("markdown", "")
    pred = pred.replace("latex", "")
    pred = pred.replace("Latex", "")
    if "arxiv" in gt_path:
        # change \n# to \n\n#
        # pred = pred.replace(r"\n#", r"\n\n#")
        pass
    if "image2latex" in gt_path or "chrome_math" in gt_path:
        def latexfilter(x):
            x = x.replace(" ", "")
            x = x.replace("$", "\n")
            x = x.replace("\]", "\n")
            x = x.replace("\[", "\n")
            while '  ' in x:  
                x = x.replace('  ', ' ') 
            x = x.replace("\n ", "\n")
            while "\n\n" in x:
                x = x.replace("\n\n", "\n")
            x = x.replace("\n", "\n\n")
            return x
        gt, pred = latexfilter(gt), latexfilter(pred)

    if "table" in gt_path:
        lines = pred.split("\n")
        line1 = lines[0]
        if "able " in line1:
            lines = lines[1:]
            pred = "\n".join(lines) + "\n\n" + line1
        def filter(s):
            s = s.replace(":", "")
            while '--' in s:  
                s = s.replace('--', '-')  
            return s
        gt, pred = filter(gt), filter(pred)
    ned = calculate_ned(gt, pred)
    nted = calculate_nted(gt, pred)
    # if ned < 0.3:
    #     print(gt_path)
    #     print(pred_path)
    #     print(gt)
    #     print(pred)
    #     print(ned, nted)
    #     sys.exit(1)
    json_path = pred_path.replace(".md", ".json")
    with open(json_path, "w") as f:
        f.write(json.dumps({"ned": ned, "nted": nted}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", type=str, default="/home/yuzhongzhao/zyz/ckpts/eval/", help="Path to the evaluation data")
    parser.add_argument("--type", "-t", type=str, default="image2latex", help="Data type")
    parser.add_argument("--pred", "-p", type=str, default="case/", help="Path to the predictions")
    
    args = parser.parse_args()
    name = args.pred.split("/")[-1]

    gt_dir = os.path.join(args.data, args.type, "mds")
    assert os.path.exists(gt_dir)

    gt_paths, pred_paths = [], []
    total = 0
    # map in parallel
    for root, dirs, files in os.walk(gt_dir):
        for file in tqdm(files, desc=name+" map", disable=True, colour="green"):
            if file.endswith(".md"):
                total += 1
                gt_path = os.path.join(gt_dir, file)
                pred_path = os.path.join(args.pred, file)
                if not os.path.exists(pred_path):
                    # print(f"missing {pred_path}")
                    continue
                gt_paths.append(gt_path)
                pred_paths.append(pred_path)

    with Pool(64) as p:
        p.starmap(calculate, zip(gt_paths, pred_paths))

    # reduce
    nedAcc = 0
    ntedAcc = 0
    cnt = 0
    for root, dirs, files in os.walk(args.pred):
        for file in tqdm(files, desc=name+" reduce", colour="red"):
            if file.endswith(".json"):
                pred_path = os.path.join(args.pred, file)
                data = json.load(open(pred_path, "r"))
                ned, nted = data["ned"], data["nted"]
                nedAcc += ned
                ntedAcc += nted
                cnt += 1
                os.remove(pred_path)
    if cnt==0:
        print(f"No files found in {args.pred}")
    else:
        print(f"NED/NTED: {nedAcc / cnt:.3f} / {ntedAcc / cnt:.3f} CNT: {cnt} / {total}")