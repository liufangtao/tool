import os
from unicodedata import name
import xml.etree.ElementTree as ET
import glob

def count_num(indir):

    # 提取xml文件列表
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    dict = {} # 新建字典，用于存放各类标签名及其对应的数目
    for i, file in enumerate(annotations): # 遍历xml文件
       
        # actual parsing
        in_file = open(file, encoding = 'utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 遍历文件的所有标签
        for obj in root.iter('object'):
            name = obj.find('name').text
            if(name in dict.keys()): dict[name] += 1 # 如果标签不是第一次出现，则+1
            else: dict[name] = 1 # 如果标签是第一次出现，则将该标签名对应的value初始化为1

    # 打印结果
    print("各类标签的数量分别为：")
    for key in dict.keys(): 
        print(key + ': ' + str(dict[key]))            

# indir=r'Y:\liu\gz\xmls/'   # xml文件所在的目录

# count_num(indir) # 调用函数统计各类标签数目
#*************************************************************************
def count_classes_in_labels(label_folder):
    class_counts = {}

    for filename in os.listdir(label_folder):
        if filename.endswith(".txt"):
            label_file_path = os.path.join(label_folder, filename)
            
            with open(label_file_path, 'r') as label_file:
                lines = label_file.readlines()
            
            for line in lines:
                class_id = line.strip().split()[0]
                class_counts[class_id] = class_counts.get(class_id, 0) + 1

    return class_counts

# 示例调用
label_folder = '/1T/liufangtao/datas/glass/all8_1_2_3_7_9/bianyuan_train_val1215_9class/labels'  # 标签文件夹路径

# 定义一个函数，用于计算每个类别的标签数量
class_counts = count_classes_in_labels(label_folder)

print("类别数目统计：")
for class_id, count in class_counts.items():
    print(f"类别 {class_id}: {count} 个")

# c类别数目统计：
# 类别数目统计：
# 类别 0: 183 个
# 类别 1: 258 个
# 类别 2: 9 个
# 类别 3: 7 个

# t类别数目统计：
# 类别 0: 73 个
# 类别 1: 28 个
# 类别 3: 2 个
# 0728类别数目统计：
# 类别 3: 37 个
# 类别 0: 3229 个
# 类别 9: 381 个
# 类别 4: 238 个
# 类别 5: 505 个
# 类别 7: 1919 个
# 类别 2: 51 个
# 类别 10: 214 个
# 类别 8: 649 个
# all类别数目统计：
# 类别 0: 9509 个
# 类别 7: 2581 个
# 类别 2: 725 个
# 类别 8: 647 个
# 类别 5: 301 个
# 类别 9: 1169 个
# 类别 3: 16 个
# 类别 4: 300 个
# 类别 10: 163 个
# 类别 6: 13 个
# gls0708
# 类别 11: 383 个
# 类别 0: 3462 个
# 类别 3: 42 个
# 类别 5: 567 个
# 类别 9: 401 个
# 类别 2: 83 个
# 类别 4: 164 个
# 类别 7: 372 个
# 类别 10: 221 个
