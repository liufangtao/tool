# -*- coding: utf-8 -*-
# liufangtao
#批量处理img和xml文件，根据xml文件中的坐标把img中的目标标记出来，并保存到指定文件夹。
import xml.etree.ElementTree as ET
import os, cv2
import numpy 
# from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

annota_dir = r'/1T/liufangtao/datas/glass/0731/out0/all_tile_650/labels'
origin_dir = r'/1T/liufangtao/datas/glass/0731/out0/all_tile_650/images'
target_dir1= r'/1T/liufangtao/datas/glass/0731/out0/all_tile_650/out'

# class_dist = {0:'盘式绝缘子', 1:'棒式绝缘子', 2:'复合绝缘子', 
#                         3:'柱上开关绝缘子', 4:'针式绝缘子', 5:'玻璃绝缘子',6:'悬式棒绝缘子'}Crack', 'Waterstains','dirty
        
class_dist ={0:'broken', 1:'burr', 2:'chip',3:'Crack', 4:'Waterstains', 5:'dirty'}
def divide_img(oriname):
    img_file = os.path.join(origin_dir, oriname)
    im = cv2.imread(img_file)
    h, w = im.shape[:2]
    # print(w)
    # 图像从OpenCV格式转换成PIL格式 
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_PIL)
    #字体路径和字体大小
    font = ImageFont.truetype('SimHei.ttf', 40)
    
    
    xml_file = open(os.path.join(annota_dir, oriname[:-4] + '.txt'))  # 读取每个原图像的xml文件
    
        
    # print(xml_file)
    for bbox in xml_file.readlines():
        id, x1, y1, x2, y2 = map(float, bbox.strip().split())
        #int(bbox.split(' ')[0]), float(bbox.split(' ')[2]), float(bbox.split(' ')[3]), float(bbox.split(' ')[4]), float(bbox.split(' ')[5])
        xmin = ((x1*2*w)-x2*w)/2
        xmax = ((x1*2*w)+x2*w)/2
        ymin = ((y1*2*h)-y2*h)/2
        ymax = ((y1*2*h)+y2*h)/2
        # xmin = x1
        # xmax = x2
        # ymin = y1
        # ymax = y2
        

        # print(xmin, ymin, xmax, ymax)
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 在边界框的两点（左上角、右下角）画矩形，无填充，边框红色，边框像素为5
        draw.rectangle(((xmin, ymin), (xmax, ymax)), fill=None, outline='green', width=5)
        draw.text((xmin, ymin-40), class_dist[id], font=font, fill=(254, 0, 0))       
    
    # 转换回OpenCV格式 
    img_OpenCV = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR) 
    img_name = oriname 
    print(img_name)
    to_name = os.path.join(target_dir1, img_name)
    cv2.imwrite(to_name, img_OpenCV)

img_list = os.listdir(origin_dir)

for name in img_list:
    if name.endswith('.jpg') or name.endswith('.png'):
        divide_img(name)
    # try: 
    #     divide_img(name.rstrip('.jpg'))
    # except FileNotFoundError:
    #     continue