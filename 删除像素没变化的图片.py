# -*- coding: utf-8 -*-
"""
@author: liufangtao
@software: VScode
@file: json2xml.py
@function: json2xml
@create_time: 2023/10/24
"""

import cv2
import os
import numpy as np
from PIL import Image
from tqdm import tqdm


def is_blackish(image_path, threshold=50):
    """
    判断图片是否看起来是黑色的函数。
    Args:
        image_path (str): 图片文件路径。
        threshold (int): 阈值，用于判断是否为黑色。较小的值表示更严格的判断。
    
    Returns:
        bool: 如果图片看起来是黑色的，则返回True，否则返回False。
    """
    img = Image.open(image_path).convert("L")
    width, height = img.size
    pixels = img.getdata()
    
    black_pixel_count = 0
    for pixel in pixels:
        r = pixel
        if r <= threshold: # and g <= threshold and b <= threshold:
            black_pixel_count += 1
    
    # 根据黑色像素数量和图片总像素数量的比例来判断
    black_ratio = black_pixel_count / (width * height)
    return  black_ratio >= 0.05  # 如果黑色像素比例达到90%以上，则判断为黑色图片

# def calculate_white_pixel_ratio(image_path):
#     image = Image.open(image_path)
#     # Convert the image to grayscale
#     grayscale_image = image.convert('L')
    
#     # Convert grayscale image to binary (black and white)
#     binary_image = grayscale_image.point(lambda p: p > 200 and 255)  # 
    
#     # Calculate the ratio of white pixels
#     total_pixels = image.width * image.height
#     white_pixels = sum(1 for pixel in binary_image.getdata() if pixel == 255)
#     white_pixel_ratio = white_pixels / total_pixels
    
#     return white_pixel_ratio >= 0.01
def is_whiteish(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to the LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into L, A, and B channels
    l_channel, _, _ = cv2.split(lab_image)
    
    # Calculate the percentage of pixels that have L values above a certain threshold
    white_pixel_ratio = np.sum(l_channel > 200) / l_channel.size
    
    return white_pixel_ratio >= 0.02

def is_colorful_image(image_path, threshold=25):
    # 读取图片
    image = cv2.imread(image_path)

    # 将图片转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算灰度图像的标准差
    std_dev = np.std(gray_image)

    # 判断是否为彩色图片，如果标准差小于设定的阈值，则认为是没有颜色变化的图片
    return std_dev >= threshold

def batch_delete_colorless_images(folder_path, out_path, threshold=10):
    folder_dir = os.listdir(folder_path)
    for filename in tqdm(folder_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(filename)
            image_path = os.path.join(folder_path, filename)
            new_image_path = os.path.join(out_path, filename)
            # if is_blackish(image_path):# 黑色图片过滤
            if is_whiteish(image_path):  #白色图片过滤
            # if not is_colorful_image(image_path, threshold):
                # os.remove(image_path)
                os.rename(image_path, new_image_path)
                print(f"Deleted colorless image: {image_path}")

if __name__ == "__main__":
    # 设置图片文件夹路径
    image_folder = "/1T/liufangtao/datas/glass_changxin/11monthdatas/1206/1701843253378/out1"
    out_path = "/1T/liufangtao/datas/glass_changxin/11monthdatas/1206/1701843253378/out2"
    os.makedirs(out_path, exist_ok=True)
    # 批量删除没有颜色变化的图片
    batch_delete_colorless_images(image_folder, out_path)
    
