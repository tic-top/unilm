name="mt_js"
cd /home/yilinjia/MambaOCR/eval/ocr_eval
zip -rj ${name}_s.zip /home/yilinjia/MambaOCR/result/${name}/pred
zip -rj ${name}_gt.zip /home/yilinjia/MambaOCR/sampled/${name}/ocr
python script.py -g=${name}.zip -s=${name}_gt.zip
cd /home/yilinjia/MambaOCR/