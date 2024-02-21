import os
import re

# 定义一个正则表达式，用于匹配中文字符
chinese_pattern = re.compile(r'[\u4e00-\u9fa5（）\s]+')

# 指定图片文件所在的文件夹路径
image_folder = '/1T/liufangtao/datas/galss_baoming/test/9-8/T/out1xml'

# 遍历文件夹中的文件
for filename in os.listdir(image_folder):
    # 构建完整的文件路径
    file_path = os.path.join(image_folder, filename)
    
    # 检查是否是文件而不是文件夹
    if os.path.isfile(file_path):
        # 使用正则表达式替换中文字符为空字符串
        new_filename = re.sub(chinese_pattern, '', filename)
        
        # 构建新的文件路径
        new_file_path = os.path.join(image_folder, new_filename)
        
        # 重命名文件
        os.rename(file_path, new_file_path)
