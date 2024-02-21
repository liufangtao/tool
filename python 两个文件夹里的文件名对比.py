import os
import shutil
from tqdm import tqdm

def copy_images_with_different_names(source_directory1, source_directory2, destination_directory):
    # 获取两个源目录中的文件列表
    source_files1 = os.listdir(source_directory1)
    source_files2 = os.listdir(source_directory2)

    # 创建目标目录（如果不存在）
    os.makedirs(destination_directory, exist_ok=True)

    # 遍历第一个源目录中的文件
    for source_file1 in tqdm(source_files1):
        source_file_path1 = os.path.join(source_directory1, source_file1)

        # 检查文件是否是图片文件（可以根据需要调整文件扩展名的判断条件）
        if source_file1.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # 构建目标文件路径，保持文件名不变
            destination_file_path = os.path.join(destination_directory, source_file1)
            try:

                # 如果同名文件不在第二个源目录中，复制文件到目标目录
                if source_file1 not in source_files2:
                    shutil.copy(source_file_path1, destination_file_path)
            except OSError:
                continue

if __name__ == "__main__":
    # 两个源目录包含要比较的图片
    source_directory1 = '/run/user/1000/gvfs/smb-share:server=192.168.10.14,share=wanglei/宝明项目/缺陷数据测试集---勿随意增加数据/C面测试数据--已筛选/凹点/有缺陷'
    source_directory2 = '/run/user/1000/gvfs/smb-share:server=192.168.10.14,share=wanglei/宝明项目/缺陷数据测试集---勿随意增加数据/C面测试数据--已筛选/凹点/有缺陷-train25last模型推理结果'

    # 目标目录是复制后的图片将要存储的位置
    destination_directory = '/run/user/1000/gvfs/smb-share:server=192.168.10.14,share=wanglei/宝明项目/缺陷数据测试集---勿随意增加数据/C面测试数据--已筛选/凹点/漏检测'

    # 执行复制操作
    copy_images_with_different_names(source_directory1, source_directory2, destination_directory)