import os
from tqdm import tqdm

files = os.listdir('/home/jingyechen/md_data/table_md_unzip_test2/temp2')

for file in files:

    name = file.split('.')[0]

    line = open(f'/home/jingyechen/md_data/table_md_unzip_test2/temp2/{name}.md').read()
    try:
        caption = open(f'/home/jingyechen/md_data/table_md_unzip_test2/captions/{name}').read()
    except:
        caption = ''

    f = open(f'/home/jingyechen/md_data/table_md_unzip_test2/temp3/{name}.md', 'w+')
    f.write(f'{line}\n{caption}')
    f.close()