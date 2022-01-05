import time
import cv2
import numpy as np
from PIL import Image
import json
import xml.etree.ElementTree as ET 
import random

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素    
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个    
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作



# 送入的是dict {图像名字 ：框信息} 框信息是[[x1,y1,w,h,label], [x1,y1,w,h,label],[]]
def write(infos,shape=None):

    root = ET.Element('annotation',{"verified":"no"})  # 根节点

    folder = ET.SubElement(root, 'folder')
    folder.text = '1'
    img_name = list(infos.keys())[0].strip()  # 图像信息
    print(img_name)

    filename = img_name.split("/")[-1]
    file_name = ET.SubElement(root, 'filename')
    file_name.text = filename  # 文件名这个tag

    path = ET.SubElement(root, 'path')  # 路径的tag
    path.text = img_name 

    source = ET.SubElement(root, 'source')
    database = ET.SubElement(source, 'database')
    database.text = "Unknown"

    if shape:
        h,w,c = shape[1], shape[0],shape[2]
    else:
        img = cv2.imread(img_name)
        h,w,c = img.shape 
        
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(w)
    height = ET.SubElement(size, 'height')
    height.text = str(h)
    depth = ET.SubElement(size, 'depth')
    depth.text = str(c)

    segmented = ET.SubElement(root, 'segmented')
    segmented.text = str(0)

    for key in infos.keys():
        bboxes = infos[key]
        for bbox in bboxes:
            object_tag = ET.SubElement(root, 'object')
            # bbox = ['911', '258', '153', '326', 'class1']
            name = ET.SubElement(object_tag, 'name')
            name.text = bbox[-1]  #框名字
            
            pose = ET.SubElement(object_tag, 'pose')
            pose.text = "Unspecified"
            trunc = ET.SubElement(object_tag,'truncated')
            trunc.text = '0'
            diff = ET.SubElement(object_tag,'difficult')
            diff.text = '0'
            # 下面是写入坐标框
            bndbox = ET.SubElement(object_tag,'bndbox')
            #left_x:  911   top_y:  258   width:  153   height:  326
            bbox[2] = str(int(bbox[2]))
            bbox[3] = str(int(bbox[3]))

            xmin = ET.SubElement(bndbox,'xmin')
            xmin.text = str(int(bbox[0]))

            ymin = ET.SubElement(bndbox,'ymin')
            ymin.text = str(int(bbox[1]))

            xmax = ET.SubElement(bndbox,'xmax')   
            # 如果是 x y w h
            # xmax.text = str(int(bbox[0]) + int(bbox[2]) )
            # 如果是 x1 y1 x2 y2
            xmax.text = str(int(bbox[2]) )

            ymax = ET.SubElement(bndbox,'ymax')

            # ymax.text = str(int(bbox[1]) + int(bbox[3]) )
            ymax.text = str(int(bbox[3]))

    pretty_xml(root, '\t', '\n')  # 执行美化方法
    #ET.dump(root)
    tree = ET.ElementTree(root)
    xml_name = filename.replace("jpg","xml")  # 要保存的xml文件名字 和图像文件名相同，仅后缀不同
    tree.write(f"D:\\build\\meter_det\\testxml\\{xml_name}", encoding="utf-8",xml_declaration=False)


    

# 打开json标签文件
with open(r'D:\build\meter_det\annotations\instance_test.json','r') as f:
    data_an = {}  # 外围大字典
    json_dicts = json.loads(f.read())



cate = json_dicts['categories']
print(cate)
cls_name = [0]*len(cate)
cls_name = ['背景', 'meter']
print(cls_name)

# for cate_dict in cate:
#     cls_name[cate_dict['id']] = cate_dict['name'] # 各个类别对应的名字 按顺序放在cls_name中，如id为0的类别名就是cls_name[0]

# 类别 按照id顺序来的
#  ['背景', '瓶盖破损', '瓶盖变形', '瓶盖坏边', '瓶盖打旋', '瓶盖断点', '标贴歪斜', '标贴起皱', '标贴气泡', '喷码正常', '喷码异常', '酒液杂质', '瓶身破损', '瓶身气泡']

images_info = json_dicts["images"]  # 图像信息

image_nums = len(images_info)  # 图像数量
print(image_nums)

file_list = []  # 存放图像基本信息 依次按顺序读入，这样图像image_id是k的图像信息就是file_list[k-1]  k从1开始

annot_list = [[] for _ in range(image_nums)] # 存放每个图像对应的框,每个图像的全部目标是一个元素，因此初始化为一个长度和图像数量相同的列表，列表的每个元素是一个空列表，后面用于增加目标框信息

for index in range(image_nums):
    # 第 index张图像的信息 包括文件名 宽高
    file_name = images_info[index]["file_name"]  # id从1变换到2668  索引从0到2667
    width = images_info[index]["width"]
    height = images_info[index]['height']
    # print([file_name,width,height],'-------')
    file_list.append([file_name,width,height])  # file_list列表保存


annot = json_dicts["annotations"]
# 根据目标所属的图像id，放到列表对应的位置。从而使一张图片的多个目标聚合在一起
for index in range(len(annot)):  # 获取标签信息
    # 第index个目标的框可能是x y w h或者x1 y1 x2 y2的形式。按照实际情况修改
    annot[index]['bbox'][2] = annot[index]['bbox'][2] + annot[index]['bbox'][0]  # 这是x y w h的形式 转成x1 y1 x2 y2的形式。或者不转，和write函数保持一致就可以
    annot[index]['bbox'][3] = annot[index]['bbox'][3] + annot[index]['bbox'][1]
    
    # 这个目标的类别id是annot[index]["category_id"] 它的名字是cls[索引]  注意json文件中类别id可能是从1开始，而cls_name的索引是0开始 注意保持对应
    annot[index]['bbox'].append(cls_name[ annot[index]["category_id"] ])  # 在框信息后面 加入 label
    # print(annot[index]['bbox'],annot[index]['image_id']-1)
    # -1是因为该目标对应的图像id是从1开始，因此要放在列表的第 id -1的位置
    annot_list[annot[index]['image_id']-1].append(annot[index]['bbox'])   # bbox是 x1 y1 w h 


# 对每一张图 写入xml文件
for index in range(image_nums):
    print(index)
    box = annot_list[index]
    print(box)
    # info的key是文件名 value是坐标列表
    write({file_list[index][0]: box},shape=[str(file_list[index][1]),str(file_list[index][2]),'3'])  # shape =hwc
