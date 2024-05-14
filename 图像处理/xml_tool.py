import os
import sys
import random
import cv2

import xml.etree.ElementTree as ET
import multiprocessing
import shutil

# Original dataset organisation.
DIRECTORY_ANNOTATIONS = 'Annotations/'
DIRECTORY_IMAGES = 'Images/'
DIRECTORY_SEGMENT ='SEGMENT/'






def gene_SegImage_name(filename,name,ymin,xmin,ymax,xmax):
    segment_name = "{0}_seg_{1}_seg_{2}_seg_{3}_seg_{4}_seg_{5}.png".format(filename,name,ymin,xmin,ymax,xmax)
    return segment_name







def crop_box_img(dataset_dir,image_name):

    file = os.path.join(dataset_dir, DIRECTORY_IMAGES, image_name)
    try:
        print(file)
        img = cv2.imread(file)
    except:
        print (file+"not found !")

    filename = image_name[:-4]
    # Read the XML annotation file.
    filename_annotation = os.path.join(dataset_dir, DIRECTORY_ANNOTATIONS, filename + '.xml')

    try:
        tree = ET.parse(filename_annotation)
    except:
        print (filename_annotation+"not found !")

    root = tree.getroot()

    # Image shape.
    size = root.find('size')
    shape = [int(size.find('height').text),
             int(size.find('width').text),
             int(size.find('depth').text)]
    # Find annotations.


    for obj in root.findall("object"):
        
        name = obj.find("name").text
        # pose = obj.find("pose").text


        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))
        print (ymin, xmin, ymax, xmax)
        target_dir = os.path.join(dataset_dir, DIRECTORY_SEGMENT,name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        cv2.imwrite(os.path.join(target_dir,gene_SegImage_name(filename,name,ymin,xmin,ymax,xmax)),img[ymin:ymax,xmin:xmax,:])






def get_boxes_from_xml(filename_annotation):

    try:
        tree = ET.parse(filename_annotation)
    except:
        print (filename_annotation+"not found !")

    root = tree.getroot()

    # Image shape.
    # size = root.find('size')
    # shape = [int(size.find('height').text),
    #          int(size.find('width').text),
    #          int(size.find('depth').text)]
    # Find annotations.

    box_list=[]
    for obj in root.findall("object"):
        name = obj.find("name").text
        pose = obj.find("pose").text

        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))

        box_list.append([ymin,xmin,ymax,xmax])

    return box_list





def get_label_boxes_from_xml(filename_annotation):

    try:
        tree = ET.parse(filename_annotation)
    except:
        print (filename_annotation+"not found !")

    root = tree.getroot()

    # Image shape.
    # size = root.find('size')
    # shape = [int(size.find('height').text),
    #          int(size.find('width').text),
    #          int(size.find('depth').text)]
    # Find annotations.

    label_box_dict = {}
    box_list=[]
    for obj in root.findall("object"):
        name = obj.find("name").text
        pose = obj.find("pose").text

        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))

        box = [ymin,xmin,ymax,xmax]
        box_list.append(box)
        
        if name not in label_box_dict.keys():
            label_box_dict.update({name:[]})
        label_box_dict[name].append(box)

    return label_box_dict, box_list





def select_object_num(dataset_dir,image_name):

    file = os.path.join(dataset_dir, DIRECTORY_IMAGES, image_name)
    img = cv2.imread(file)
    filename = image_name[:-4]
    # Read the XML annotation file.
    filename_annotation = os.path.join(dataset_dir, DIRECTORY_ANNOTATIONS, filename + '.xml')
    tree = ET.parse(filename_annotation)
    root = tree.getroot()

    # Image shape.
    size = root.find('size')
    shape = [int(size.find('height').text),
             int(size.find('width').text),
             int(size.find('depth').text)]
    # Find annotations.

    num=0
    for obj in root.findall("object"):
        num =num+1
        print (num)
        if num>1:
            print (filename_annotation)
            os.system("cp "+ filename_annotation +" "+ os.path.join(os.path.dirname(filename_annotation),".."))




        
