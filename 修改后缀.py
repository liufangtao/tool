import os
 
files = os.listdir("E:\\liufangtao\\smokeimage\\森林烟火")#列出当前目录下所有的文件
for filename in files:
     portion = os.path.splitext(filename)#分离文件名字和后缀
     print(portion)
     if portion[1] ==".png":
     	newname = portion[0]+".jpg"#要改的新后缀
     	os.chdir("E:\\liufangtao\\smokeimage\\森林烟火")#切换文件路径,如无路径则要新建或者路径同上,做好备份
     	os.rename(filename,newname)
 
     
     


         
         