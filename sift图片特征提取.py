# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("/1T/liufangtao/datas/glass/0802/out0/all/corp/Crack/cam-XD-DOWN-2023073110064274421_17_259.jpg")
img1 = img.copy()
img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create(nfeatures=10)

kp = sift.detect(gray,None)
des = sift.compute(gray,kp)# 计算所有特征点的特征值
feature_value = des[1]  # 拿到所有特征点的特征值
# print(feature_value)

cv2.drawKeypoints(img1,kp,img)
cv2.drawKeypoints(img1,kp,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

plt.subplot(121), plt.imshow(img),
plt.title('Destination'), plt.axis('off')
plt.subplot(122), plt.imshow(img1),
plt.title('Destination'), plt.axis('off')
plt.show()

