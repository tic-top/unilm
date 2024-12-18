
data="/home/yuzhongzhao/zyz/ckpts/eval"
names=("cord" "mt_sj" "gptocr2" "OpenLibrary" "LAION" "receipts" "hwfont" "gptocr4" "TMDB" "parallel_chrome_math" "parallel_docx" "parallel_sec" "parallel_web_1" "funsd" "sroie" "parallel_arxiv")


for name in "${names[@]}"
do
    result_dir=${data}/${name}/ocrs/
    echo "================================================================="
    echo "INFO: Testing task ("${name}") with prediction ("${result_dir}")"
    python eval/eval_ocr.py -d ${data} -t ${name} -p ${result_dir}
done