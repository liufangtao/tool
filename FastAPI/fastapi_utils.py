#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作者: liufangtao
创建时间: 2024-04-30
最后修改时间: 2024-05-14
脚本功能说明:
     
    
"""
from PIL import Image
import cv2


def crop_image(image_array, boxes):
    cropped_images = []
    for i, box in enumerate(boxes):
        x, y, w, h = box
        # 计算扩大1.5倍后的宽度和高度
        new_w = w * 1.5
        new_h = h * 1.5
        # 确定正方形的边长
        square_size = max(new_w, new_h)
        # 计算正方形区域的左上角坐标
        x1 = x - ((square_size - new_w) // 2 +new_w // 2 )
        y1 = y - ((square_size - new_h)// 2 + new_h // 2)
        # 计算正方形区域的右下角坐标
        x2 = x + ((square_size - new_w) // 2 +new_w // 2 )
        y2 = y + ((square_size - new_h) // 2 + new_h // 2)
        # 确保裁剪区域在图片范围内
        x1 = int(max(x1, 0))
        y1 = int(max(y1, 0))
        x2 = int(min(x2, image_array.shape[1]))
        y2 = int(min(y2, image_array.shape[0]))
        # 裁剪图片
        cropped = image_array[y1:y2, x1:x2]
        # 保存裁剪后的图片
        save_path = f"{i}.jpg"
        cv2.imwrite(save_path, cropped)
        cropped_images.append(cropped)
    return cropped_images



def cut_value_normal(val):
    val = max(val, 0.0)
    val = min(val, 1.0)
    return val*1.0


def expand_center_rect(center_x, center_y, rect_w, rect_h, expand_rate, height, width):

    bigger_side = max(rect_w*width, rect_h*height)

    rect_w = bigger_side/width*expand_rate
    rect_h = bigger_side/height*expand_rate

    xmin_f = min((center_x - rect_w/2),0)
    ymin_f = min((center_y - rect_h/2),0)
    xmax_f = max((center_x + rect_w/2),width)
    ymax_f = max((center_y + rect_h/2),height)


    
   

    # center_x = (xmax_f+xmin_f)/2
    # center_y = (ymax_f+ymin_f)/2

    # rect_w = xmax_f-xmin_f
    # rect_h = ymax_f-ymin_f

    return int(xmin_f),int(ymin_f),int(xmax_f),int(ymax_f)


def expand_mvboxes(image_array,boxes,rate):
    width = image_array.shape[1]
    height = image_array.shape[0]
    cropped_images = []
    # boxes=[boxes]
    print(boxes)
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = expand_center_rect(
            box[i][0], box[i][1], box[i][2], box[i][3], rate, height, width)
        # print(x1, y1, x2, y2)

        cropped = image_array[y1:y2, x1:x2]
        save_path = f"{i}.jpg"
        cv2.imwrite(save_path, cropped)
        cropped_images.append(cropped)
    return boxes