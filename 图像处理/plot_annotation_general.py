

import sys
import os
import cv2
import annoutils
import annotation_yolo
import 图像处理.annotation_voc_xml as annotation_voc_xml
from multiprocessing import Pool


resize_rate=0.5;rectange_width=2
# resize_rate=1;rectange_width=1

color_list=[(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255), (0, 0, 0),
            (100, 155, 0), (100, 0, 255), (255, 100, 0), (255, 255, 100), (100, 255, 255), (255, 100, 255), (100, 0, 0)]

print(color_list)
def base_plot(filename,box_type,image_np,box_list,label_list,save_dir,total_labels):
    image_h,image_w = image_np.shape[:2]
    for idx,box in enumerate(box_list):

        if box_type =="center":
            center_x,center_y,rect_w,rect_h = box
            xmin,ymin,xmax,ymax = annoutils.center_f2xyxy(center_x,center_y,rect_w,rect_h,image_h,image_w)
        elif box_type =="xyxy":
            xmin,ymin,xmax,ymax = box

        label =label_list[idx]
        color =color_list[total_labels.index(label)]
        
        cv2.rectangle(image_np, (xmin,ymin), (xmax, ymax), color, rectange_width)
        cv2.putText(image_np,label_list[idx],(xmin,ymin+10),cv2.FONT_HERSHEY_COMPLEX,0.8,color,2)

    image_np = cv2.resize(image_np,(int(image_w*resize_rate),int(image_h*resize_rate)))
    if save_dir:
        if not os.path.exists(save_dir):
            os.system("mkdir -p "+save_dir)

        has_result_dir = os.path.join(save_dir,"has_result")
        if not os.path.exists(has_result_dir):
            os.system("mkdir -p "+has_result_dir)

        unhas_result_dir = os.path.join(save_dir,"unhas_result")
        if not os.path.exists(unhas_result_dir):
            os.system("mkdir -p "+unhas_result_dir)

        if len(box_list):
            cv2.imwrite(os.path.join(has_result_dir,filename+".jpg"),image_np)   
        else:
           cv2.imwrite(os.path.join(unhas_result_dir,filename+".jpg"),image_np)         
        
    else:
        cv2.imshow("show",image_np)
        cv2.waitKey(1000)        



def plot_yolo_anno(images_dir,anno_dir,save_dir,total_labels):

    pool = Pool(processes=30)
    
    files_num = len(os.listdir(images_dir))
    for idx,imgfile in enumerate(sorted(os.listdir(images_dir))):
        filename = os.path.splitext(imgfile)[0]
        annofile = os.path.join(anno_dir,filename+".txt")
        if not os.path.exists(annofile):
            print(annofile ,"not exist!")
            continue

        image_np = cv2.imread(os.path.join(images_dir,imgfile))
        print(idx,"/",files_num,annofile)
        box_list,class_id_list = annotation_yolo.parse_yolo_anno(annofile)
        label_list = [total_labels[id] for id in class_id_list]
        pool.apply(base_plot, args=(filename,"center",image_np,box_list,label_list,save_dir,total_labels))
    
    print(total_labels)



def plot_yolo_anno_useanno(images_dir,anno_dir,save_dir,total_labels):

    pool = Pool(processes=20)
    
    files_num = len(os.listdir(anno_dir))
    for idx,annofile in enumerate(sorted(os.listdir(anno_dir))):
        filename = os.path.splitext(annofile)[0]
        imagefile = os.path.join(anno_dir,filename+".jpg")
        if not os.path.exists(imagefile):
            print(imagefile ,"not exist!")
            continue

        image_np = cv2.imread(os.path.join(images_dir,imagefile))
        print(idx,"/",files_num,annofile)
        box_list,class_id_list = annotation_yolo.parse_yolo_anno(annofile)
        label_list = [total_labels[id] for id in class_id_list]

        pool.apply(base_plot, args=(filename,"center",image_np,box_list,label_list,save_dir,total_labels))
    
    print(total_labels)




def plot_voc_anno(images_dir,anno_dir,save_dir):
    pool = Pool(processes=20)
    files_num = len(os.listdir(images_dir))
    for idx,imgfile in enumerate(sorted(os.listdir(images_dir))):
        filename,ext = os.path.splitext(imgfile)[:2]
        image_np = cv2.imread(os.path.join(images_dir,imgfile))
        annofile = os.path.join(anno_dir,filename+".xml")

        if not os.path.exists(annofile):
            print(annofile ,"not exist!")
            continue

        print(idx,"/",files_num,annofile)
        #  xmin,ymin,xmax,ymax
        label_box_dict = annotation_voc_xml.parse_voc_anno(annofile)
        box_list=[]
        label_list=[]
        for label in label_box_dict:
            for box in label_box_dict[label]:
                box_list.append(box)
                label_list.append(label)
            if label not in total_labels:
                total_labels.append(label)
        
        pool.apply(base_plot, args=(filename,"xyxy",image_np,box_list,label_list,save_dir,total_labels))

    print(total_labels)


