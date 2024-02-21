import cv2
import os
import shutil
from tqdm import tqdm
# 模板图像文件夹和目标图像文件夹
templates_folder = '/1T/liufangtao/datas/galss_quanmian/test/0919_pm/12line20230918/templates'  # 存放模板图像的文件夹
input_folder = '/1T/liufangtao/datas/galss_quanmian/test/0919_pm/12line20230918/T-out1'  # 存放目标图像的文件夹
output_folder = '/1T/liufangtao/datas/galss_quanmian/test/0919_pm/12line20230918/T-out1-2'  # 存放匹配结果图像的文件夹

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 加载模板图像
template_images = []
for template_name in os.listdir(templates_folder):
    if template_name.endswith('.jpg') or template_name.endswith('.png'):
        template_path = os.path.join(templates_folder, template_name)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        template_images.append(template)

# 遍历目标图像文件夹中的图像
for image_name in tqdm(os.listdir(input_folder)):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(input_folder, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        # print(image_name)
        # 遍历模板图像
        for template_index, template in enumerate(template_images):
            # 进行模板匹配

            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
            # print(result)
            if result.size !=1:
                continue
            result = result.item()
            # 设置匹配阈值
            threshold = 0.9
            
            # 找到匹配位置
            # locations = cv2.findNonZero(result >= threshold)
            if result >= threshold:
            # 在图像上标记匹配区域
            # if locations:
            #     for loc in locations:
            #         top_left = loc[0]
            #         bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            #         cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
                
                # 保存匹配结果图像到输出文件夹
                output_image_path = os.path.join(output_folder, image_name)
                try:
                    shutil.move(image_path, output_image_path)
                    # cv2.imwrite(output_image_path, image)
                    print(output_image_path)
                except FileNotFoundError:
                    continue
                
