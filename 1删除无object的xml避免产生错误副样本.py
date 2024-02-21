import shutil, os
import cv2
from pathlib import Path 
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

save_draw_imgDir = r"/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/kong" #空object保存位置
Path_dir = r"/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/xmls"  #xml文件在一个文件夹
images_dir = r'/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/images'
os.listdir(Path_dir)
os.makedirs(save_draw_imgDir, exist_ok=True)


def GetAnnotBoxLoc():
    for parent, dirnames, filenames in os.walk(Path_dir):
        for filename in filenames:
            if filename.endswith(".xml"):#判断字符串是否以指定的x结尾
                filename_qianzhui = Path(filename).stem #排除后缀名的文件或路径名
                img_file_path = os.path.join(images_dir, filename_qianzhui) + ".jpg"
                xml_file_path = os.path.join(Path_dir, filename_qianzhui) + ".xml"
                copy_file = os.path.join(Path_dir, xml_file_path)

                tree = ET.ElementTree(file=copy_file) 
                root = tree.getroot()  
                ObjectSet = root.findall('object')
                i = 0
                for child in ObjectSet:
                    if child != "":
                        i= i+1
                if i == 0:
                    shutil.move(xml_file_path, save_draw_imgDir)
                    shutil.move(img_file_path, save_draw_imgDir)
                    print(img_file_path)
                    # os.remove(xml_file_path)

GetAnnotBoxLoc()
