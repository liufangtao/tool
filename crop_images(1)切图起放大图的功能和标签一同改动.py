# -*- coding: utf-8 -*-
import os
import shutil
import numpy as np
import cv2
import math
import random
from tqdm import tqdm


def create_local_dirs(path):
    if not os.path.isdir(path):
        print(f'Creating path: {path}')
        os.makedirs(path, exist_ok=True)
    else:
        print(f'Path already exist: {path}')
    return True


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def get_label_list(data_path):
    label_files_list = []
    for file in os.listdir(data_path):
        tmp_file_path = os.path.join(data_path, file)
        if os.path.isfile(tmp_file_path) and file.endswith('.txt'):
            label_files_list.append(tmp_file_path)
    return label_files_list


def read_text_file(fpath):
    f1 = open(os.path.join(fpath), "r")
    lines = f1.readlines()
    f1.close()
    annos = []
    for line in lines:
        anno_sec = str(line).split(' ')
        label_index = int(anno_sec[0])
        cx, cy = float(anno_sec[1]), float(anno_sec[2])
        w, h = float(anno_sec[3]), float(anno_sec[4])
        annos.append([label_index, cx, cy, w, h])
    return annos


"""
update variables here
"""

# dxdg
# class_name = 'dxdg'
class_dict = {
    'aodian': 0,
    'diaomo': 1,
    'huashang': 2,
    'zangwu':3
}

flag_draw_bbox = True # True, False
tile_h, tile_w = 512, 512    #想corp的大小像素
tile_min_h, tile_min_w = 10, 10
tile_overlapping = 10  #重叠像素
tile_max_aspect_ratio = 1/10.0  #坐标转换随机加偏差，new_h/new_w不要超过1/6

data_root = r'/1T/liufangtao/datas/glass_changxin'
new_suffix = '_tile_512bat'

dataset_names = ['1008']
# dataset_names = ['val', 'test']
# dataset_names = ['train', 'val', 'test']





for d_name in dataset_names:
    yolo_data_root = os.path.join(data_root, d_name)
    output_data_root = os.path.join(data_root, d_name , new_suffix)

    # init path
    labels_path = os.path.join(yolo_data_root, "labels")
    images_path = os.path.join(yolo_data_root, "images")
    output_labels_path = os.path.join(output_data_root, "labels")
    output_images_path = os.path.join(output_data_root, "images")
    create_local_dirs(output_labels_path)
    create_local_dirs(output_images_path)

    # get all label files
    label_files_list = get_label_list(labels_path)

    for label_fpath in tqdm(label_files_list, desc="crop images..."):

        # label_fpath = label_files_list[0]
        label_fname = os.path.basename(label_fpath)
        print(label_fname)
        image_fname = label_fname.replace('.txt', '.jpg')
        image_fpath = os.path.join(images_path, image_fname)

        # read image
        img = cv2.imread(image_fpath)
        img_h, img_w, c = img.shape
        # print('-'*33)
        # print(image_fpath)
        # print(img.shape)

        # load labels
        annos = read_text_file(label_fpath)
        print(f'number of labels: {len(annos)}')

        print('-'*33)
        if img_h < tile_h or img_w < tile_w:
            new_label_fpath = os.path.join(output_labels_path, label_fname)
            new_image_fpath = os.path.join(output_images_path, image_fname)
            shutil.copy(label_fpath, new_label_fpath)
            shutil.copy(image_fpath, new_image_fpath)
        else:
            for y in range(0, img_h, tile_h-tile_overlapping):
                for x in range(0, img_w, tile_w):   #-tile_overlapping
                    # if image is smaller than tile size, copy image over
                    if (img_h - y) < tile_h or (img_w - x) < tile_w:
                        break

                    x0, y0 = x, y # starts
                    x1 = x + tile_w
                    y1 = y + tile_h
                    print('-'*33)
                    print(x0, x1, y0, y1)

                    # check whether the patch width or height exceeds the image width or height
                    if x1 > img_w:
                        x0 = img_w - tile_w
                        x1 = img_w - 1
                    if y1 > img_h:
                        y0 = img_h - tile_h
                        y1 = img_h -1
                    tile_img = img[y0:y1, x0:x1].copy()

                    # workout intersected anno location
                    tile_annos = []
                    for anno in annos:
                        label_index = anno[0]
                        cx, cy = float(anno[1]) * img_w, float(anno[2]) * img_h
                        w, h = float(anno[3]) * img_w, float(anno[4]) * img_h
                        anno_x0, anno_x1 = int(cx - w/2.0), int(cx + w/2.0)
                        anno_y0, anno_y1 = int(cy - h/2.0), int(cy + h/2.0)

                        # add randomness to the bounding box +-10
                        anno_x0 = anno_x0 + np.random.randint(20) - 10
                        anno_x1 = anno_x1 + np.random.randint(20) - 10
                        anno_y0 = anno_y0 + np.random.randint(20) - 10
                        anno_y1 = anno_y1 + np.random.randint(20) - 10

                        # check intersect
                        minx, miny = max(x0, anno_x0), max(y0, anno_y0)
                        # if h > 2* tile_h:


                        maxx, maxy = min(x1, anno_x1), min(y1, anno_y1)
                        if minx > maxx or miny > maxy:
                            continue

                        # new anno pos in tile
                        new_x0, new_x1 = minx - x0, maxx - x0
                        new_y0, new_y1 = miny - y0, maxy - y0
                        new_w, new_h = new_x1-new_x0, new_y1-new_y0
                        print(f'Found intersected bounding box: {new_x0, new_x1, new_y0, new_y1} - {new_w, new_h}')
                        if new_w < tile_min_w or new_h < tile_min_h:
                            print('tile too small..')
                            continue
                        # if new_w/new_h > 1.0/tile_max_aspect_ratio or new_w/new_h < tile_max_aspect_ratio:
                        #     continue

                        new_cx, new_cy = (new_x1+new_x0)*0.5/tile_w, (new_y1+new_y0)*0.5/tile_h
                        new_wr, new_hr = new_w/tile_w, new_h/tile_h
                        tile_annos.append("%s %.6f %.6f %.6f %.6f\n" % (label_index, new_cx, new_cy, new_wr, new_hr))

                        # draw bounding box
                        # if flag_draw_bbox:
                        #     classes_colors = {class_dict[j]: hsv2rgb(i/len(class_dict)*360, 1.0, 1.0) for i, j in enumerate(class_dict.keys())}
                        #     tile_img = cv2.rectangle(tile_img, (new_x0, new_y0), (new_x1, new_y1), classes_colors[label_index], 3)
                    
                    # save image and label
                    new_image_fname = image_fname.replace('.jpg', '_y' + str(y0) + '_x' + str(x0) + '.jpg')
                    cv2.imwrite(os.path.join(output_images_path, new_image_fname), tile_img)
                    new_label_fname = image_fname.replace('.jpg', '_y' + str(y0) + '_x' + str(x0) + '.txt')
                    with open(os.path.join(output_labels_path, new_label_fname), "w") as f:
                        f.writelines(tile_annos)


