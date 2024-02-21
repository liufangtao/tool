# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
from tqdm import tqdm
import re

def line_detect_possible_demo(image, file, save_path):  # 检测出可能的线段
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 100, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=40, maxLineGap=5)
    """
    HoughLinesP概率霍夫变换（是加强版）使用简单，效果更好，检测图像中分段的直线（而不是贯穿整个图像的直线)
    第一个参数是需要处理的原图像，该图像必须为cannay边缘检测后的图像；
    第二和第三参数：步长为1的半径和步长为π/180的角来搜索所有可能的直线
    第四个参数是阈值，概念同霍夫变换
    第五个参数：minLineLength-线的最短长度，比这个线短的都会被忽略。
    第六个参数：maxLineGap-两条线之间的最大间隔，如果小于此值，这两条线就会被看成一条线
    """
    xlist = []
    for line in lines:
        #   print(type(line))
        x1, y1, x2, y2 = line[0]
        xlist.append(x1)
    left = r'(XD|YR)'
    result1 = re.search(left, file)
    if result1:
    # x1 = min(xlist)
        x1 = max(xlist)
    # cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cropped = image[0:image.shape[0], x1-590:x1+50]
        # cv2.imwrite(os.path.join(save_path,file), cropped)

        sub_images = batch_crop_Yimages(cropped, (640,640), overlap=18) #M10边缘上下重叠18
        for i, sub_img in enumerate(sub_images):
            if is_colorful_image(sub_img, threshold=15):  # 单色图片过滤
                cv2.imwrite(os.path.join(save_path, f"{os.path.splitext(file)[0]}_{i}.jpg"), sub_img)

    right = r'(YL|XU)'
    result2 = re.search(right, file)
    if result2:
        x1 = min(xlist)
    # cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cropped = image[0:image.shape[0], x1-50:x1+590]  #x1-50:x1+590
        # cv2.imwrite(os.path.join(save_path,file), cropped)


        sub_images = batch_crop_Yimages(cropped, (640,640), overlap=18) #M10边缘上下重叠18
        for i, sub_img in enumerate(sub_images):
            if is_colorful_image(sub_img, threshold=15):  # 单色图片过滤
                cv2.imwrite(os.path.join(save_path, f"{os.path.splitext(file)[0]}_{i}.jpg"), sub_img)

        
    # cv2.imshow("line_detect_possible_demo", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
def is_colorful_image(image, threshold=25):
    # 读取图片
    # image = cv2.imread(image_path)

    # 将图片转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算灰度图像的标准差
    std_dev = np.std(gray_image)

    # 判断是否为彩色图片，如果标准差小于设定的阈值，则认为是没有颜色变化的图片
    return std_dev >= threshold
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
def batch_split_images(image_dir, save_dir,size):
    images_dir = os.listdir(image_dir)
    for filename in tqdm(images_dir):
        if filename.endswith(".jpg" ):
            img_path = os.path.join(image_dir, filename)
            img = cv2.imread(img_path)
            
            
            sub_images = batch_crop_Yimages(img, size, overlap=50) #M10边缘上下重叠18
            for i, sub_img in enumerate(sub_images):
                if is_colorful_image(sub_img, threshold=15):  # 单色图片过滤
                    cv2.imwrite(os.path.join(save_dir, f"{os.path.splitext(filename)[0]}_{i}.jpg"), sub_img)
path = r'/1T/liufangtao/datas/glass/test/20240205'
img_path = os.path.join(path,'out0')
save_path = os.path.join(path,'out1')
os.makedirs(save_path , exist_ok=True)
file_list=os.listdir(img_path)
for file in tqdm(file_list):
    image = cv2.imread(os.path.join(img_path, file))
    print(file)
    line_detect_possible_demo(image, file, save_path)
# path1 = save_path
# save_dir = os.path.join(path,'out2')
# os.makedirs(save_dir, exist_ok=True)
# batch_split_images(path1, save_dir,(512,640))