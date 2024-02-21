from PIL import Image, ImageFilter
import numpy as np
import cv2


def foggy_effect(image_path, radius=10):
    # 打开图像
    image = Image.open(image_path)
    # 应用高斯模糊
    foggy_image = image.filter(ImageFilter.GaussianBlur(radius))
    return foggy_image





def add_gaussian_noise_to_image(image_path, output_path, mean=0, std_dev=30):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not open or find the image.")
        return

    # 生成高斯噪声
    gaussian_noise = np.random.normal(mean, std_dev, (image.shape[0], image.shape[1], image.shape[2])).astype(np.uint8)

    # 将噪声添加到图像上
    noisy_image = image + gaussian_noise

    # 确保像素值在0-255范围内
    noisy_image = np.clip(noisy_image, 0, 255)

    # 保存添加噪声后的图像
    cv2.imwrite(output_path, noisy_image)

    print(f"Image with Gaussian noise saved to {output_path}")




def shift_image(image_path, output_path, shift_amount, fill_color=(1, 1, 1)):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not open or find the image.")
        return

    # 获取图像尺寸
    height, width, channels = image.shape

    # 创建一个与原图像相同尺寸的白色背景
    shifted_image = np.full((height, width, channels), fill_color, dtype=np.uint8)

    # 计算位移后的坐标
    new_x = shift_amount
    if new_x >= 0:
        # 向右移动
        shifted_image[:, new_x:] = image[:, :width - new_x]
    else:
        # 向左移动
        shifted_image[:, :width+new_x] = image[:, -new_x:]
        # shifted_image[:, new_x:] = image[:, -new_x:]

    # 保存位移后的图像
    cv2.imwrite(output_path, shifted_image)

    print(f"Shifted image saved to {output_path}")

# 使用示例
# image_path = 'path_to_your_image.jpg'  # 替换为你的图片路径
#  # 输出图片的路径
# shift_amount = 50  # 水平位移量


# 加载图像
# original_image = Image.open(r'C:\Users\Admin\Pictures\xy\20231122081343_a2f76a0fd5c7ccb8e528ed4848dfebd8.jpg')
image_path = r'C:\Users\Admin\Pictures\xy\20231122081343_a2f76a0fd5c7ccb8e528ed4848dfebd8.jpg'
# 应用雾化效果
# foggy_image = foggy_effect(original_image, radius=10)

# 添加高斯噪声
# 使用示例

# output_path = 'noisy_image.jpg'  # 输出图片的路径
# add_gaussian_noise_to_image(image_path, output_path)

# 水平位移
output_path = 'shifted_image.jpg' 
shift_image(image_path, output_path, -300)

# 保存或显示结果
# foggy_image.save('foggy_image.jpg')
# noisy_image.save('noisy_image.jpg')
# shifted_image.save('shifted_image.jpg')



