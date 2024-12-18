import os
from tqdm import tqdm
files = os.listdir('/home/jingyechen/md_data/table_md_unzip_test2/temp')

for file in tqdm(files):
    os.system(f'pandoc --from latex --to markdown_github --standalone --no-highlight -o /home/jingyechen/md_data/table_md_unzip_test2/temp2/{file}.md /home/jingyechen/md_data/table_md_unzip_test2/temp/{file}')




