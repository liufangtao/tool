import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw

def xml_to_mask(xml_path, image_size):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    image_name = root.find("filename").text

    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)
    Object = root.findall("object")
    for obj in root.findall("object"):
        label = obj.find("name").text
       
        points = obj.findall("polygon/point")
        polygon = []
        for point in points:
            x = float(point.find("x").text)
            y = float(point.find("y").text)
            polygon.append((x, y))

        draw.polygon(polygon, fill=255)

    return mask

# 输入和输出文件夹路径
input_xml_folder = "/1T/liufangtao/datas/glass/images_draw"
output_mask_folder = "/1T/liufangtao/datas/glass/images_draw_out"
os.makedirs(output_mask_folder, exist_ok=True)

xml_files = os.listdir(input_xml_folder)
for xml_file in xml_files:
    if xml_file.endswith(".xml"):
        xml_path = os.path.join(input_xml_folder, xml_file)
        image_name = xml_file.replace(".xml", ".png")  #
        image_path = os.path.join(input_xml_folder, image_name)  # 假设图像文件在input_images文件夹下

        image = Image.open(image_path)
        image_size = image.size

        mask = xml_to_mask(xml_path, image_size)
        
        mask_name = xml_file.replace(".xml", ".png")
        mask_path = os.path.join(output_mask_folder, mask_name)

        mask.save(mask_path)

print("Conversion completed.")
