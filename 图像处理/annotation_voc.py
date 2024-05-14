
import os
import sys
import cv2
sys.path.append("/home/linguosen/DiskA/CodeWareHouse/BasicToolHouse/AnnotationTool/")
import annoutils
# from utils import
import threading
import xml.etree.ElementTree as ET


def gene_anno(filename,boxes,labels,width,height,exportdir):

    exportdir = os.path.join(exportdir,"Annotations")
    if not os.path.exists(exportdir):
        os.makedirs(exportdir)

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "VOC2007"
    ET.SubElement(annotation, "filename").text = filename+".jpg"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    ET.SubElement(annotation, "segmented").text = "0"

    for idx,box in enumerate(boxes):
        imageobject = ET.SubElement(annotation, "object")
        ET.SubElement(imageobject, "name").text =str(labels[idx])
        ET.SubElement(imageobject, "pose").text = str(idx)
        ET.SubElement(imageobject, "truncated").text = "0"
        ET.SubElement(imageobject, "difficult").text = "0"

        bndbox = ET.SubElement(imageobject, "bndbox")
        ymin, xmin, ymax, xmax = box
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)

    savedir = os.path.join(exportdir,filename +".xml")
    tree = ET.ElementTree(annotation)
    tree.write(savedir)



def gene_SegImage_name(filename,name,ymin,xmin,ymax,xmax):
    segment_name = "{0}_C{1}_ymin{2}_xmin{3}_ymax{4}_xmax{5}.png".format(filename,name,ymin,xmin,ymax,xmax)
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

        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))

        box = [xmin,ymin,xmax,ymax]
        box_list.append(box)
        
        if name not in label_box_dict.keys():
            label_box_dict.update({name:[]})
        label_box_dict[name].append(box)

    return label_box_dict, box_list


   
def parse_voc_anno(annofile):
    label_box_dict, box_list = get_label_boxes_from_xml(annofile)
    return label_box_dict


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



def boxes_filter_iou(boxes,class_id_list,boxfilter,rate):
    new_boxes=[]
    new_class_id_list=[]
    for i,box in enumerate(boxes):
        score = iou_center(box,boxfilter)
        if score>rate:
            continue

        new_boxes.append(box)
        new_class_id_list.append(class_id_list[i])

    return new_boxes,new_class_id_list





def remove_box(anno_dir,boxfilter,save_dir,rate):
    if not os.path.exists(save_dir):
        os.system("mkdir -p "+save_dir)

    for file in sorted(os.listdir(anno_dir)):
        if file == "classes.txt":
            continue
        annofile = os.path.join(anno_dir,file)
        boxes, class_id_list = parse_yolo_anno(annofile,anno_type="center")
        new_boxes,new_class_id_list = boxes_filter_iou(boxes,class_id_list,boxfilter,rate)
        save_anno_yolo(new_boxes,new_class_id_list,save_dir,file[:-4])


def boxes_filter_iou_self(boxes,class_id_list,rate):
    new_boxes=[]
    new_class_id_list=[]
    for i,box in enumerate(boxes):
        flag=0
        for boxfilter in new_boxes:
            score = iou_center(box,boxfilter)
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

def fix_wh(filename_annotation,image_w,image_h,save_filename_annotation):
    try:
        annotation = ET.parse(filename_annotation)
    except:
        print (filename_annotation+"not found !")

    root = annotation.getroot()
    size = root.find("size")
    width = size.find("width")
    height = size.find("height")

    width.text = str(image_w)
    height.text = str(image_h)

    tree = ET.ElementTree(root)
    tree.write(save_filename_annotation)



def fix_voc_anno(image_fold,anno_fold,save_anno_fold):
    files = sorted(os.listdir(image_fold))
    for idx, file in enumerate(files):
        print(idx+1,"/",len(files))
        image_file = os.path.join(image_fold,file)
        image = cv2.imread(image_file)
        height,width = image.shape[:2]
        filename_annotation = os.path.join(anno_fold,os.path.splitext(file)[0]+".xml")
        save_filename_annotation = os.path.join(save_anno_fold,os.path.splitext(file)[0]+".xml")
        if not os.path.exists(filename_annotation):
            print(filename_annotation," not exist!")
            return
        else:
            fix_wh(filename_annotation,width,height,save_filename_annotation)

    
