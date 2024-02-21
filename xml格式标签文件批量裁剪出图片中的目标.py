
from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np

ImgPath = '/1T/liufangtao/datas/glass/0731/out0/all_tile_650bat/all8_1_2_3_7_9/out/images/' 
AnnoPath = '/1T/liufangtao/datas/glass/0731/out0/all_tile_650bat/all8_1_2_3_7_9/out/xmls/'#xml位置
ProcessedPath = '/1T/liufangtao/datas/glass/0731/out0/all_tile_650bat/all8_1_2_3_7_9/out/corp/'#保存图片新地址
labels_list=['Broken', 'Burr', 'Chip', 'Draw', 'Crack', 'Waterstains','dirty']
imagelist = os.listdir(ImgPath)
i = 1
 
for image in imagelist:
    image_pre, ext = os.path.splitext(image)
    imgfile = ImgPath +  image
    print(imgfile)
    if not os.path.exists(AnnoPath + image_pre + '.xml'): continue
    xmlfile = AnnoPath+  image_pre + '.xml'
    DomTree = xml.dom.minidom.parse(xmlfile)
    annotation = DomTree.documentElement
    filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]
    # filename = filenamelist[0].childNodes[0].data
    objectlist = annotation.getElementsByTagName('object')

    for objects in objectlist:
        namelist = objects.getElementsByTagName('name')
        objectname = namelist[0].childNodes[0].data
        savepath = ProcessedPath + objectname
        if objectname in labels_list:
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            bndbox = objects.getElementsByTagName('bndbox')
            cropboxes = []
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
                w = x2 - x1
                h = y2 - y1
                obj = np.array([x1, y1, x2, y2])
                shift = np.array([[1, 1, 1, 1]])
                XYmatrix = np.tile(obj, (1, 1))
                cropboxes = XYmatrix * shift
                img = Image.open(imgfile)
                img = img.convert("RGB")
                for cropbox in cropboxes:
                    cropedimg = img.crop(cropbox)
                    cropedimg.save(savepath+'/' + image_pre + '_' + str(i) + '.jpg')
                    i += 1                
print(i)



# python reader_infer.py --detector_dir D:\PaddleX\w\meter_det_inference_model --segmenter_dir D:\PaddleX\w\meter_seg_inference_model --image D:\PaddleX\w\4.jpg --save_dir D:\PaddleX\w\output --use_erode