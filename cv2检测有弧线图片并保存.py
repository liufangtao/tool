'''
import cv2
import os
import numpy as np

# Input and output directories
input_dir = 'input_images'
output_dir = 'output_images'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through images in the input directory
for image_name in os.listdir(input_dir):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(input_dir, image_name)
        
        # Load the image
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        
        # Apply Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=200,
            param2=30,
            minRadius=10,
            maxRadius=100
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            for circle in circles[0, :]:
                # Draw the circle
                center = (circle[0], circle[1])
                radius = circle[2]
                cv2.circle(image, center, radius, (0, 255, 0), 2)
        
        # Save the processed image to the output directory
        output_image_path = os.path.join(output_dir, image_name)
        cv2.imwrite(output_image_path, image)
'''
##################################################################################
import cv2
import os
import numpy as np

# 输入和输出文件夹
input_dir = '/1T/liufangtao/datas/glass/0731/out0/all_tile_650bat/imghu'  # 输入图像所在文件夹
output_dir = '/1T/liufangtao/datas/glass/0731/out0/all_tile_650bat/imghuout'  # 输出检测结果图像的文件夹

# 如果输出文件夹不存在，则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历输入文件夹中的图像
for image_name in os.listdir(input_dir):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(input_dir, image_name)
        
        # 加载图像
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        # 将图像转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 应用 Canny 边缘检测
        edges = cv2.Canny(gray, threshold1=100, threshold2=300)
        
        # 在边缘图像中找到轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 遍历检测到的轮廓
        for contour in contours:
            # 将轮廓逼近为多边形
            epsilon = 0.05 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # 判断轮廓是否是弧线（曲线的一部分）
            if  len(approx) >= 3:
                # 在原始图像上绘制检测到的弧线
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        
        # 将带有检测到的弧线的图像保存到输出文件夹
        output_image_path = os.path.join(output_dir, image_name)
        print(image_name)
        cv2.imwrite(output_image_path, image)
