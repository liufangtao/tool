from PIL import Image
import os
from tqdm import tqdm

def merge_images(folder1, folder2, output_folder):
    # 获取两个文件夹中所有图片的名字
    images1 = [f for f in os.listdir(folder1) if f.endswith('.jpg')]
    images2 = [f for f in os.listdir(folder2) if f.endswith('.jpg')]

    # 找出名字相同的图片
    common_images = set(images1) & set(images2)

    # 按照纵坐标方向拼接图片
    for image_name in tqdm(common_images):
        image1 = Image.open(os.path.join(folder1, image_name))
        image2 = Image.open(os.path.join(folder2, image_name))
        width1, height1 = image1.size
        width2, height2 = image2.size
        new_image = Image.new('RGB', (max(width1, width2), height1+height2+10))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (0, 10+height1))
        new_image.save(os.path.join(output_folder, image_name))

# 使用示例
folder1='/1T/liufangtao/datas/glass_changxin/10monthdatas/1018/images'
folder2='/1T/liufangtao/ultralytics/runs/detect/changxin_test_conc'
output_folder='/1T/liufangtao/datas/glass_changxin/10monthdatas/1018/out2'
merge_images(folder1, folder2, output_folder)
