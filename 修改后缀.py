import os
 
files = os.listdir("/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/MatrixVision/烟火/fire_and_smoke/JPEGImages")#列出当前目录下所有的文件
for filename in files:
     portion = os.path.splitext(filename)#分离文件名字和后缀
     # print(portion)
     if portion[1] ==".png":
          print(portion)
          newname = portion[0]+".jpg"#要改的新后缀
          os.chdir("/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/MatrixVision/烟火/fire_and_smoke/JPEGImages")#切换文件路径,如无路径则要新建或者路径同上,做好备份
          os.rename(filename,newname)
 
     
     


         
         