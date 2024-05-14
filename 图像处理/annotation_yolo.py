
import os
import sys
import cv2

import annoutils
# from utils import
import threading


def  save_image_yolo(image,save_dir,filename):
    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)
    cv2.imwrite(os.path.join(save_dir,filename+".png"),image)



def  save_anno_yolo(boxes,class_id_list,save_dir,filename):
    # center_x,center_y,rect_w,rect_h

    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)

    file = os.path.join(save_dir, filename+".txt")
    file_write_obj = open(file, 'a')
    file_write_obj.seek(0)
    file_write_obj.truncate() 
    for i,box in enumerate(boxes):
        #### box = x_center, y_center, width, height
        file_write_obj.write(str(class_id_list[i]))
        file_write_obj.write(" ")
        for i in range(4):
            box[i] = max(min(box[i],1.),0.)
            file_write_obj.write(("%f" % box[i]))
            file_write_obj.write(" ")

        file_write_obj.write('\n')
    
    file_write_obj.close()






def gene_SegImage_name(filename,name,ymin,xmin,ymax,xmax):
    segment_name = "{0}_C{1}_ymin{2}_xmin{3}_ymax{4}_xmax{5}.jpg".format(filename,name,ymin,xmin,ymax,xmax)
    return segment_name




def base_crop(filename_list,images_dir,labels_dir,dst_dir,expand_method,expand_rate):
    total_num = len(filename_list)
    for idx,filename in enumerate(filename_list):
        label_file = os.path.join(labels_dir,filename+".txt")
        image_file_jpg = os.path.join(images_dir,filename+".jpg")
        image_file_png = os.path.join(images_dir,filename+".png")

        image_file=""
        if  os.path.exists(image_file_jpg):
            image_file = image_file_jpg
        elif os.path.exists(image_file_png):
            image_file = image_file_png
        else:
            continue


        image = cv2.imread(image_file)
        print (idx,"/",total_num, image_file)

        for line in open(label_file):
            info = line.split(" ")
            class_id = info[0]
            center_x,center_y,rect_w,rect_h = [float(i) for i in info[1:5]]
            height, width = image.shape[:2]

            if str(class_id) not in ["0","2","3"]:
                continue
            # center_x,center_y,rect_w,rect_h = annoutils.expand_center(center_x,center_y,rect_w,rect_h,expand_method,expand_rate)

            # print (rect_w,rect_h)
            # continue
            # xmin, ymin, xmax, ymax = annoutils.center_f2xyxy(center_x,center_y,rect_w,rect_h,height, width)

            xmin, ymin, xmax, ymax = annoutils.expand_center(center_x,center_y,rect_w,rect_h,expand_method,expand_rate,height, width)

            crop_img = image.copy()[ymin:ymax,xmin:xmax]

            segmentname = gene_SegImage_name(filename,str(class_id),ymin,xmin,ymax,xmax)
            sub_dst_dir = os.path.join(dst_dir,str(class_id))
            if not os.path.exists(sub_dst_dir):
                os.system("mkdir -p "+sub_dst_dir)
            cv2.imwrite(os.path.join(sub_dst_dir,segmentname),crop_img)
            # cv2.waitKey(1)


