names=("docx_md_unzip_test2" "readme_md_unzip_test" "arxiv_md" "table_md_unzip_test2" "image2latex" "chrome_math_md")
models=("t5-md" "vary-md" "gpt-4o-md" "nougat-md" "210")

names=("image2latex" "chrome_math_md")
models=("210")
nm="${names[*]}"

for model in "${models[@]}"
do
    echo $model
    cd /home/yilinjia/MambaOCR/eval
    for name in "${names[@]}"
    do
        python eval-md-p.py -g /home/yilinjia/MambaOCR/sampled/${name}/mds/ -p /home/yilinjia/MambaOCR/outcome/$model/${name}
    done
done