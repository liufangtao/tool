import os
import shutil
from tqdm import tqdm

def add_folder_name_to_files(target_folder):
    for root, dirs, files in os.walk(target_folder):
        for file in tqdm(files):
            old_file_path = os.path.join(root, file)
            classes = root.split('/')[-2]
            new_file_name = os.path.basename(root) + '_' +classes+'_'+ file
            new_path, _ = os.path.split(root)
            new_paths = os.path.join(new_path,'images')
            os.makedirs(new_paths , exist_ok=True)
            new_file_path = os.path.join(new_paths, new_file_name)
            shutil.copy(old_file_path, new_file_path)

folder = '/1T/liufangtao/datas/glass/test/1204/缺陷数据1204'
lists = ['bali','crack','broken','chiping']
for list in lists:
    target_folder = os.path.join(folder, list)
    add_folder_name_to_files(target_folder)

