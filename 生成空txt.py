import os
import xml.dom.minidom
import cv2
 
img_path = r'/1T/liufangtao/datas/glass_quanmian/test/20240205/images'
xml_path = r'/1T/liufangtao/datas/glass_quanmian/test/20240205/labels/'



# 创建新的xml文件（保留所有原有label为非背景的xml）
for img_file in os.listdir(img_path):    
    filename = os.path.join(img_path, img_file)
    # img_cv = cv2.imread(filename)
    
    img_name = os.path.splitext(img_file)[0]
    print(img_name)   
    if not os.path.exists(xml_path+'%s.txt'%img_name):
        with open(xml_path+'%s.txt'%img_name, mode="w", encoding="utf-8") as f:
        	f.write('')
        
