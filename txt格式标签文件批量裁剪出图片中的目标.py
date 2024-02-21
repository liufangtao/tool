
from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import cv2

ImgPath = r'/1T/liufangtao/datas/glass/all8_1_2_3_7_9/bianyuan_train_val1215_9class/images/' 

AnnoPath = r'/1T/liufangtao/datas/glass/all8_1_2_3_7_9/bianyuan_train_val1215_9class/labels/'#txt位置

ProcessedPath = r'/1T/liufangtao/datas/glass/all8_1_2_3_7_9/bianyuan_train_val1215_9class/corp/'#保存图片新地址

imagelist = os.listdir(ImgPath)
i = 1

for image in imagelist:
    # print(image)

    image_pre, ext = os.path.splitext(image)

    imgfile = ImgPath +  image
    im = cv2.imread(imgfile)
    h, w = im.shape[:2]

    print(imgfile)
    
    if not os.path.exists(AnnoPath + image_pre + '.txt'): continue

    
    xml_file = open(os.path.join(AnnoPath, image_pre + '.txt'))
    # print(xml_file.readlines())
    # if xml_file.readlines() != None:
    for bbox in xml_file.readlines():
        try:
            id, x1, y1, x2, y2 = str(bbox.split(' ')[0]), float(bbox.split(' ')[1]), float(bbox.split(' ')[2]), float(bbox.split(' ')[3]), float(bbox.split(' ')[4])
            # id, x1, y1, x2, y2 = str(bbox.split(' ')[0]), bbox.split(' ')[1], bbox.split(' ')[2], bbox.split(' ')[3], bbox.split(' ')[4]
            xmin = ((x1*2*w)-x2*w)/2
            xmax = ((x1*2*w)+x2*w)/2
            ymin = ((y1*2*h)-y2*h)/2
            ymax = ((y1*2*h)+y2*h)/2
        
            obj = np.array([xmin, ymin, xmax, ymax])

            shift = np.array([[1, 1, 1, 1]])

            XYmatrix = np.tile(obj, (1, 1))

            cropboxes = XYmatrix * shift

            img = Image.open(imgfile)
            if id in ['3']:
                savepath = ProcessedPath + id

                if not os.path.exists(savepath):
                    os.makedirs(savepath)

                for cropbox in cropboxes:
                    cropedimg = img.crop(cropbox)

                    cropedimg.save(savepath+'/' + image_pre + '_' + str(i) + '.jpg')
                    i += 1
        except ValueError:
            continue
                
print(i)



