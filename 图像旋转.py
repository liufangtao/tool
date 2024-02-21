import os
import cv2
import numpy as np
from xml.etree import ElementTree as ET

def rotate_with_padding(image, angle_degrees, bg_color):
    # 与前面的代码相同，定义旋转并填充的函数

# 设置输入和输出文件夹
input_images_folder = 'input_images'
input_annotations_folder = 'input_annotations'
output_images_folder = 'output_images'
output_annotations_folder = 'output_annotations'
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_annotations_folder, exist_ok=True)

# 定义背景色为白色 (255, 255, 255)
background_color = (255, 255, 255)

# 获取输入文件夹中的图像文件列表
image_files = os.listdir(input_images_folder)

for image_file in image_files:
    # 读取图像
    image_path = os.path.join(input_images_folder, image_file)
    image = cv2.imread(image_path)
    
    # 读取相应的标签文件（假设标签是使用Pascal VOC XML格式存储）
    annotation_file = image_file.replace('.jpg', '.xml')
    annotation_path = os.path.join(input_annotations_folder, annotation_file)
    
    # 解析标签文件
    tree = ET.parse(annotation_path)
    root = tree.getroot()

    # 进行旋转并填充
    rotated_image = rotate_with_padding(image, 30, background_color)

    # 保存旋转后的图像
    output_image_path = os.path.join(output_images_folder, image_file)
    cv2.imwrite(output_image_path, rotated_image)
    
    # 更新标签中的坐标信息
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        
        # 旋转标签框的坐标
        # 这里需要根据旋转矩阵计算新的坐标值
        # ...
        
        # 更新旋转后的坐标信息
        bbox.find('xmin').text = str(new_xmin)
        bbox.find('ymin').text = str(new_ymin)
        bbox.find('xmax').text = str(new_xmax)
        bbox.find('ymax').text = str(new_ymax)
    
    # 保存更新后的标签文件
    output_annotation_path = os.path.join(output_annotations_folder, annotation_file)
    tree.write(output_annotation_path)