def crop_image_from_yolo_anno(src_dir,dst_dir):
    
    images_dir = os.path.join(src_dir,"images")
    labels_dir = os.path.join(src_dir,"labels")

    files= sorted(os.listdir(labels_dir))

    thread_num=6
    sub_files_list = [files[i:i+len(files)//thread_num] for i in  range(0, len(files), len(files)//thread_num)]

    
    ths=[]
    for sub_files_name in sub_files_list:
        # print (len(sub_files_name))
        sub_files_name = [f[:-4] for f in sub_files_name]
        t = threading.Thread(target=base_crop, args=(sub_files_name,images_dir,labels_dir,dst_dir))
        t.start()
        ths.append(t)
        

    for t in ths:
        t.join()



   
def parse_yolo_anno(annofile,anno_type="center"):
    boxes=[]
    class_id_list=[]
    for line in open(annofile):
        line_content = [l for l in line.split(" ") if l]

        class_id  = int(line_content[0])

        if anno_type=="center":
            center_x,center_y,rect_w,rect_h = [float(i) for i in line_content[1:5]]
            boxes.append([center_x,center_y,rect_w,rect_h])
        elif anno_type=="xyxy":
            x_min, x_max, y_min, y_max = [int(i) for i in line_content[1:5]]
            boxes.append([x_min, x_max, y_min, y_max])
        elif anno_type=="xyxy_f":
            x_min_f, x_max_f, y_min_f, y_max_f = [float(i) for i in line_content[1:5]]
            boxes.append([x_min_f, x_max_f, y_min_f, y_max_f])

        class_id_list.append(class_id)

    return boxes, class_id_list    



   
def parse_mv_boxes(mv_boxes,model_use_label):
    boxes=[]
    class_id_list=[]
    for box in mv_boxes:
        if box["label"] in model_use_label:
            boxes.append([box["x_center"], box["y_center"], box["w"], box["h"]])
            class_id_list.append(box["class_id"])

    return boxes, class_id_list    




def center_boxes2xyxy_boxes(boxes,height, width):

    xyxy_boxes=[]
    for box in boxes:
        center_x,center_y,rect_w,rect_h = box
        xmin, ymin, xmax, ymax = annoutils.center_f2xyxy(center_x,center_y,rect_w,rect_h,height, width)
        xyxy_boxes.append([xmin, ymin, xmax, ymax])

    return xyxy_boxes

def center_boxes2yxyx_boxes(boxes,height, width):
    
    xyxy_boxes=[]
    for box in boxes:
        center_x,center_y,rect_w,rect_h = box
        xmin, ymin, xmax, ymax = annoutils.center_f2xyxy(center_x,center_y,rect_w,rect_h,height, width)
        xyxy_boxes.append([ymin,xmin, ymax,  xmax])

    return xyxy_boxes  





def CalculateOverlap(xmin0, ymin0, xmax0, ymax0, xmin1, ymin1, xmax1, ymax1):
    w = max(0.0, min(xmax0, xmax1) - max(xmin0, xmin1))
    h = max(0.0, min(ymax0, ymax1) - max(ymin0, ymin1))
    i = w * h
    u = (xmax0 - xmin0) * (ymax0 - ymin0) + (xmax1 - xmin1) * (ymax1 - ymin1) - i

    if u <= 0.0:
        return 0.0

    return i / u



def iou_center(box_src,box_filter):
    src_center_x,src_center_y,src_rect_w,src_rect_h = box_src
    src_xmin_f, src_ymin_f, src_xmax_f, src_ymax_f = annoutils.center_f2xyxy_f(src_center_x,src_center_y,src_rect_w,src_rect_h)
    filt_center_x,filt_center_y,filt_rect_w,filt_rect_h = box_filter
    filt_xmin_f, filt_ymin_f, filt_xmax_f, filt_ymax_f = annoutils.center_f2xyxy_f(filt_center_x,filt_center_y,filt_rect_w,filt_rect_h)

    score=CalculateOverlap(src_xmin_f, src_ymin_f, src_xmax_f, src_ymax_f,filt_xmin_f, filt_ymin_f, filt_xmax_f, filt_ymax_f)

    return score



def boxes_filter_iou(boxes,class_id_list,rm_box_list,rate):
    new_boxes=[]
    new_class_id_list=[]
    for i,box in enumerate(boxes):
        need_rm=0
        for rm_box in rm_box_list:
            score = iou_center(box,rm_box)
            if score>rate:
                need_rm=1
                break
        if need_rm:
            continue

        center_x,center_y,w,h = box
        if w/h>0.8:
            continue


        new_boxes.append(box)
        new_class_id_list.append(class_id_list[i])

    return new_boxes,new_class_id_list





def remove_box(anno_dir,rm_box_list,save_dir,rate):
    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)

    files =sorted(os.listdir(anno_dir))
    for indx,file in enumerate(files):
        print(indx+1,"/",len(files))
        if file == "classes.txt":
            continue
        annofile = os.path.join(anno_dir,file)
        boxes, class_id_list = parse_yolo_anno(annofile,anno_type="center")
        new_boxes,new_class_id_list = boxes_filter_iou(boxes,class_id_list,rm_box_list,rate)
        save_anno_yolo(new_boxes,new_class_id_list,save_dir,file[:-4])


def boxes_filter_iou_self(boxes,class_id_list,rate):
    new_boxes=[]
    new_class_id_list=[]
    for i,box in enumerate(boxes):
        flag=0
        for rm_box in new_boxes:
            score = iou_center(box,rm_box)
            if score>rate:
                flag=1
        if not flag:
            new_boxes.append(box)
            new_class_id_list.append(class_id_list[i])

    return new_boxes,new_class_id_list



    
def remove_box_self(anno_dir,save_dir,rate):
    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)

    for file in sorted(os.listdir(anno_dir)):
        if file == "classes.txt":
            continue
        annofile = os.path.join(anno_dir,file)
        boxes, class_id_list = parse_yolo_anno(annofile,anno_type="center")
        new_boxes,new_class_id_list = boxes_filter_iou_self(boxes,class_id_list,rate)
        save_anno_yolo(new_boxes,new_class_id_list,save_dir,file[:-4])


