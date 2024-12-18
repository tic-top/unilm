import os

files = os.listdir('/home/jingyechen/md_data/table_md_unzip_test2/pdfs')
data = [f'/home/jingyechen/md_data/table_md_unzip_test2/pdfs/{i}' for i in files]
data_str = ' '.join(data)

# use batch size 8 for inference
os.system(f'nougat {data_str} -o /home/jingyechen/md_data/table_md_unzip_test2/nougat_mds2 --markdown --batchsize 8')


