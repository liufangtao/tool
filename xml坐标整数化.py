# *_* coding : UTF-8 *_*
# 开发人员
# 开发时间： 2020/11/25 21:42
# 文件名称： resize_img_xml.py
# 开发工具： PyCharm
# 功能描述： 改变xml文件里的某个属性


import os
import xml.etree.ElementTree as ET

path = r'U:\liu\428-8239-ok\train\xmls'   # 包含xml的文件夹路径

def edit_xml(xml_file):
    """
    修改xml文件
    :param xml_file:xml文件的路径
    :return:
    """
    all_xml_file = os.path.join(path, xml_file)
    tree = ET.parse(all_xml_file)
    print(all_xml_file)
    objs = tree.findall('object')
    for ix, obj in enumerate(objs):
        obj_bnd = obj.find('bndbox')
        obj_xmin = obj_bnd.find('xmin')
        obj_ymin = obj_bnd.find('ymin')
        obj_xmax = obj_bnd.find('xmax')
        obj_ymax = obj_bnd.find('ymax')
        xmin = float(obj_xmin.text)
        ymin = float(obj_ymin.text)
        xmax = float(obj_xmax.text)
        ymax = float(obj_ymax.text)
        obj_xmin.text = str(round(xmin))  #四舍五入转为整数
        obj_ymin.text = str(round(ymin))
        obj_xmax.text = str(round(xmax))
        obj_ymax.text = str(round(ymax))

    tree.write(all_xml_file, method='xml', encoding='utf-8')  # 覆盖更新xml文件

if __name__ == '__main__':
    files = os.listdir(path)              # 获取文件名列表
    for i, file in enumerate(files):
        if file.endswith('.xml'):
            edit_xml(file)
            
