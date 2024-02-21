import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from skimage import io, color

# 读取图片
image = io.imread('/1T/liufangtao/datas/galss_quanmian/test/0913/out2/origin-cam2-20230912141125136586_2_30.jpg')

# 将彩色图片转换为灰度图
gray_image = color.rgb2gray(image)

# 将二维图像矩阵转换为一维向量
data = gray_image.flatten()

# 初始化PCA模型，选择降维后的维度（这里选择2维）
pca = PCA(n_components=2)

# 拟合PCA模型并进行降维
reduced_data = pca.fit_transform(data.reshape(-1, 1))

# 获取主成分和解释方差比例
components = pca.components_
explained_variance_ratio = pca.explained_variance_ratio_

# 输出解释方差比例
print("解释方差比例:", explained_variance_ratio)

# 绘制主成分
plt.figure(figsize=(8, 6))
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], cmap='viridis', s=5)
plt.xlabel("主成分1")
plt.ylabel("主成分2")
plt.title("PCA分析结果")
plt.show()