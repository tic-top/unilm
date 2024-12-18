basename="/home/yilinjia/MambaOCR/outcome/"
# outcome_names=("vary-ocr" "gpt-4o-normalized-fix" "gpt-4o-raw" "google" "nougat-ocr" "trocr" "210" "2-rel2-200k")
outcome_names=($1)
for outcome_name in "${outcome_names[@]}"
do
    echo ${outcome_name}
    # python ~/MambaOCR/postprocess.py -i $outcome_name -o $outcome_name
    outcome="${basename}${outcome_name}"
    cd /home/yilinjia/MambaOCR/eval/ocr_eval
    rm -rf ${outcome}/result.txt
    names=($(ls ${outcome}))
    # names=("LAION")
    for name in "${names[@]}"
    do
        rm -rf ${name}_s.zip
        rm -rf ${name}_gt.zip
        zip -rj -q ${name}_s.zip ${outcome}/${name}
        zip -rj -q ${name}_gt.zip /home/yilinjia/MambaOCR/sampled/${name}/ocrs
        # zip -rj -q ${name}_gt.zip ${basename}210/${name} #/home/yilinjia/MambaOCR/sampled/${name}/ocrs
        echo ${name} | tee -a ${outcome}/result.txt
        python script.py -g="${name}_gt.zip" -s="${name}_s.zip" | tee -a "${outcome}/result.txt"
        echo "" | tee -a "${outcome}/result.txt"
    done
done