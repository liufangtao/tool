# # !/usr/bin/env python
# # encoding: utf-8

# import os
# import glob
# from PIL import Image

# #指定找到文件后，另存为的文件夹路径
# outDir = os.path.abspath('E:\\windows_v1.8.0\\lg\\剩余图片') 

# #指定第一个文件夹的位置
# imageDir1 = os.path.abspath('E:\\windows_v1.8.0\\lungu-pre')

# #定义要处理的第一个文件夹变量
# image1 = [] #image1指文件夹里的文件，包括文件后缀格式；
# imgname1 = [] #imgname1指里面的文件名称，不包括文件后缀格式

# #通过glob.glob来获取第一个文件夹下，所有'.jpg'文件
# imageList1 = glob.glob(os.path.join(imageDir1, '*.jpg'))

# #遍历所有文件，获取文件名称（包括后缀）
# for item in imageList1:
#     image1.append(os.path.basename(item))

# #遍历文件名称，去除后缀，只保留名称
# for item in image1:
#     (temp1, temp2) = os.path.splitext(item)
#     imgname1.append(temp1)

# #对于第二个文件夹路径，做同样的操作
# imageDir2 = os.path.abspath('E:\\windows_v1.8.0\\lungu-lg1-lg2\\JPEGImages')
# image2 = []
# imgname2 = []
# imageList2 = glob.glob(os.path.join(imageDir2, '*.jpg'))

# for item in imageList2:
#     image2.append(os.path.basename(item))

# for item in image2:
#     (temp1, temp2) = os.path.splitext(item)
#     imgname2.append(temp1)

# #通过遍历，获取第一个文件夹下，文件名称（不包括后缀）与第二个文件夹相同的文件，并另存在outDir文件夹下。文件名称与第一个文件夹里的文件相同，后缀格式亦保持不变。
# for item1 in imgname1:
#     for item2 in imgname2:
#         if item1 == item2:
#             dir = imageList1[imgname1.index(item1)]
#             img = Image.open(dir)
#             name = os.path.basename(dir)
#             os.remove(os.path.join(imageDir1, name))
#             # img.save(os.path.join(outDir, name))
#             print(name)
#             
import os
import shutil
from tqdm import tqdm

# data1_path = r'/1T/liufangtao/ultralytics/runs/detect/baoming_glass_result' #
# data2_path = r'/1T/liufangtao/datas/galss_baoming/cut/mangkongaodian/out0'
# data3_path = r'/1T/liufangtao/datas/galss_baoming/cut/mangkongaodian/out1'

# file1_list = os.listdir(data1_path)
# file2_list = os.listdir(data2_path)

# test_list = []
# for file1 in tqdm(file1_list):
#     a = file1[:-6]
#     for file2 in file2_list:
#         b = file2[:-6]
#         if a==b:#and file2 != file1
#             shutil.copy(os.path.join(data2_path, file2), os.path.join(data3_path, file2))

import os
import shutil

def compare_and_copy_files(source_directory1, source_directory2):
    # 获取两个源目录中的文件列表
    files1 = os.listdir(source_directory1)
    files2 = os.listdir(source_directory2)

    # 创建目标目录（如果不存在）
    # os.makedirs(destination_directory, exist_ok=True)

    # 比较文件并拷贝
    for file1 in tqdm(files1):
        for file2 in files2:
            # if file1 == file2:
            #     # 如果文件名相同，则跳过，不做任何操作
            #     continue
            if file1[:-6] == file2[:-6]:
                # 如果文件名部分相同，且文件2中不存在相同的文件，拷贝到目标目录
                source_path = os.path.join(source_directory1, file1)
                destination_path = os.path.join(source_directory2, file1)
                if not os.path.exists(destination_path):
                    shutil.copy(source_path, destination_path)

if __name__ == "__main__":
    # 源目录1包含要比较的文件
    source_directory1 = '/1T/liufangtao/datas/galss_baoming/cut/aodian/C/out1'

    # 源目录2包含要比较的文件
    source_directory2 = '/1T/liufangtao/datas/galss_baoming/cut/aodian/C/out2'

    # 目标目录是拷贝后的文件将要存储的位置
    # destination_directory = 'path_to_destination_directory'

    # 执行比较和拷贝操作
    compare_and_copy_files(source_directory1, source_directory2)


    


