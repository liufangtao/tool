import os
import shutil
import cv2
import numpy as np
from tqdm import tqdm
import datetime
import schedule
import time

def is_blackish(image, threshold=50):

    # 将图片转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_pixels = np.sum(gray_image <= threshold)
    total_pixels = gray_image.size
    black_ratio = black_pixels / total_pixels

    return black_ratio >= 0.9  # 如果黑色像素比例达到90%以上，则判断为黑色图片

def job (img_dir):
    img_list = os.listdir(img_dir)
    # new_file_name = os.path.basename(root)
    for img_name in tqdm(img_list):
        if img_name.endswith('.jpg'):
            part = img_name.split('-')[1]
            img_path = os.path.join(img_dir, img_name)
            img = cv2.imread(img_path)
            if not is_blackish(img):

                if part == '0':
                    new_path1 = os.path.join(img_dir, part )
                    if not os.path.exists(new_path1):
                        os.makedirs(new_path1)
                    new_path1 = os.path.join(new_path1,img_name)
                    shutil.move(img_path,new_path1)
                elif part == '1':
                    new_path2 = os.path.join(img_dir, part)
                    if not os.path.exists(new_path2):
                        os.makedirs(new_path2)
                    new_path2 = os.path.join(new_path2,img_name)
                    shutil.move(img_path,new_path2)
                elif part == '2':
                    new_path3 = os.path.join(img_dir, part)
                    if not os.path.exists(new_path3):
                        os.makedirs(new_path3)
                    new_path3 = os.path.join(new_path3,img_name)
                    shutil.move(img_path,new_path3)
                elif part == '3':
                    new_path4 = os.path.join(img_dir, part)
                    if not os.path.exists(new_path4):
                        os.makedirs(new_path4)
                    new_path4 = os.path.join(new_path4,img_name)
                    shutil.move(img_path,new_path4)
                elif part == '4':
                    new_path5 = os.path.join(img_dir, part)
                    if not os.path.exists(new_path5):
                        os.makedirs(new_path5)
                    new_path5 = os.path.join(new_path5,img_name)
                    shutil.move(img_path,new_path5)
            else:
                try:
                    os.remove(img_path)
                except:
                    pass
if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
  
    dir = r'/1T/liufangtao/datas/glass_changxin/1monthdatas/0103'
    img_dir = os.path.join(dir, '2024-01-03', 'defect_image')
    job(img_dir)

    # schedule.every(24).hours.do(job, img_dir)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    
        
