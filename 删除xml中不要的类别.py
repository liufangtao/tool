import xml.etree.cElementTree as ET
import os

path_root = [r'/1T/liufangtao/datas/galss_baoming/0824/16C-20230823/xmls']  #自己的xml路径
# CLASSES = ['person']
# CLASSES1 = []
CLASSES = ['aodian', 'kajiawei', 'tudian', 'heneiyiwu', 'shenhuashang', 'qianhuashang', 'jinshuijinsuan', 'yejingbuliang', 'yejingqipao', 'zangwu', 'shuibowen', 'mangkong','shikebujun']
for anno_path in path_root:
    # print(anno_path)
    xml_list = os.listdir(anno_path)
    for axml in xml_list:
        path_xml = os.path.join(anno_path, axml)
        # print(path_xml)
        tree = ET.parse(path_xml)
        root = tree.getroot()

        for child in root.findall('object'):
            name = child.find('name').text
            # print(name)
            if not name in CLASSES :
                root.remove(child)
        print(axml)
        tree.write(os.path.join(r'/1T/liufangtao/datas/galss_baoming/0824/16C-20230823/xmls0', axml))  #处理结束后保存的路径