def update_annotation(segment_dir, annotation_dir):
    for root, folds, files in os.walk(segment_dir, annotation_dir):
        if not len(files):
            continue

        fold = os.path.basename(root)
        for file in files:
            filename =file[:-4]
            image_na,image_me,label,ymin,xmin,ymax,xmax = filename.split("_")[:7]
            image_name = image_na+'_'+image_me
            ymin = ymin[4:]
            xmin = xmin[4:]
            ymax = ymax[4:]
            xmax = xmax[4:]

            if label==fold:
                continue

            annotation_file = os.path.join(annotation_dir, image_name + '.xml')
            tree = ET.parse(annotation_file)
            root = tree.getroot()
            print(annotation_file)
            for obj in root.findall("object"):
                anno_name = obj.find("name")
                bbox = obj.find('bndbox')
                ymin_ =bbox.find('ymin').text
                xmin_ =bbox.find('xmin').text
                ymax_ =bbox.find('ymax').text
                xmax_ =bbox.find('xmax').text

                if (ymin==ymin_ and xmin==xmin_ and ymax==ymax_ and xmax==xmax_):#iou=0.95
                    anno_name.text =fold
                    anno_name.set('updated', 'yes')
            
            tree.write(annotation_file)







def remove_object(segfile_dir,anno_source_dir,save_dir,hold =False):

    if not os.path.exists(save_dir):
        os.makedirs(os.path.join(save_dir,"Annotations"))
        os.makedirs(os.path.join(save_dir,"JPEGImages"))

    for anno_file in os.listdir(anno_source_dir):

        filename = anno_file[:-4]
        tree = ET.parse(os.path.join(anno_source_dir,anno_file))
        root = tree.getroot()
        for obj in root.findall('object'):
            name = obj.find('name').text
            bbox = obj.find('bndbox')
            ymin =bbox.find('ymin').text
            xmin =bbox.find('xmin').text
            ymax =bbox.find('ymax').text
            xmax =bbox.find('xmax').text

            segment_name=gene_SegImage_name(filename,name,ymin,xmin,ymax,xmax)
            if os.path.exists(os.path.join(segfile_dir,segment_name)):
                root.remove(obj)

        tree.write(os.path.join(save_dir,"Annotations",anno_file))






        # image_name,label,ymin,xmin,ymax,xmax = filename.split("_seg_")[:6]
        # print (label,"===",ymin,xmin,ymax,xmax)

        # Anno_file = os.path.join("Annotations",image_name+".xml")
        # JPEG_file = os.path.join("JPEGImages",image_name+".jpg")

        # annotation_file = os.path.join(source_dir,Anno_file)
        # tree = ET.parse(annotation_file)
        # root = tree.getroot()    

        # for obj in root.findall('object'):
        #     name = obj.find('name').text
        #     bbox = obj.find('bndbox')
        #     ymin_anno =bbox.find('ymin').text
        #     xmin_anno =bbox.find('xmin').text
        #     ymax_anno =bbox.find('ymax').text
        #     xmax_anno =bbox.find('xmax').text
        #     print ("-----------------------------------")
            
        #     if (ymin==ymin_anno and xmin==xmin_anno and ymax==ymax_anno and xmax==xmax_anno):
        #         root.remove(obj)
        #         print (name,"===",ymin_anno,xmin_anno,ymax_anno,xmax_anno,"+++++++")
        #     else:

        #         if name==label:

        #             print (filename)
        #             print ("ooooooooooooooooooooooooooooooooooooooooooooooo")
        #         print (name,"===",ymin_anno,xmin_anno,ymax_anno,xmax_anno)
            
            
        # print ("************************************************************")

        # tree.write(os.path.join(save_dir,Anno_file ))

        
    
# def add_object(anno_dir,add_anno_dir,save_dir):
    
#     if not os.path.exists(save_dir):
#         os.makedirs(os.path.join(save_dir,"Annotations"))

#     for anno_file in os.listdir(add_anno_dir):
    
#         tree = ET.parse(os.path.join(anno_dir,anno_file))
#         root = tree.getroot()
#         tree_add = ET.parse(os.path.join(add_anno_dir,anno_file))
#         root_add = tree_add.getroot()
#         for obj in root_add.findall('object'):

#             name = obj.find('name').text
#             bbox = obj.find('bndbox')
#             ymin =bbox.find('ymin').text
#             xmin =bbox.find('xmin').text
#             ymax =bbox.find('ymax').text
#             xmax =bbox.find('xmax').text

