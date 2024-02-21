import os
import pandas as pd
import shutil
from tqdm import tqdm
import sys
from importlib.resources import path
import yaml
# 遍历文件夹
def walk_dir(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv'):
                yield os.path.join(root, file)

# 读取CSV文件
def read_csv(file_path):
    return pd.read_csv(file_path)

# 查找字符串
def find_string(df, string):
    return df[df.apply(lambda row: row.astype(str).str.contains(string).any(), axis=1)]

# 拷贝文件
def copy_file(src, dst):
    shutil.copy(src, dst)

def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config



# 主函数
def main():
    config = read_config('config.yaml')
    data_dir = config['paths']['data_dir']
    log_dir = config['paths']['input_strings']
    path = data_dir
    # path = '/1T/liufangtao/datas/glass_changxin/11monthdatas/1115'
    # path_lists = ['2023_11_15','2023_11_14']
    path_lists = log_dir
    for path_list in path_lists:

        src_dir = os.path.join(path,path_list)
        dst_dir = os.path.join(path,path_list+'out0')
        string = 'zangwu' or 'huashang'
        os.makedirs(dst_dir , exist_ok=True)

        for csv_file in tqdm(walk_dir(src_dir)):
            df = read_csv(csv_file)
            matched_rows = find_string(df, string)
            if not matched_rows.empty:
                jpg_file = os.path.splitext(csv_file)[0] + '.jpg'
                copy_file(jpg_file, dst_dir)

if __name__ == '__main__':
    main()
