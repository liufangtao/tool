import os
import sys
import shutil

import annotation_voc_xml as annotation_voc_xml
import annotation_yolo
import annoutils


import cv2



def voc2yolo(xml_dir,save_dir):

    # labels=['Broken', 'Burr', 'Chip', 'Crack', 'Waterstains','dirty','BigBurr','water','split']
    labels=["person","hardhat","head","safetyvest","hand"]
    # labels=["aodian","diaomo", "huashang", "zangwu","shike"]
    # labels=['diaomo','shike','zangwu','huashang']
    # labels=['broken', 'burr', 'chip']
    xml_files=sorted(os.listdir(xml_dir))
    for idx,txt_file in enumerate(xml_files):
        print(idx+1,"/",len(xml_files),txt_file)
        filename = os.path.splitext(txt_file)[0]
        width,height,anno_list = annotation_voc_xml.get_xml_info(os.path.join(xml_dir,txt_file))
        class_id_list=[]
        boxes=[]
        for info in anno_list:
            name,xmin,ymin,xmax,ymax = info
            if name not in labels:
                labels.append(name)
            id = labels.index(name)
            class_id_list.append(id)

            xyxy=[xmin,ymin,xmax,ymax]
            center_x, center_y, rect_w, rect_h = annoutils.xyxy2center_f(xyxy, height, width)
            boxes.append([center_x, center_y, rect_w, rect_h])
            
        annotation_yolo.save_anno_yolo(boxes,class_id_list,save_dir,filename)
    
    print(labels)
    return labels        



def yolo2voc(txt_dir,images_dir,labels_list,save_dir):

    

    txt_files=sorted(os.listdir(txt_dir))
    for idx,txt_file in enumerate(txt_files):
        print(idx+1,"/",len(txt_files))
        filename = os.path.splitext(txt_file)[0]
        print(filename)
        boxes, class_id_list = annotation_yolo.parse_yolo_anno(os.path.join(txt_dir,txt_file))
        if os.path.isfile(os.path.join(images_dir,filename+".png")):
            image = cv2.imread(os.path.join(images_dir,filename+".png"))
        else:
            image = cv2.imread(os.path.join(images_dir,filename+".jpg"))
        height,width = image.shape[:2]

        xyxy_boxes=[]
        labels=[]
        for idx,box in enumerate(boxes):
            center_x, center_y, rect_w, rect_h = box
            xmin, ymin, xmax, ymax = annoutils.center_f2xyxy(center_x, center_y, rect_w, rect_h, height, width)
            # print(xmin, ymin, xmax, ymax)
            xyxy_boxes.append([ymin, xmin, ymax, xmax])
            labels.append(labels_list[class_id_list[idx]])
        
        annotation_voc_xml.gene_anno(filename,xyxy_boxes,labels,width,height,save_dir)
        



if __name__ == "__main__":
    base_dir="/1T/liufangtao/datas/matrix/datas"


    # projects="广州数据/明厨亮灶images_0528/kitcken"
    # image_fold = os.path.join(base_dir,projects,"images")
    ############################# fix_voc_anno  #############################
    '''    
    anno_fold = os.path.join(base_dir,projects,"Annotations")
    save_anno_fold = os.path.join(base_dir,projects,"annotations")
    if not os.path.exists(save_anno_fold):
        os.system("mkdir "+save_anno_fold)

    annotation_voc.fix_voc_anno(image_fold,anno_fold,save_anno_fold)

    # exit()
    '''


    #############################     voc2yolo        #####################################

    projects="person_hardhat_head_safetyvest_hand_unmask_mask"
    
    xml_dir = os.path.join(base_dir,projects,"xmls")
    save_dir = os.path.join(base_dir,projects,"labels")
    labels_list=voc2yolo(xml_dir,save_dir)
    # # exit()s
    # shutil.rmtree(xml_dir)

    #######################################################################################
    #############################     yolo2voc        #####################################
    #######################################################################################
    
    labels_list=["yi_wu","can_jiao","ci_shang","hua_shang"]
    # labels_list=["aodian","diaomo", "huashang", "zangwu","shike"]
    # labels_list=['Broken', 'Burr', 'Chip', 'Crack', 'Waterstains','dirty','BigBurr','water','split']
    # labels_list=['diaomo','shike','zangwu','huashang']
    # # # # # projects="Annotations"

    # images_dir = os.path.join(base_dir,projects,"images")
    # txt_dir = os.path.join(base_dir,projects,"labels")
    # save_dir = os.path.join(base_dir,projects)
    # yolo2voc(txt_dir,images_dir,labels_list,save_dir)

    # os.system("cp -r "+images_dir+" "+os.path.join(base_dir,projects+"_voc","JPEGImages"))
    