if __name__ == "__main__":

    base_dir_images = "/home/linguosen/DiskA/NFSDATA_Data"
    base_dir="/home/linguosen/DiskA/NFSDATA_Data/"

    resize_rate=1;rectange_width=1
    # resize_rate=0.5;rectange_width=2
    ################################################
    ##################### YOLO  #####################
    ################################################

    # base_dir = "/home/linguosen/DiskA/WareHouse_Data/HelmetDetection/"
    # base_dir="/home/linguosen/DiskA/WareHouse_Data/Hardhat"
    # images_dir =os.path.join(base_dir,"Images")
    # anno_dir = os.path.join(base_dir,"labels") 
    # labels =["hardhat","head","person"]

    # base_dir ="/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA_linguosen/images/Hardhat"
    # images_dir =os.path.join(base_dir,"images")
    # anno_dir = os.path.join(base_dir,"hand_labels") 
    # save_dir = os.path.join(base_dir,"plot_result")  
    # labels =["hand"]

    # plot_yolo_anno(images_dir,anno_dir,save_dir)

    ################################################
    ##################### VOC  #####################
    ################################################

    # base_dir = "/home/linguosen/DiskA/NFSDATA_Data/HandsDataSet/all_dataset/coco_hand_yolo/"
    # base_dir = "/home/linguosen/DiskA/NFSDATA_Data/Hardhat/"
    # base_dir="/home/linguosen/DiskA/NFSDATA_Data/VOC2020_fire"

    # images_dir =os.path.join(base_dir,"JPEGImages")
    # anno_dir = os.path.join(base_dir,"Annotations") 


    # base_dir = "/home/linguosen/DiskA/NFSDATA_Data/DaTangXiangYang"
    # images_dir =os.path.join(base_dir,"images")
    # anno_dir = os.path.join(base_dir,"labels_merged/hand_hardhat_head");total_labels=["hand","hardhat","head"]
    # anno_dir = os.path.join(base_dir,"new_labels");total_labels=["hand","hardhat","head"]
    # anno_dir = os.path.join(base_dir,"labels_divided/head");total_labels=["head"]
    # save_dir = os.path.join(base_dir,"plot_result","person")  


    '''
    projects="ManuVisionData/工业金属表面缺陷数据集GC10-DET/Defects_location_for_metal_surface"
    images_dir =os.path.join(base_dir,projects,"JPEGImages")
    anno_dir = os.path.join(base_dir,projects,"Annotations");total_labels=[]
    save_dir = os.path.join(base_dir,projects,"result")
    plot_voc_anno(images_dir,anno_dir,save_dir)
    exit()
    '''


    ################################################
    ##################### YOLO  #####################
    ################################################

    # anno_dir = os.path.join(base_dir,"labels_test/person");total_labels=["person"]
    # plot_yolo_anno(images_dir,anno_dir,save_dir,total_labels)


    resize_rate=0.5;rectange_width=2
    # resize_rate=1;rectange_width=1
    # images_dir = os.path.join(base_dir_images,"YanHua/images")
    # anno_dir = os.path.join(base_dir_images,"YanHua/labels/1219_person_fix");total_labels=["person"]
    # save_dir = os.path.join(base_dir_images,"YanHua/plot_result","1219_person_fix")  


    # images_dir = os.path.join(base_dir_images,"Fire/dataset/images")
    # anno_dir = os.path.join(base_dir_images,"Fire/dataset/labels");total_labels=["smoke","fire"]
    # save_dir = os.path.join(base_dir_images,"Fire/dataset/plot_result")  

    '''
    images_dir = "/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA_linguosen/images/five/images"
    anno_dir = "/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA_linguosen/images/five/labels";total_labels=["hardhat","head"]
    save_dir = "/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA_linguosen/images/five/result"

    plot_yolo_anno(images_dir,anno_dir,save_dir,total_labels)
    '''

    '''
    projects="Fire/VOC2020_fire"
    images_dir = os.path.join(base_dir,projects,"images")
    anno_dir = os.path.join(base_dir,projects,"labels");total_labels=["fire"]
    save_dir = os.path.join(base_dir,projects,"result_")
    plot_yolo_anno(images_dir,anno_dir,save_dir,total_labels)
    '''



    # '''
    projects="mtstudio/2023-06-06_10-58-49"
    images_dir = os.path.join(base_dir,projects,"images")
    anno_dir = os.path.join(base_dir,projects,"labels");total_labels=[str(i) for i in range(100)];total_labels=["shuiban","youban","chongkong"]
    save_dir = os.path.join(base_dir,projects,"result/")
    plot_yolo_anno(images_dir,anno_dir,save_dir,total_labels)
    # '''