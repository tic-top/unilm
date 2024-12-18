import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", type=str, default="/home/yuzhongzhao/zyz/ckpts/eval/", help="Path to the evaluation data")
    parser.add_argument("--type", "-t", type=str, default="cord", help="Task type")
    parser.add_argument("--pred", "-p", type=str, default="case/", help="Path to the predictions")

    args = parser.parse_args()

    cwd = os.getcwd()
    eval_script_dir = os.path.join(args.data, "ocr_eval")
    assert os.path.exists(eval_script_dir)

    os.system(f"rm -rf ocr_result_{args.type}.txt")
    os.system(f"rm -rf {args.type}_s.zip")
    os.system(f"rm -rf {args.type}_gt.zip")

    os.system(f"zip -rj -q {args.type}_s.zip {args.pred}")
    gt_data_dir = os.path.join(args.data, args.type, "ocrs")
    assert os.path.exists(gt_data_dir)
    print(gt_data_dir)
    os.system(f"zip -rj -q {args.type}_gt.zip {gt_data_dir}")

    os.system(f"python {eval_script_dir}/script.py -g={args.type}_gt.zip -s={args.type}_s.zip | tee -a {cwd}/ocr_result_{args.type}.txt")
    os.system(f"echo '' | tee -a {cwd}/ocr_result_{args.type}.txt")
    os.system(f"rm -rf {args.type}_s.zip")
    os.system(f"rm -rf {args.type}_gt.zip")