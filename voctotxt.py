"""
voc(xml格式)转yolo(txt格式)
"""
import os
import xml.etree.ElementTree as ET

# 注意修改数据集标签的路径
dirpath = r'/1T/liufangtao/datas/glass/test/1101/bigbali/out2/xmls'  # 原来存放xml文件的目录
newdir = r'/1T/liufangtao/datas/glass/test/1101/bigbali/out2/labels'  # 修改label后形成的txt目录

if not os.path.exists(newdir):
    os.makedirs(newdir)

for fp in os.listdir(dirpath):
    # 直接解析XML文件:
    root = ET.parse(os.path.join(dirpath, fp)).getroot()
    
    xmin, ymin, xmax, ymax = 0, 0, 0, 0
    sz = root.find('size')
    if sz==None:
        with open(os.path.join(newdir, fp.rsplit('.',1)[0] + '.txt'), 'a+') as f:
            f.write('')
    else:
        width = float(sz[0].text)
        height = float(sz[1].text)
        filename = root.find('filename').text

    if root.find('object'):

        for child in root.findall('object'):  # 找到图片中的所有框
            name = child.find('name').text
           # print(name)修改自己的类别！！！！！！！！！！！！！
            if name == 'bigburr':
                classes = 6
            # elif name == 'fire':
            #     classes = 2
            # elif name == 'cjyzps':
            #     classes = 2
            # else:
            #     classes = 1
            sub = child.find('bndbox')  # 找到框的标注值并进行读取
            #***************注意不同的xml格式*************************
            # xmin = float(sub[0].text)
            # ymin = float(sub[1].text)
            # xmax = float(sub[2].text)
            # ymax = float(sub[3].text)
            xmin = float(sub[0].text)
            xmax = float(sub[1].text)
            ymin = float(sub[2].text)
            ymax = float(sub[3].text)
            try:  # 转换成yolov3的标签格式，需要归一化到（0-1）的范围内
                x_center = (xmin + xmax) / (2 * width)
                y_center = (ymin + ymax) / (2 * height)
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height
                x_center = ('%.6f' % x_center)
                y_center = ('%.6f' % y_center)
                w = ('%.6f' % w)
                h = ('%.6f' % h)
            except ZeroDivisionError:
                print(filename, '的 width有问题')
            # b = fp.rsplit('.', 1)[0]
            # print(b)
            with open(os.path.join(newdir, fp.rsplit('.',1)[0] + '.txt'), 'a+') as f:
                f.write(' '.join([str(classes), str(x_center), str(y_center), str(w), str(h) + '\n']))
                print(os.path.join(newdir, fp.rsplit('.',1)[0] + '.txt'))

    else:
        with open(os.path.join(newdir, fp.rsplit('.',1)[0] + '.txt'), 'a+') as f:
            f.write(' ')
        print(filename, '运行中....')