#             annotation = ET.Element("annotation")
#             imageobject = ET.SubElement(annotation, "object")
#             ET.SubElement(imageobject, "name").text =name
#             ET.SubElement(imageobject, "pose").text = 'Unspecified'
#             ET.SubElement(imageobject, "truncated").text = "0"
#             ET.SubElement(imageobject, "difficult").text = "0"

#             bndbox = ET.SubElement(imageobject, "bndbox")
#             ET.SubElement(bndbox, "xmin").text = str(xmin)
#             ET.SubElement(bndbox, "ymin").text = str(ymin)
#             ET.SubElement(bndbox, "xmax").text = str(xmax)
#             ET.SubElement(bndbox, "ymax").text = str(ymax)

#             root.append(imageobject)

#         tree.write(os.path.join(save_dir,"Annotations",anno_file),pretty_print=True)





# from generate_annotation_xml import gene_anno
# def add_object(anno_dir,add_anno_dir,save_dir):
    


#     for anno_file in os.listdir(add_anno_dir):
#         filename = anno_file[:-4]
#         boxes=[]
#         labels=[]

#         tree = ET.parse(os.path.join(anno_dir,anno_file))
#         root = tree.getroot()
#         tree_add = ET.parse(os.path.join(add_anno_dir,anno_file))
#         root_add = tree_add.getroot()

#         for obj in root.findall('object'):

#             name = obj.find('name').text
#             bbox = obj.find('bndbox')
#             ymin =bbox.find('ymin').text
#             xmin =bbox.find('xmin').text
#             ymax =bbox.find('ymax').text
#             xmax =bbox.find('xmax').text

#             boxes.append([ymin, xmin, ymax, xmax])
#             labels.append(name)

#         for obj in root_add.findall('object'):
    
#             name = obj.find('name').text
#             bbox = obj.find('bndbox')
#             ymin =bbox.find('ymin').text
#             xmin =bbox.find('xmin').text
#             ymax =bbox.find('ymax').text
#             xmax =bbox.find('xmax').text

#             boxes.append([ymin, xmin, ymax, xmax])
#             labels.append(name)

#         gene_anno(filename,boxes,save_dir,labels)






if __name__ == "__main__":


    """
    dataset_dir = "/home/linguosen/DiskA/NFSDATA_Data/zhanting/hardhat_head_zt_20230310_5m_640_640/anno"


    pool = multiprocessing.Pool(processes=8)
    for file in os.listdir(os.path.join(dataset_dir,DIRECTORY_IMAGES)):
        print (file)
        crop_box_img(dataset_dir,file)  #按照xml坐标切图

        # print (file)

        # if not os.path.exists(os.path.join(dataset_dir,DIRECTORY_ANNOTATIONS,file[:-4]+".xml")):
        #     print (file[:-4]+".xml","not find")
        #     continue

        '''
        # try:
        #     crop_box_img(dataset_dir,file)
        #     # select_object_num(dataset_dir,file)

        # except:
        #     print (file,"not found!!!")
        #     continue
        '''

        # pool.apply_async(crop_box_img,(dataset_dir,file))

    pool.close()
    pool.join()

    """
        

    ##############  update  ################

   
    segment_dir = "/1T/liufangtao/datas/stream2_images/crop_rect1.5/result"
    annotation_dir = "/1T/liufangtao/datas/stream2_images/corpxml_rect1.5"
    update_annotation(segment_dir, annotation_dir)

    
    ###############  remove ###########


    """
    segfile_dir = "/home/linguosen/DiskA/NFSDATA_Data/zhanting/hardhat_head_zt_20230310_5m_640_640/anno/SEGMENT/other"
    source_dir = "/home/linguosen/DiskA/NFSDATA_Data/zhanting/hardhat_head_zt_20230310_5m_640_640/anno/"

    anno_source_dir= os.path.join(source_dir,"Annotations")
    anno_save_dir = os.path.join(anno_source_dir,"..","anno_obj_removed")
    remove_object(segfile_dir,anno_source_dir,anno_save_dir,hold =True)

    """



    ############### add ###########


    """
    anno_dir = "/media/guosen/Dataset_disk/exchange_data/Judan/zgc20180425_result/result/loukuang/anno/Annotations"
    add_anno_dir = "/media/guosen/Dataset_disk/exchange_data/Judan/zgc20180425_result/result/loukuang/Annotations"
    save_dir = os.path.join(anno_dir,"..","added_new_object")
    add_object(anno_dir,add_anno_dir,save_dir)

    """