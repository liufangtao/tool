import cv2
import numpy as np
import os

# 遍历图像文件夹
input_folder = '/1T/liufangtao/datas/glass_changxin/10monthdatas/kong/images'
output_folder = '/1T/liufangtao/datas/glass_changxin/10monthdatas/kong/mask-7-25-2'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        # 加载图像
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (5,5), 0)  # 高斯模糊去除一些噪声，酌情加减
        _, binary = cv2.threshold(gray, 190,255, cv2.THRESH_TOZERO_INV)  #c侧205，255 T侧190，255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7)) #C侧(7,7)MORPH_ELLIPSE  MORPH_RECT

        closed_image = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        kernel = np.ones((7,7), np.uint8)
        eroded = cv2.erode(closed_image, kernel, iterations=25) #C侧30 T侧50

        result_image = image.copy()
        result_image[eroded == 0] = [0,0,0]

        # 保存结果图像
        output_path = os.path.join(output_folder, filename)
        print(output_path)
        cv2.imwrite(output_path, result_image)

# #include <iostream>
# #include <opencv2/opencv.hpp>
# #include <filesystem>

# namespace fs = std::filesystem;

# int main() {
#     std::string input_folder = "/1T/liufangtao/datas/glass_changxin/10monthdatas/kong/white";
#     std::string output_folder = "/1T/liufangtao/datas/glass_changxin/10monthdatas/kong/mask-7-25";

#     if (!fs::exists(output_folder)) {
#         fs::create_directory(output_folder);
#     }

#     for (const auto& entry : fs::directory_iterator(input_folder)) {
#         if (entry.path().extension() == ".jpg") {
#             // 加载图像
#             cv::Mat image = cv::imread(entry.path().string());
#             cv::Mat gray, blurred, binary, closed_image, eroded, result_image;

#             cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
#             cv::GaussianBlur(gray, blurred, cv::Size(5, 5), 0);
#             cv::threshold(blurred, binary, 190, 255, cv::THRESH_TOZERO_INV);

#             cv::Mat kernel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(7, 7));
#             cv::morphologyEx(binary, closed_image, cv::MORPH_CLOSE, kernel);

#             kernel = cv::Mat::ones(7, 7, CV_8U);
#             cv::erode(closed_image, eroded, kernel, cv::Point(-1, -1), 25);

#             result_image = image.clone();
#             result_image[eroded == 0] = cv::Scalar(0, 0, 0);

#             // 保存结果图像
#             std::string output_path = output_folder + "/" + entry.path().filename().string();
#             std::cout << output_path << std::endl;
#             cv::imwrite(output_path, result_image);
#         }
#     }

#     return 0;
# }


# import cv2
# import os
# import numpy as np

# # 读取文件夹中的所有图片
# folder_path = '/1T/liufangtao/datas/glass_changxin/10monthdatas/负样本/out0'
# images = [cv2.imread(os.path.join(folder_path, img)) for img in os.listdir(folder_path) if img.endswith('.jpg') or img.endswith('.png')]

# # 创建一个新的文件夹来保存处理后的图片
# output_folder = '/1T/liufangtao/datas/glass_changxin/10monthdatas/负样本/out0-mask1'
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # 对每张图片进行处理
# for i, img in enumerate(images):
#     # 将图片转换为灰度图
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # 对灰度图进行二值化处理
#     ret, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_TOZERO_INV)  #cv2.THRESH_TOZERO_INV

#     # 找到二值化图像中的白色区域，并将这些区域的边缘平滑
#     kernel = np.ones((5,5),np.uint8)
#     dilation = cv2.dilate(binary,kernel,iterations = 1)

#     # 将处理后的图像保存到新的文件夹
#     cv2.imwrite(os.path.join(output_folder, f'processed_{i}.jpg'), dilation)
