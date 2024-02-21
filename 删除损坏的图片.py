# -*- coding:utf-8 -*-

import cv2
import imghdr
import os
#获取所要操作的文件夹(换成你的文件夹路径)
# filepath = r"U:\liu\jyzchage\绝缘子倾斜463"

path= r'/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/defect_image/2'
txt_path =r'/1T/liufangtao/datas/glass_changxin/1monthdatas/0103/2024-01-03/defect_image/2/'
for root, dirs, files in os.walk(path, topdown=False):
	for name in files:
		# print(os.path.join(root, name))
		filepath=os.path.join(root, name)
		#获取文件夹内的照片名列表
		# name_list = os.listdir(filepath)
		#创建删除记录文本文件
		fp=open(txt_path+"删除记录.txt","a+")
		#循环文件名列表
		# for name in name_list:
		#拼接照片的绝对路径
		delpath = filepath 
		
		#判断文件是否损坏
		if not imghdr.what(delpath) :
		#如果损坏，则进行删除
			print(delpath)
			os.remove(delpath)
			#然后把删除操作记录写入文本中（内存）
			fp.write(delpath +'\n')
			#最后进行刷新操作，把内存中的数据保存到文本文件中
			fp.flush()
		