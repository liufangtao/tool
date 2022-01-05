# -*- coding: utf-8 -*-   
import shutil 
import os  
  
def file_name(file_dir):
    path = []
    for root, dirs, files in os.walk(file_dir):
        # fileNames = []
        
    	# print(root) #当前目录路径  
    	# print(dirs) #当前路径下所有子目录  
        # print(files) #当前路径下所有非目录子文件
        # path.clear()
        for fname in files:
            # print(fname)
            if fname.split("_")[0] == 'DJI':
                # print(fname)
            # if os.path.splitext(fname)[1] == '.doc':
                path.append(str(root)+'\\'+str(fname))
                # print(path)
                # path.append(fname)
    return path

file_dir = 'V:\\share20211117\\data\\缺陷照片\\'
new_dir = 'V:\\share20211117\\data\\liu\\1\\'
path = file_name(file_dir)
num = len(path)
print(path, num) 
for i in path:
    print(i)
    j = i.split('\\')[-1]
    # print(j)
    new_file_path = os.path.join(new_dir, j)
    # print(new_file_path)
    shutil.copy(i , new_file_path)
print('-------------程序运行完成------------------')

