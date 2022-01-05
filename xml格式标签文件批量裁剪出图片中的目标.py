import cv2
import xml.etree.ElementTree as ET
import os 

img_path = r'E:\liufangtao\home\tree1\images' #图片路径
xml_path = r'E:\liufangtao\home\tree1\xmls' #标签路径
obj_img_path = r'E:\liufangtao\home\tree1\img'   #目标裁剪图片存放路径

for img_file in os.listdir(img_path):    #遍历图片文件夹
    if img_file[-4:] in ['.png', '.jpg']:    #判断文件是否为图片格式
        img_filename = os.path.join(img_path, img_file)  #将图片路径与图片名进行拼接
        img_cv = cv2.imread(img_filename)  #读取图片
        
        img_name = (os.path.splitext(img_file)[0])  #分割出图片名，如“000.png” 图片名为“000”
        xml_name = xml_path + '\\' + '%s.xml'%img_name  #利用标签路径、图片名、xml后缀拼接出完整的标签路径名
        
        if os.path.exists(xml_name):  #判断与图片同名的标签是否存在，因为图片不一定每张都打标
            root = ET.parse(xml_name).getroot() #利用ET读取xml文件
            count = 0 #目标框个数统计，防止目标文件覆盖
            for obj in root.iter('object'):  #遍历所有目标框
                name = obj.find('name').text   #获取目标框名称，即label名
            
                xmlbox = obj.find('bndbox')   #找到框目标
                x0 = xmlbox.find('xmin').text  #将框目标的四个顶点坐标取出
                y0 = xmlbox.find('ymin').text
                x1 = xmlbox.find('xmax').text
                y1 = xmlbox.find('ymax').text
                
                obj_img = img_cv[int(y0):int(y1), int(x0):int(x1)]  #cv2裁剪出目标框中的图片
                
                cv2.imwrite(obj_img_path + '\\' + '%s_%s'%(img_name, count) + '.jpg', obj_img)  #保存裁剪图片
                count += 1 #目标框统计值自增1

