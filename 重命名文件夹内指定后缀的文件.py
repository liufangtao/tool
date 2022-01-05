#coding:utf8
# import os;
 
# your_need_process_type=["label"]
# def rename():
#         i=0
#         path="E:\\liufangtao\\DJI_20210320162110_0002_Z\\";
#         filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
#         for files in filelist:#遍历所有文件
#             print(files)
#             i=i+1
#             Olddir=os.path.join(path,files);#原来的文件路径
#             print(Olddir)
                
#          #    # if os.path.isdir(Olddir):#如果是文件夹则跳过
#          #    #         continue;
#          #    filename=os.path.splitext(files)[0];#文件名
#          #    filetype=os.path.splitext(files)[1];#文件扩展名
# 	        # if filename in your_need_process_type:
#          #        Newdir=os.path.join(path,"BusinessHall_"+str(i)+filetype);#新的文件路径
#          #    	os.rename(Olddir,Newdir)#重命名
# rename()
import os
from shutil import copy
 #path为批量文件的文件夹的路径
path = 'E:\\windows_v1.8.0\\lg\\9'
to_path= "E:\\windows_v1.8.0\\lg"
 #文件夹中所有文件的文件名
file_names = os.listdir(path)
print(file_names)
 #外循环遍历所有文件名，内循环遍历每个文件名的每个字符
for name in file_names:
    print(name)
    for s in name:
        print(s)
        if s == 'g':
            index_num=name.index(s)  #index_num为要删除的位置索引
            print(index_num)
   #采用字符串的切片方式删除编号
            # os.renames(os.path.join(path,name),os.path.join(path,name[:index_num-3]+'.jpg')) 
            os.renames(os.path.join(path,name),os.path.join(path,name[:index_num-4])) 
            break  #重命名成功，跳出内循环


files = os.listdir(path)
for i in files:       
    print (i)
    os.rename(os.path.join(path+'\\' + i,"label.png"),os.path.join(path+'\\'+i,i+".png"))
    copy(os.path.join(path+'\\'+i,i+".png"), to_path)
