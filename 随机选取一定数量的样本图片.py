import os, random
import shutil
from tqdm import tqdm

data_base_dir ="/1T/liufangtao/datas/glass_changxin/10monthdatas/1020-21/1020-21/out1/"  # 源图片文件夹路径

tarDir = "/1T/liufangtao/datas/glass_changxin/10monthdatas/1020-21/1020-21/out2/"  # 移动到新的文件夹路径

  
pathDir = os.listdir(data_base_dir)
filenumber = len(pathDir)

if filenumber >= 70000:
    picknumber = 20000  # 所取图片数量
    sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片
    # print(sample)
    for name in tqdm(sample):
        # print(tarDir + name)
        shutil.move(data_base_dir + name, tarDir + name)
