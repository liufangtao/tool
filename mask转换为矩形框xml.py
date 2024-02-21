import os
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
import cv2

def find_horizontal_ranges(mask):
    white_pixels = np.where(mask == 255)
    y_mask, x_mask, height_mask, width_maks = cv2.boundingRect(np.column_stack(white_pixels))
    ranges = []
    row_y0 =[]
    row_x1 =[]
    width, height = mask.shape
    ds=[]
    if height_mask/width_maks >= 1:
        for y in range(height):
            in_range = False
            row_x0 = []
            for x in range(width):
                # pixel_value = mask.getpixel((x, y))
                pixel_value = mask[y,x]
                if pixel_value == 255:
                    row_x0.append(x)
                    if y%5 ==0 and y not in row_y0:
                        ranges.append([x, y])
                        row_y0.append(y)
            if not row_x0:
                continue          
            max_d = max(row_x0)
            min_d = min(row_x0)
            ds.append(max_d-min_d)
    else:
        for x in range(height):
            in_range = False
            row_y1 = []
            for y in range(width):
                # pixel_value = mask.getpixel((x, y))
                pixel_value = mask[y,x]
                if pixel_value == 255:
                    row_y1.append(y)
                    if x%5 ==0 and x not in row_x1:
                        ranges.append([x, y])
                        row_x1.append(x)
            if not row_y1:
                continue          
            max_d = max(row_y1)
            min_d = min(row_y1)
            ds.append(max_d-min_d)


    return ranges, ds

# 输入和输出文件夹路径
input_images = "/1T/liufangtao/datas/glass/images_draw"
input_mask_folder = "/1T/liufangtao/datas/glass/images_draw_out"
output_xml_folder = "/1T/liufangtao/datas/glass/images_drawxmls"

os.makedirs(output_xml_folder, exist_ok=True)

mask_files = os.listdir(input_mask_folder)
for mask_file in mask_files:
    if mask_file.endswith(".png"):
        mask_path = os.path.join(input_mask_folder, mask_file)
        # mask = Image.open(mask_path).convert("L")
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        ranges, ds = find_horizontal_ranges(mask)
        

        # image_name = mask_file.replace(".png", ".jpg")
        image_path = os.path.join(input_images, mask_file)  # 假设图像文件在input_images文件夹下

        annotation = ET.Element("annotation")
        filename_elem = ET.SubElement(annotation, "filename")
        filename_elem.text = mask_file

        size_elem = ET.SubElement(annotation, "size")
        width_elem = ET.SubElement(size_elem, "width")
        height_elem = ET.SubElement(size_elem, "height")
        depth_elem = ET.SubElement(size_elem, "depth")
        
        image = Image.open(image_path)
        width, height = image.size
        width_elem.text = str(width)
        height_elem.text = str(height)
        depth_elem.text = "3"  # 假设图像是彩色图像
        
        for i in range(0,len(ranges)-1):
            if ds[i] >50:
                ds[i] = 10
            
            # xy.append(range_list)
            # if range_list[i] - range_list[i] >20:

            
            object_elem = ET.SubElement(annotation, "object")
            name_elem = ET.SubElement(object_elem, "name")
            name_elem.text = "draw"  # 假设目标名称为 "object"

            bndbox_elem = ET.SubElement(object_elem, "bndbox")

            if ranges[i][0]>=ranges[i+1][0]:
                xmin = ranges[i+1][0]-1
                ymin = ranges[i][1]-1
                xmax = xmin+ds[i]
                ymax = ymin+ds[i]
            else:
                xmin = ranges[i][0]-2
                ymin = ranges[i][1]-2
                xmax = xmin+ds[i]
                ymax = ymin+ds[i]


            # xmin = min(ranges[i][0], ranges[i-1][0])
            # ymin = min(ranges[i][1], ranges[i-1][1])
            # xmax = max(ranges[i][0], ranges[i-1][0])
            # ymax = max(ranges[i][1], ranges[i-1][1])

            xmin_elem = ET.SubElement(bndbox_elem, "xmin")
            ymin_elem = ET.SubElement(bndbox_elem, "ymin")
            xmax_elem = ET.SubElement(bndbox_elem, "xmax")
            ymax_elem = ET.SubElement(bndbox_elem, "ymax")

            ymin_elem.text = str(ymin)
            ymax_elem.text = str(ymax)
            xmin_elem.text = str(xmin)
            xmax_elem.text = str(xmax)

        xml_file_name = mask_file.replace(".png", ".xml")
        print(xml_file_name)
        xml_file_path = os.path.join(output_xml_folder, xml_file_name)
        
        tree = ET.ElementTree(annotation)
        tree.write(xml_file_path)

print("XML annotation files generated.")



# def find_horizontal_ranges(mask):
#     ranges = []
#     row = []
#     width, height = mask.size
    
#     for y in range(height):
#         in_range = False
#         for x in range(width):
#             pixel_value = mask.getpixel((x, y))
#             if pixel_value == 255:
#                 if y%50 ==0 and y not in row:
#                     ranges.append([x, y])
#                     row.append(y)

#     return ranges