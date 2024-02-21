import os
import hashlib
from tqdm import tqdm
 
def get_md5(file):
    file = open(file,'rb')
    md5 = hashlib.md5(file.read())
    file.close()
    md5_values = md5.hexdigest()
    return md5_values
 
file_path = "/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/kong/images"
save_path = "/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/kong/MD5" #保存重复的图片
os.makedirs(save_path, exist_ok=True)
os.chdir(file_path)
file_list = os.listdir(file_path)

md5_list =[]
for file in tqdm(file_list):
    md5 = get_md5(file)
    if md5 not in md5_list:
        md5_list.append(md5)
    else:
        image_path = os.path.join(file_path, file)
        new_image_path = os.path.join(save_path, file)
        # os.remove(file)
        os.rename(image_path, new_image_path)