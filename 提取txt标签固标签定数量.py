import os
import random
import shutil

# 指定YOLOv5标签文件所在的目录和输出目录
label_dir = "/1T/liufangtao/datas/galss_baoming/0728/labels"  # YOLOv5标签文件目录
images_dir = "/1T/liufangtao/datas/galss_baoming/0728/images"
output_dir = "/1T/liufangtao/datas/galss_baoming/0728/2"  # 输出目录

# 指定要提取的类别
target_class = "2"

# 创建输出目录（如果不存在）

output_path = os.path.join(output_dir, 'labels')
output_imgpath = os.path.join(output_dir, 'images')
if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(output_imgpath):
    os.makedirs(output_imgpath)

# 初始化计数器
count = 0

# 获取标签文件列表
label_files = [file for file in os.listdir(label_dir) if file.endswith(".txt")]

# 打乱标签文件列表的顺序，以随机选择
random.shuffle(label_files)

# 遍历标签文件列表
for label_file in label_files:
    label_path = os.path.join(label_dir, label_file)
    image_path = os.path.join(images_dir, label_file[:-4]+ '.jpg')
    
    # 打开标签文件并逐行检查
    with open(label_path, 'r') as f:
        for line in f:
            class_name, _, _, _, _ = line.strip().split()
            
            # 如果当前行包含目标类别
            if class_name == target_class:
                # 将标签文件复制到输出目录
                output_pathfile = os.path.join(output_path, label_file)
                output_imgpathfile = os.path.join(output_imgpath, label_file[:-4]+ '.jpg')

                
                shutil.copyfile(label_path,  output_pathfile)
                shutil.copyfile(image_path, output_imgpathfile)

                
                # 增加计数器
                count += 1
                
                # 如果已经达到200个目标文件，退出循环
                if count >= 200:
                    break
                
        if count >= 200:
            break

# 输出成功提取的文件数量
print(f"Successfully extracted {count} files containing '{target_class}'.")
