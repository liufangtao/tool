from PIL import Image
import os
from tqdm import tqdm

def concatenate_images(input_directory, output_directory):
    # 获取输入目录中的所有文件
    image_files = os.listdir(input_directory)

    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    x_offset = 0  # 用于跟踪水平位置
    current_output_image = None  # 当前的输出图像
    current_output_name = None  # 当前输出图像的名称

    # 遍历文件并按照文件名排序
    for image_file in tqdm(sorted(image_files)):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):  # 仅处理图像文件
            image_path = os.path.join(input_directory, image_file)
            small_image = Image.open(image_path)

            # 获取小图像的名称（去除文件扩展名）
            image_name = os.path.splitext(image_file)[0][:-2]

            # 如果当前输出图像为空或者已经填满了，就创建一个新的输出图像
            if current_output_image is None or image_name != current_output_name:
                if current_output_image is not None:
                    # 保存并关闭当前的输出图像
                    current_output_image.save(os.path.join(output_directory, f'{current_output_name}.jpg'))
                # 创建一个新的输出图像
                current_output_image = Image.new('RGB', (4096, 512))
                x_offset = 0
                current_output_name = image_name

            # 粘贴小图像到当前输出图像的指定位置
            current_output_image.paste(small_image, (x_offset, 0))
            x_offset += small_image.width

    # 保存最后一个输出图像
    if current_output_image is not None:
        current_output_image.save(os.path.join(output_directory, f'{current_output_name}.jpg'))



if __name__ == "__main__":
    # 输入目录中包含命名相同的512x512小图像
    input_directory = '/1T/liufangtao/ultralytics/runs/detect/baoming_glass_result'

    # 输出目录路径
    output_directory = '/1T/liufangtao/ultralytics/runs/detect/baoming_glass_resultt'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 执行拼接操作
    concatenate_images(input_directory, output_directory)