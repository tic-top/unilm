
data=$1
names=("image2latex" "chrome_math_md" "docx_md_unzip_test2" "arxiv_md" "table_md_unzip_test2" "readme_md_unzip_test")


for name in "${names[@]}"
do
    result_dir=${data}/${name}/mds/
    echo "================================================================="
    echo "INFO: Testing task ("${name}") with prediction ("${result_dir}")"
    python eval/eval_md.py -d ${data} -t ${name} -p ${result_dir}
done
