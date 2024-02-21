import os
from tqdm import tqdm

def count_files_with_string(directory, target_strings):
    """
    统计具有相同字符串的文件名数量
    :param directory: 文件夹路径
    :param target_string: 目标字符串
    :return: 具有相同字符串的文件名数量
    """
    file_names = os.listdir(directory)
    count_dict = {target_string: 0 for target_string in target_strings}
    for file_name in file_names:
        for target_string in target_strings:
            if target_string in file_name:
                count_dict[target_string] += 1
    return count_dict

def add_folder_name_to_files(directory):
    str_lists = []
    for root, dirs, files in os.walk(directory):
        for file in tqdm(files):
            str_lists.append("_".join(file.split('_')[:2]))
    return list(set(str_lists))


# 示例用法
img_path = "/1T/liufangtao/datas/glass/test/1204/缺陷数据1204/test/out2"  #原始图
directory = "/1T/liufangtao/ultralytics/runs/detect/M10_glass0.3_result"  #检测出的图片
target_strings = add_folder_name_to_files(img_path)
print('共有玻璃片数:'+str(len(target_strings)))
result = count_files_with_string(directory, target_strings)
print('检测出玻璃片数：'+str(len(result)))
print(result)

