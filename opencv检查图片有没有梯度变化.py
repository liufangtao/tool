import cv2
import os

def has_gradient(image_path, threshold=18.558):
    # 读取图像  缺省threshold=19
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 计算图像的梯度
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)

    # 判断梯度是否小于阈值
    if cv2.mean(gradient_magnitude)[0] < threshold:
        return True  # 梯度小于阈值，没有梯度变化
    else:
        return False  # 梯度大于阈值，有梯度变化

def main():
    input_folder = "/1T/liufangtao/datas/glass/0802/out4"  # 输入文件夹
    output_folder = "/1T/liufangtao/datas/glass/0802/out1"  # 输出文件夹
    output1_folder = "/1T/liufangtao/datas/glass/0802/out5"  # 输出删除文件夹
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的图像文件
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(input_folder, filename)

            # 检查图像是否没有梯度变化
            if has_gradient(image_path):
                # 删除没有梯度变化的图像
                # os.remove(image_path)
                new1_image_path = os.path.join(output1_folder, filename)
                os.rename(image_path, new1_image_path)
                print(f"已删除图像：{filename}")
            else:
                # 移动有梯度变化的图像到输出文件夹
                new_image_path = os.path.join(output_folder, filename)
                # os.rename(image_path, new_image_path)
                print(f"已移动图像：{filename}")

if __name__ == "__main__":
    main()
