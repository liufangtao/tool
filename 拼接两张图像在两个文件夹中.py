import cv2
import numpy as np
import pandas as pd
import os,hashlib,shutil

def images_concat(left_img_path, right_img_path, concat_image_path, text=None):
    '''
    :param left_img_path: 左侧图片本地路径
    :param right_img_path: 右侧图片本地路径
    :param concat_image_path: 拼接结果保存路径
    :param text: 批注文字
    :return: None
    '''
    if not left_img_path and not right_img_path:
        return
    w_final = h_final = h_left = w_left = h_right = w_right = 0
    if left_img_path:
        left_img = cv2.imread(left_img_path)
        h_left, w_left = left_img.shape[:2]
        w_final += w_left
    if right_img_path:
        right_img = cv2.imread(right_img_path)
        h_right, w_right = right_img.shape[:2]
        w_final += w_right
    h_final = max(h_left, h_right) # 以较大的图的高度为准
    if text: h_final += 20 # 为批注文字预留位置

    canvas = np.zeros([h_final, w_final, 3], np.uint8)
    # 填入像素，兼容图片为空的情况
    if left_img_path and right_img_path:
        canvas[0:h_left, 0:w_left] = left_img
        canvas[0:h_right, w_left-1:-1] = right_img
    elif left_img_path:
        canvas[0:h_left, 0:w_left] = left_img
    elif right_img_path:
        canvas[0:h_right, 0:w_right] = right_img

    if text: # 写入文字
        cv2.putText(canvas, text, (5, h_final-5), cv2.FONT_HERSHEY_PLAIN, 15, (0, 0, 255), 25)
    cv2.imwrite(concat_image_path, canvas)


img_a = r'/1T/liufangtao/datas/glass_changxin/10monthdatas/负样本/out0/images'#左图地址
img_b = r'/1T/liufangtao/datas/glass_changxin/10monthdatas/负样本/out0/mask3-7-25'#右图地址
img_c = r'/1T/liufangtao/datas/glass_changxin/10monthdatas/负样本/out0/out'#保存地址

a_name = os.listdir(img_a)
# print(a_name)
b_name = os.listdir(img_b)

for a in a_name:
	print(a)
	for b in b_name:
		if a[:-4] == b[:-4]:
			images_concat(img_a+'/'+a, img_b+'/'+b, img_c+'/'+a) #, text='true'+' '*42+'predicted'
print(len(a_name))
print('success')

			

	


# img1 = cv2.imread('E:\\tmp\\xray\\1.png')
# img2 = cv2.imread('E:\\tmp\\xray\\1_out.png')

# # img1 = cv2.resize(img1, (640, 480))
# # img2 = cv2.resize(img2, (640, 480))
 
# # 核心代码
# image = np.concatenate([img1, img2], axis=1)
 
# cv2.imshow("test", image)
# cv2.waitKey(0)