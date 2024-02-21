import os
import glob

seq_dir = os.path.expanduser('/1T/liufangtao/datas/phone_others/train/labels/')
files=glob.glob(seq_dir + '*.txt') 
for f, file in enumerate(files):
    readfile = open(file, 'r') #读取文件
    fline = readfile.readlines() #读取txt文件中每一行
    
    for j in fline:
        if j == '  ':
        # s ='1'+ j[1:]
            print(file)
            savetxt = open(file, 'w')
            savetxt.write('') #写入新的文件中
        


   