def rename_class_id_self(anno_dir,save_dir,new_id_dict):
    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)

    for file in sorted(os.listdir(anno_dir)):
        if file == "classes.txt":
            continue
        annofile = os.path.join(anno_dir,file)
        boxes, class_id_list = parse_yolo_anno(annofile,anno_type="center")

        # new_class_id_list =[new_id for i in range(len(class_id_list))]

        new_class_id_list=[]
        for id in class_id_list:
            new_class_id_list.append(new_id_dict[id])

        save_anno_yolo(boxes,new_class_id_list,save_dir,file[:-4])


    
    




if __name__ == "__main__":

    # src_dir="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/result/phone"
    # images_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/images/20210611"
    # labels_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/labels"
    # dst_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/croped/phone"



    ################ base_crop ##################

    # '''  
    base_dir="/home/linguosen/DiskA/NFSDATA_Data/ManuVisionData/工业金属表面缺陷数据集GC10-DET/Defects_location_for_metal_surface/t2i"

    filenames_dir = os.path.join(base_dir,"labels")
    images_dir = os.path.join(base_dir,"images")
    labels_dir =os.path.join(base_dir,"labels")


    filename_list = [os.path.splitext(file)[0] for file in sorted(os.listdir(filenames_dir))]

    dst_dir =os.path.join(base_dir,"crop_rect")    
    base_crop(filename_list,images_dir,labels_dir,dst_dir,expand_method="bigger_rect",expand_rate=1)

    # dst_dir =os.path.join(base_dir,"crop")    
    # base_crop(filename_list,images_dir,labels_dir,dst_dir,expand_method="normal",expand_rate=1)

    # '''

    exit()
    ######################################################
    ###############   rm box  ###########################
    ######################################################
    '''
    anno_dir ="/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA/images/showroom_demo_hand/run5l/158/20210615-20210627/20210615-20210619/158_images_ok_20210615-20210619-A_labels"
    rm_box =[0.822917 ,0.905556, 0.018750, 0.040741  ]
    save_dir ="/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA/images/showroom_demo_hand/run5l/158/20210615-20210627/20210615-20210619/158_images_ok_20210615-20210619-A_labels_"
    remove_box(anno_dir,rm_box,save_dir,rate=0.1)
    '''

    '''
    anno_dir ="/home/linguosen/DiskA/NFSDATA_Data/YanHua/labels/1219_person"
    rm_box_list =[[0.678125, 0.914583, 0.368750, 0.16666],
    [0.677344, 0.930208, 0.382812, 0.139583],
    [0.678125, 0.879167, 0.359375, 0.233333],
    [0.682031, 0.932292, 0.364062, 0.131250],
    [0.675000, 0.935417, 0.375000, 0.129167],
    [0.680469, 0.934375, 0.385938, 0.131250],
    [0.675781, 0.903125, 0.395313, 0.185417],
    [0.667969, 0.891667, 0.395313, 0.216667],
    [0.670313, 0.904167, 0.387500, 0.183333],
    [0.668750, 0.896875, 0.390625, 0.202083],
    [0.666406, 0.905208, 0.385938, 0.189583]]
    save_dir ="/home/linguosen/DiskA/NFSDATA_Data/YanHua/labels/1219_person_fix"
    remove_box(anno_dir,rm_box_list,save_dir,rate=0.7)
    '''

    #################################################################################
    #################################################################################

    # anno_dir ="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/local_image/yolo_anno_data/labels"
    # save_dir ="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/local_image/yolo_anno_data/labels_"
    # remove_box_self(anno_dir,save_dir,rate=0.9)

    '''
    anno_dir ="/media/linguosen/DiskB/DataSetHouse/CAT-DOG/labels"
    save_dir ="/media/linguosen/DiskB/DataSetHouse/CAT-DOG/labels_"

    new_id_dict={15:0,16:1}
    rename_class_id_self(anno_dir,save_dir,new_id_dict)
    '''