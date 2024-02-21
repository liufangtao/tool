import shutil, os
# import cv2
from pathlib import Path 
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# os.listdir(Path_dir)  ['burrbat','chipbat','crackbat']  ['broken', 'burr']


def GetAnnotBoxLoc(xml_dir, Path_dir, save_draw_imgDir):
    CLASSES=['zangwu','huashang','shike']
    for parent, dirnames, filenames in os.walk(Path_dir):
        for filename in filenames:
            if filename.endswith(".jpg"):#判断字符串是否以指定的x结尾
                filename_qianzhui = Path(filename).stem #排除后缀名的文件或路径名
                img_file_path = os.path.join(Path_dir, filename_qianzhui) + ".jpg"
                xml_file_path = os.path.join(xml_dir, filename_qianzhui) + ".xml"
                # copy_file = os.path.join(xml_dir, xml_file_path)
                
                tree = ET.ElementTree(file=xml_file_path) 
                root = tree.getroot()  
                ObjectSet = root.findall('object')
                i = 0
                for child in ObjectSet:
                    name = child.find('name').text
                    print(filename)
                    if name in CLASSES:
                    # if child = "jyz_tc_bs_min":
                        try:
                            shutil.move(xml_file_path, save_draw_imgDir)
                            shutil.move(img_file_path, save_draw_imgDir)
                            # os.remove(xml_file_path)shutil.move
                        except Exception as e :
                            print(str(e))

if __name__ == "__main__": 
    save_draw_imgDir = "/1T/liufangtao/datas/glass_changxin/12monthdatas/1221/1.1"
    Path_dir = "/1T/liufangtao/datas/glass_changxin/12monthdatas/1221/images"  #jpg文件在一个文件夹
    xml_dir = '/1T/liufangtao/datas/glass_changxin/12monthdatas/1221/xmls' #xml文件           
    GetAnnotBoxLoc(xml_dir, Path_dir, save_draw_imgDir)

