import cv2

from PIL import Image

# 读取图像
image_path = '/1T/liufangtao/datas/galss_quanmian/test/0913/out2/origin-cam2-20230912141125136586_2_29.jpg'
image = Image.open(image_path)

# 转换为灰度图像
gray_image = image.convert('L')

# 获取图像的灰度像素值
pixel_values = list(gray_image.getdata())

# 获取图像的高度和宽度
height, width = gray_image.size

# 定义保存像素值的txt文件路径
output_txt_path = 'pixel_data.txt'

# 打开txt文件以写入模式
with open(output_txt_path, 'w') as txt_file:
    # 遍历图像的每一行
    for i in range(height):
        # 遍历每一行的每一列
        for j in range(width):
            # 获取当前像素值
            pixel_value = pixel_values[i * width + j]
            # 将像素值写入txt文件
            txt_file.write(f'{pixel_value}\t')
        # 写入换行符
        txt_file.write('\n')


# # 加载图像
# image = cv2.imread('/1T/liufangtao/datas/galss_quanmian/test/0913/out2/origin-cam2-20230912141125136586_2_27.jpg')

# # 检查是否成功加载图像
# if image is not None:
#     # 获取图像的高度和宽度
#     height, width, _ = image.shape
#     with open ('pixel_values.txt', 'w') as txt_file:

#         # 访问图像的像素值
#         for y in range(height):
#             for x in range(width):
#                 # 获取像素值 (B, G, R)
#                 pixel = image[y, x]
#                 blue, green, red = pixel

#                 # 在这里可以对像素值进行处理，例如输出到控制台
#                 txt_file.write(f'Pixel at ({x}, {y}): R={red}, G={green}, B={blue}\n')
# else:
#     print('无法加载图像。')

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# # 读取图像
# image = mpimg.imread('/1T/liufangtao/datas/galss_quanmian/test/0913/out2/origin-cam2-20230912141125136586_2_27.jpg')

# # 创建一个新的图形窗口
# plt.figure(figsize=(image.shape[1]/100.0, image.shape[0]/100.0), dpi=100)

# output_txt_path = 'pixel_data.txt'
# with open(output_txt_path, 'w') as txt_file:
#     height, width, _ = image.shape
    
#     for j in range(width):
#         for i in range(height):
#             pixel_value = image[j, i]
#             txt_file.write(f'Pixel ({j}, {i}): {pixel_value}\n')

# # 显示图像
# plt.imshow(image)
# plt.axis('off')  # 关闭坐标轴
# plt.show()

