import shutil, os
import cv2
from pathlib import Path 
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

save_draw_imgDir = r"E:\liufangtao\home\all\1"
Path_dir = r"E:\liufangtao\home\all\bljyz"  #xml文件和jpg文件在一个文件夹
os.listdir(Path_dir)


def GetAnnotBoxLoc():
    for parent, dirnames, filenames in os.walk(Path_dir):
        for filename in filenames:
            if filename.endswith(".xml"):#判断字符串是否以指定的x结尾
                filename_qianzhui = Path(filename).stem #排除后缀名的文件或路径名
                img_file_path = os.path.join(Path_dir, filename_qianzhui) + ".jpg"
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
                    # os.remove(xml_file_path)

GetAnnotBoxLoc()
