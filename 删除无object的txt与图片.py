import os
import shutil

def move_empty_files(image_folder, label_folder, destination_folder):
    for filename in os.listdir(label_folder):
        if filename.endswith(".txt"):
            label_file_path = os.path.join(label_folder, filename)
            image_file_path = os.path.join(image_folder, f"{os.path.splitext(filename)[0]}.jpg")
            
            # 检查是否存在对应的图片文件
            if os.path.exists(image_file_path) and os.path.getsize(label_file_path) == 0:
                # 移动空的txt文件
                shutil.move(label_file_path, os.path.join(destination_folder, filename))
                
                # 移动对应的图片文件
                shutil.move(image_file_path, os.path.join(destination_folder, f"{os.path.splitext(filename)[0]}.jpg"))

# 示例调用
image_folder = '/1T/liufangtao/datas/glass_changxin/train_val/images'  # 图片文件夹路径
label_folder = '/1T/liufangtao/datas/glass_changxin/train_val/labels'  # 标签文件夹路径
destination_folder = '/1T/liufangtao/datas/glass_changxin/train_val/kong'  # 目标文件夹路径
os.makedirs(destination_folder, exist_ok=True)
move_empty_files(image_folder, label_folder, destination_folder)
