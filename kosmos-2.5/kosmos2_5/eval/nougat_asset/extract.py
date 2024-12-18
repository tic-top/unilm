import re
import os
from tqdm import tqdm

def modify_table(md):
    table_pattern = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

    table_info = []
    for match in re.finditer(table_pattern, md):
        match_text = match.group()  # 匹配到的字符串
        start_pos = match.start()  # 起始位置
        end_pos = match.end()  # 结束位置

        caption = md[end_pos:].strip().split('\n')[0]
        new_end_pos = end_pos + md[end_pos:].index(caption) + len(caption)

        table = "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"\
                + "\\begin{table}" \
                + match_text \
                + "\n\\end{table}" + "\n\\end{document}"
        table_info.append([[start_pos, new_end_pos], caption, table])
    if len(table_info) != 0:
        table_info.sort(key=lambda x:x[0][0], reverse=True)

    return table_info


num_of_files = len(os.listdir('/home/jingyechen/md_data/table_md_unzip_test2/images'))
dic = {}
for i in tqdm(range(num_of_files)):
    line = open(f'/home/jingyechen/md_data/table_md_unzip_test2/nougat_mds2/{i}.mmd').read()
    result = modify_table(line)

    


    f = open(f'/home/jingyechen/md_data/table_md_unzip_test2/temp/{i}', 'w+')

    if len(result) == 0: # no table is found
        f.close()
        continue

    item = result[0]

    if len(item) not in dic:
        dic[len(item)] = 1
    else:
        dic[len(item)] += 1


    if len(item) >= 2:
        f.write(f'{result[0][2]}') # table and caption are found
        f_caption = open(f'/home/jingyechen/md_data/table_md_unzip_test2/captions/{i}', 'w+') # store the caption to a separate file
        f_caption.write(f'{result[0][1]}')
        f_caption.close()
    else:
        f.write(f'{result[0][1]}') # only table is found, no caption
    f.close()

print(dic)