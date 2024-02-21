import os


path=r'/1T/liufangtao/datas/glass_changxin/10monthdatas/1019'     

#获取该目录下所有文件，存入列表中
fileList=os.listdir(path)

n=0
for i in fileList:
    
    #设置旧文件名（就是路径+文件名）
    oldname=path+ os.sep + fileList[n]   # os.sep添加系统分隔符
    #设置新文件名
    # newname=path + os.sep +'test3_1227_'+str(n).zfill(5)+'.jpg'
    newname=path + os.sep +'1019_'+i[:-4]+'_'+str(n).zfill(5)+'.jpg'
    os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
    print(oldname,'======>',newname)
    
    n+=1


