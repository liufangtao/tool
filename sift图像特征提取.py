import cv2
import numpy as np 

original_image = '/1T/liufangtao/datas/glass/0802/out0/all/_tile_650bat/kong/cam-XD-DOWN-2023073110064274421_1_y1280_x0.png'
target_image = '/1T/liufangtao/datas/glass/0802/out0/all/_tile_650bat/images/cam-XD-DOWN-2023073110064274421_6_y1920_x0.png'
# 读取原始图像和目标图像
original_image = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
target_image = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)

# 创建SIFT、KAZE对象
# sift = cv2.xfeatures2d.SIFT_create()
kaze = cv2.KAZE_create()

# 在原始图像和目标图像上计算SIFT关键点和描述符
# keypoints_original, descriptors_original = sift.detectAndCompute(original_image, None)
# keypoints_target, descriptors_target = sift.detectAndCompute(target_image, None)

keypoints_original, descriptors_original = kaze.detectAndCompute(original_image, None)
keypoints_target, descriptors_target = kaze.detectAndCompute(target_image, None)

# 使用FLANN匹配器进行特征匹配
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # 控制匹配器的搜索次数

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors_original, descriptors_target, k=2)

# 根据Lowe's比率测试保留好的匹配
good_matches = []
for m, n in matches:  # m,n 的数量不同，会是
    if m.distance < 0.95 * n.distance: #97,190
        good_matches.append(m)

# 如果匹配点足够多，认为图像中存在缺陷
if len(good_matches) > 50:
    print("图像中无缺陷")
else:
    print("图像中存在缺陷")

# 绘制匹配的关键点
result_image = cv2.drawMatches(original_image, keypoints_original, target_image, keypoints_target, good_matches, None)

# 显示结果图像
cv2.imshow('Result Image', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
