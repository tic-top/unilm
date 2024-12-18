from ned import calculate_ned
from nted import calculate_nted
import argparse
import os
import sys
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # ground truth folder
    # pred folder
    parser.add_argument("--gt", "-g", type=str, default="case/")
    parser.add_argument("--pred", "-p", type=str, default="case/")
    args = parser.parse_args()
    name = args.pred.split("/")[-1]
    nedAcc = 0
    ntedAcc = 0
    cnt = 0
    ss = 0
    for root, dirs, files in os.walk(args.gt):
        for file in tqdm(files, desc=name):
            if file.endswith(".md"):
                try:
                    gt = open(os.path.join(root, file)).read()
                    pred = open(os.path.join(args.pred, file)).read()
                except:
                    continue
                # if the first line of pred is "markdown"
                #remove markdown latex Latex
                pred = pred.replace("markdown", "")
                pred = pred.replace("latex", "")
                pred = pred.replace("Latex", "")

                if "image2latex" in root or "chrome_math" in root:
                    # print(pred)
                    def latexfilter(x):
                        # remove " ", "$", "\]", "\["
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

                if "table" in root:
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
                nedAcc += ned
                ntedAcc += nted
                cnt += 1
    print(f"NED/NTED: {nedAcc / cnt:.3f} / {ntedAcc / cnt:.3f} CNT: {cnt} / {len(files)}")