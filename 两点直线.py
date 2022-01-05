# 加载一张手写数字的灰度图片
# 从Paddle2.0内置数据集中加载手写数字数据集，本文第3章会进一步说明
import matplotlib.pyplot as plt
import pylab
import numpy as np

from paddle.vision.datasets import MNIST
# 选择测试集
mnist = MNIST(mode='test')
# 遍历手写数字的测试集
for i in range(len(mnist)):
    # 取出第一张图片
    if i == 0:
        sample = mnist[i]
        # 打印第一张图片的形状和标签
        print(sample[0].size, sample[1])
plt.imshow(mnist[0][0])
pylab.show()
print('手写数字是：', mnist[0][1])
a = np.array(mnist[0][0])
# print(a)
np.savetxt('001.txt', a, fmt="%3d", delimiter=" ")