def get_xml_info(xml_file):


    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    anno_list=[]
    for obj in root.findall("object"):
        name = obj.find("name").text
        

        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))

        anno_list.append([name,xmin,ymin,xmax,ymax])

    return w,h,anno_list




def get_xml_info_special(xml_file):


    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    anno_list=[]
    for obj in root.findall("draw_frame_list"):
        name = obj.find("label_name").text
        

        bbox = obj.find('bndbox')
        ymin = int(float(bbox.find('ymin').text))
        xmin = int(float(bbox.find('xmin').text))
        ymax = int(float(bbox.find('ymax').text))
        xmax = int(float(bbox.find('xmax').text))

        anno_list.append([name,xmin,ymin,xmax,ymax])

    return w,h,anno_list




if __name__ == "__main__":

    # src_dir="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/result/phone"
    # images_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/images/20210611"
    # labels_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/labels"
    # dst_dir = "/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/158/croped/phone"

    # base_dir="/home/linguosen/DiskA/NFSDATA_Data/"

    ################ base_crop ##################
    # '''  
    base_dir="/1T/liufangtao/datas/stream2_images"

    filenames_dir = os.path.join(base_dir,"labels")
    images_dir = os.path.join(base_dir,"images")
    labels_dir =os.path.join(base_dir,"labels")
    filename_list = [os.path.splitext(file)[0] for file in sorted(os.listdir(filenames_dir))]

    dst_dir =os.path.join(base_dir,"crop_rect1.5")    
    base_crop(filename_list,images_dir,labels_dir,dst_dir,expand_method="bigger_rect",expand_rate=1.5)

    # dst_dir =os.path.join(base_dir,"crop")    
    # base_crop(filename_list,images_dir,labels_dir,dst_dir,expand_method="normal",expand_rate=1)

    # '''

    ######################### remove_box #########################
    '''
    anno_dir ="/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA/images/showroom_demo_hand/run5l/158/20210615-20210627/20210615-20210619/158_images_ok_20210615-20210619-A_labels"
    boxfilter =[0.822917 ,0.905556, 0.018750, 0.040741  ]
    save_dir ="/home/linguosen/DiskA/CodeWareHouse/MatrixVision/AIbox/NFSDATA/images/showroom_demo_hand/run5l/158/20210615-20210627/20210615-20210619/158_images_ok_20210615-20210619-A_labels_"
    remove_box(anno_dir,boxfilter,save_dir,rate=0.1)
    '''


    ######################### remove_box_self #########################
    '''    
    anno_dir ="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/local_image/yolo_anno_data/labels"
    save_dir ="/home/linguosen/DiskA/CodeWareHouse/DeepLearningHouse/pytorch/RKNNseries/showroom_demo_hand/run5l/local_image/yolo_anno_data/labels_"
    remove_box_self(anno_dir,save_dir,rate=0.9)
    '''


    ######################### rename_class_id_self #########################
    '''
    anno_dir ="/media/linguosen/DiskB/DataSetHouse/CAT-DOG/labels"
    save_dir ="/media/linguosen/DiskB/DataSetHouse/CAT-DOG/labels_"

    new_id_dict={15:0,16:1}
    rename_class_id_self(anno_dir,save_dir,new_id_dict)
    '''


    ############################# fix_voc_anno  #############################
    '''
    projects="d"
    image_fold = os.path.join(base_dir,projects,"images")
    anno_fold = os.path.join(base_dir,projects,"annotations")
    save_anno_fold = os.path.join(base_dir,projects,"annotations_fixed")
    if not os.path.exists(save_anno_fold):
        os.system("mkdir "+save_anno_fold)

    fix_voc_anno(image_fold,anno_fold,save_anno_fold)
    '''
