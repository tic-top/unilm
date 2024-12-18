zip -rj funsd_gt.zip ~/mycontainer/tengchao/dataset/kosmos_d/ft_ocr/funsd/ocrs/
zip -rj cord_gt.zip ~/mycontainer/tengchao/dataset/kosmos_d/ft_ocr/cord/ocrs/
zip -rj sroie_gt.zip ~/mycontainer/tengchao/dataset/kosmos_d/ft_ocr/sroie/ocrs/


zip -rj cord_s.zip /home/yilinjia/MambaOCR/result/cord/pred
zip -rj sroie_s.zip /home/yilinjia/MambaOCR/result/sroie/pred
zip -rj sroi2e_s.zip /home/yilinjia/MambaOCR/result/sroie2/pred

python script.py -g=cord_gt.zip -s=cord_s.zip
python script.py -g=cord_gt.zip -s=cord_gt.zip
python script.py -g=sroie_gt.zip -s=sroie_s.zip
python script.py -g=sroie_gt.zip -s=sroie_gt.zip
python script.py -g=funsd_gt.zip -s=funsd_s.zip
python script.py -g=funsd_gt.zip -s=funsd_gt.zip
python script.py -g=sroie_gt.zip -s=sroie2_s.zip

find ~/MambaOCR/result/sroie2/pred -type f -name "*.txt" -exec truncate -s 0 {} \;


funsd {"precision": 0.9998170843241265, "recall": 0.9997713658603503, "hmean": 0.9997942245695863}

cord {"precision": 0.9992329719779096, "recall": 0.9990286298568507, "hmean": 0.9991307904693731}

sroie {"precision": 0.9999730563526384, "recall": 0.9999730563526384, "hmean": 0.9999730563526384}

mt_sj


{"precision": 0.8983674056493518, "recall": 0.8730626081182618, "hmean": 0.885534267940379}
parallel_chrome_math
{"precision": 0.9510934393638171, "recall": 0.9510934393638171, "hmean": 0.9510934393638171}
parallel_docx
{"precision": 0.95146959431614, "recall": 0.9335867367569753, "hmean": 0.9424433413885442}
parallel_sec
{"precision": 0.9697826271306216, "recall": 0.9623697387060127, "hmean": 0.9660619627885367}
parallel_web_1
{"precision": 0.3277992990223206, "recall": 0.30008376001405007, "hmean": 0.3133298303399196}


| Dataset | Precision              | Recall                | Hmean                 |
|---------|------------------------|-----------------------|-----------------------|
| FUNSD   | 0.9998170843241265     | 0.9997713658603503    | 0.9997942245695863    |
| CORD    | 0.9992329719779096     | 0.9990286298568507    | 0.9991307904693731    |
| SROIE   | 0.9999730563526384     | 0.9999730563526384    | 0.9999730563526384    |
