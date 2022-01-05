#coding=utf-8
import os
import os.path
import xml.dom.minidom

path = r"D:\build\tree1\xmls"
files = os.listdir(path) #得到文件夹下所有文件名称
s = []

for xmlFile in files:
  if not os.path.isdir(xmlFile):
    print(xmlFile)
  dom=xml.dom.minidom.parse(os.path.join(path,xmlFile)) ###最核心的部分os.path.join(path,xmlFile),路径拼接,输入的是具体路径
  root=dom.documentElement
  name=root.getElementsByTagName('name')
  for i in range(len(name)):
    print(name[i].firstChild.data)
    if name[i].firstChild.data == 'szdx':
      name[i].firstChild.data='sz'
    # else:
    #   name[i].firstChild.data='head'
    print(name[i].firstChild.data)
  with open(os.path.join(path,xmlFile),'w') as fh:
    dom.writexml(fh)
    print('写入name OK!')


