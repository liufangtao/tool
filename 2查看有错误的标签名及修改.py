# -*- coding: UTF-8 -*-
import os
import os.path
import shutil
from xml.etree.ElementTree import parse, Element
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def changeName(xml_fold, origin_name, new_name):
    '''
    xml_fold: xml存放文件夹
    origin_name: 原始名字，比如弄错的名字，原先要cow,不小心打成cwo
    new_name: 需要改成的正确的名字，在上个例子中就是cow
    '''
    files = os.listdir(xml_fold)
    cnt = 0
    for xmlFile in files:
        if os.path.splitext(xmlFile)[1] == ".xml":
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
        if os.path.splitext(xmlFile)[1] == ".xml":
            file_path = os.path.join(xml_fold, xmlFile)
            # print(file_path)
            dom = parse(file_path)
            # f = open(file_path)
            # xml_text = f.read()
            # root = ET.fromstring(xml_text)
            root = dom.getroot()
            for obj in root.iter('object'):#获取object节点中的name子节点
                tmp_name = obj.find('name').text
                
                if tmp_name not in dict:
                    dict[tmp_name] = 0
                else:
                    dict[tmp_name] += 1
            dom.write(file_path, xml_declaration=True)#保存到指定文件
        # f.write(file_path, xml_declaration=True)#保存到指定文件
    print("统计结果如下：")
    print("-"*10)
    for key,value in dict.items():
        print("类别为%s的目标个数为%d." % (key, value+1)) 

    print("-"*10)

def movexml(xml_fold,img_fold, newpath):
    '''
    xml_fold: xml存放文件夹
    '''
    files = os.listdir(xml_fold)
    
    dict={}
    for xmlFile in files:
        file_path = os.path.join(xml_fold, xmlFile)
        dom = ET.ElementTree(file=file_path) 
        root = dom.getroot()
        for obj in root.iter('object'):#获取object节点中的name子节点
            tmp_name = obj.find('name').text
        if tmp_name =='person':
            shutil.move(file_path, newpath)#保存到指定文件 
            shutil.move(os.path.join(img_fold,xmlFile[:-4]+'.jpg'),newpath) 
           
            # if tmp_name not in dict:
            #     dict[tmp_name] = 0
            # else:
            #     dict[tmp_name] += 1
        # dom.write(file_path, xml_declaration=True)#保存到指定文件
    
    print("-"*10)
    print("移动完成：")
 
    print("-"*10)

def removexml(origin_ann_dir,new_ann_dir ):#批量删除不需要的标签类以及空文件
    # origin_ann_dir = 'Annos/'# 设置原始标签路径为 Annos
    # new_ann_dir = 'Annotations/'# 设置新标签路径 Annotations
    for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):# os.walk游走遍历目录名
        for filename in filenames:
            print(filename)
            if os.path.isfile(r'%s%s' %(origin_ann_dir, filename)):#获取原始xml文件绝对路径，isfile()检测是否为文件 isdir检测是否为目录
                origin_ann_path = os.path.join(r'%s%s' %(origin_ann_dir, filename))#如果是，获取绝对路径（重复代码）
                new_ann_path = os.path.join(r'%s%s' %(new_ann_dir, filename))#
                tree = ET.parse(origin_ann_path)#ET是一个xml文件解析库，ET.parse（）打开xml文件。parse--"解析"
                root = tree.getroot()#获取根节点
                for object in root.findall('object'):#找到根节点下所有“object”节点
                    name = str(object.find('name').text)#找到object节点下name子节点的值（字符串），判断:如果不是列出的，（这里可以用in对保留列表成员进行审查），则移除该object节点及其所有子节点。
                    print(name)
                    if not (name in ["jyz_tc_bs"]):
                        root.remove(object)
                flag = 0#清楚非保留完成-标志位0
                tree.write(new_ann_path)#tree为文件，write写入新的文件中。
                for object in root.findall('object'):#找到根节点下所有子节点
                    name = str(object.find('name').text)#找到子节点中name变量，判断：如果每一个都是要保留的，则标志位变1，这是一个审查。
                    if (name in ["jyz_tc_bs"]):
                        flag = 1
                if (flag == 0):
                    os.remove(new_ann_path)#所有不满足审查：有多余object，则用os.remove(filepath)删除指定文件。




if __name__ == '__main__':
    path = r'/1T/liufangtao/datas/glass_changxin/1monthdatas/0129/xmls' #xml文件所在的目录
    # imgpath = r'U:\voc2012\VOCdevkit\people\images'
    newpath = r'E:\liufangtao\image\jyzps188\b\\'#新文件夹
    # changeName(path, "diaomo_dat", "diaomo")#(path,要改的,改了变成的)
    # changeAll(path, "difficultfuse") #谨慎使用
    # countAll(path)@zgz
    # movexml(path, imgpath,newpath)
    countAll(path)#统计
    # removexml(path,newpath)#批量删除不需要的标签类以及空文件

'''统计结果如下
统计结果如下：
----------
类别为cigarette的目标个数为1483.
类别为others的目标个数为2512.
['xycar', 'wheel', 'person', 'jdx', 'miehuoqi']

类别为Waterstains的目标个数为78.
类别为Chip的目标个数为346.
类别为dirty的目标个数为54.
类别为Crack的目标个数为57.
类别为Burr的目标个数为2.
类别为water的目标个数为83.
类别为split的目标个数为297.
'''
