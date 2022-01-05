# -*- coding: UTF-8 -*-
import os
import os.path
from xml.etree.ElementTree import parse, Element

def changeName(xml_fold, origin_name, new_name):
    '''
    xml_fold: xml存放文件夹
    origin_name: 原始名字，比如弄错的名字，原先要cow,不小心打成cwo
    new_name: 需要改成的正确的名字，在上个例子中就是cow
    '''
    files = os.listdir(xml_fold)
    cnt = 0
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text # 修改类名的
            # tmp_name = obj.find('difficult').text # 修改difficult 修改truncated
            if tmp_name == origin_name: # 修改
                obj.find('name').text = new_name
                # obj.find('difficult').text = new_name
                print("change %s to %s." % (origin_name, new_name))
                cnt += 1
        dom.write(file_path, xml_declaration=True)#保存到指定文件
    print("有%d个文件被成功修改。" % cnt)

def changeAll(xml_fold,new_name):
    '''
    xml_fold: xml存放文件夹
    new_name: 需要改成的正确的名字，在上个例子中就是cow,把所有类别改为1个类别
    '''
    files = os.listdir(xml_fold)
    cnt = 0
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text
            obj.find('name').text = new_name
            print("change %s to %s." % (tmp_name, new_name))
            cnt += 1
        dom.write(file_path, xml_declaration=True)#保存到指定文件
    print("有%d个文件被成功修改。" % cnt)

def countAll(xml_fold):
    '''
    xml_fold: xml存放文件夹
    '''
    files = os.listdir(xml_fold)
    dict={}
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text
            if tmp_name not in dict:
                dict[tmp_name] = 0
            else:
                dict[tmp_name] += 1
        dom.write(file_path, xml_declaration=True)#保存到指定文件
    print("统计结果如下：")
    print("-"*10)
    for key,value in dict.items():
        print("类别为%s的目标个数为%d." % (key, value+1))
    print("-"*10)


if __name__ == '__main__':
    path = r'E:\liufangtao\home\all\xmls' #xml文件所在的目录
    # changeName(path, "jyz _tc_ps", "jyz_bl_ps")
    # changeAll(path, "difficultfuse") #谨慎使用
    countAll(path)
'''
dxdlj_sx:439个
ugh:230个
gb:1454个
wtgb:788个
dxdlj:693个
gd_sx:57个
ugh_sx:22个
yxd:417个
nxd:332个
wtgb_sx:16个
gb_sx:161个
ugb:4个
信息统计算完毕。
ugb:4个 = ugh
gd_sx:57个 = gb_sx
'''
