import cv2
import os
from pathlib import Path
from PIL import Image 
from tqdm import tqdm
import numpy as np
from concurrent.futures import ThreadPoolExecutor

Image.MAX_IMAGE_PIXELS = 1000000000

def is_blackish(image, threshold=50):

    # 将图片转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_pixels = np.sum(gray_image <= threshold)
    total_pixels = gray_image.size
    black_ratio = black_pixels / total_pixels

    return black_ratio >= 0.9  # 如果黑色像素比例达到90%以上，则判断为黑色图片


def split_image(img, size, overlap=10):
    height, width = img.shape[:2]
    sub_width, sub_height = size
    cols = (width - sub_width) // (sub_width - overlap) + 1
    # rows = height // sub_height
    rows = (height - sub_height) // (sub_height - overlap) + 1
    sub_images = []
    for row in range(rows):
        for col in range(cols):
            x0 = col * (sub_width - overlap)
            y0 = row * (sub_height - overlap)
            x1 = x0 + sub_width
            y1 = y0 + sub_height
            sub_images.append(img[y0:y1, x0:x1])
    return sub_images

def split_imageY(img, size):
    height, width = img.shape[:2]
    sub_width, sub_height = size
    # cols = width // sub_width
    cols = width
    rows = height // sub_height
    sub_images = []
    for row in range(rows):
        # for col in range(cols):
        #     x0 = col * sub_width
        x0 = 0
        y0 = row * sub_height
        x1 = x0 + width
        y1 = y0 + sub_height
        sub_images.append(img[y0:y1, x0:x1])
    return sub_images
def split_imageX(img, size):
    height, width = img.shape[:2]
    sub_width, sub_height = size
    cols = width // sub_width
    # cols = width
    # rows = height // sub_height
    rows = height
    sub_images = []
    for col in range(cols):
        # for col in range(cols):
        #     x0 = col * sub_width
        x0 = col * sub_width
        y0 = 0
        x1 = x0 + sub_width
        y1 = y0 + height
        sub_images.append(img[y0:y1, x0:x1])
    return sub_images

def batch_crop_Yimages(img, size, overlap=18):  #M10边缘上下重叠18
    
    # 获取原始图片的宽度和高度
    height, width = img.shape[:2]
    sub_width, sub_height = size
    # 计算切割行数，每次向下移动size-overlap像素
    num_crops = (height - sub_height) // (sub_height - overlap) + 1
    sub_images = []
    for i in range(num_crops):
        # 计算切割的起始纵坐标和结束纵坐标
        x0 = 0
        y0 = i * (sub_height - overlap)
        x1 = x0 + width
        y1 = y0 + sub_height
        sub_images.append(img[y0:y1, x0:x1])
        # 切割图像并保存
    return sub_images

def batch_crop_Ximages(img, size, overlap=64):

    # 获取原始图片的宽度和高度
    height, width = img.shape[:2]
    sub_width, sub_height = size
    # 计算切割行数，每次向下移动size-overlap像素
    num_crops = (width - sub_width) // (sub_width - overlap) + 1
    sub_images = []
    for i in range(num_crops):
        # 计算切割的起始纵坐标和结束纵坐标
        x0 = i * (sub_height - overlap)
        y0 = 0
        x1 = x0 + sub_width
        y1 = y0 + height
        sub_images.append(img[y0:y1, x0:x1])
        # 切割图像并保存
    return sub_images     
def is_colorful_image(image, threshold=25):
    # 读取图片
    # image = cv2.imread(image_path)

    # 将图片转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算灰度图像的标准差
    std_dev = np.std(gray_image)

    # 判断是否为彩色图片，如果标准差小于设定的阈值，则认为是没有颜色变化的图片
    return std_dev >= threshold
def batch_split_images(image_dir, save_dir,size):
    images_dir = os.listdir(image_dir)
    
    for filename in tqdm(images_dir):
        if filename.endswith(".jpg") or filename.endswith(".bmp"):
            img_path = os.path.join(image_dir, filename)
            # img_path = Path(img_path)
            # img_path = str(img_path).encode('gbk')
            img = cv2.imread(img_path)
            
            sub_images = split_image(img, size,overlap=14) #,overlap=14
            
            # sub_images = batch_crop_Yimages(img, size, overlap=18) #M10边缘上下重叠18
            for i, sub_img in enumerate(sub_images):
                # print(filename)
                if not is_blackish(sub_img):# 黑色图片过滤
                # if is_colorful_image(sub_img, threshold=15):  # 单色图片过滤
                    cv2.imwrite(os.path.join(save_dir, f"{os.path.splitext(filename)[0]}_{i}.jpg"), sub_img)
    
        
                # sub_img.save(r'Z:\华星M10项目\7-26数据\7.26\20230726\out\\'+f"{os.path.splitext(filename)[0]}_{i}.png" )


path = '/1T/liufangtao/datas/glass_quanmian/test/20240205/images'
save_dir = '/1T/liufangtao/datas/glass_quanmian/test/20240205/out0'
os.makedirs(save_dir, exist_ok=True)
with ThreadPoolExecutor() as executor:
# executor.submit(split_imageY, img, size)
    executor.submit(batch_split_images,path, save_dir,(512,512))


# file_list=os.listdir(path)
# for file in file_list:
#     print(file)
#     img = cv2.imread(path+file)
#     sub_images = split_image(img, (2800, 2800))
#     # print(sub_images)
#     for i, sub_img in enumerate(sub_images):
#         cv2.imwrite(f"D:\datas\liu\glasses\bianyuan\out0\sub_image_{i}.jpg", sub_img)
