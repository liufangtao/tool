import os
import shutil

read_path = r'/1T/liufangtao/datas/glass_quanmian/test/20240205/out0'#原图
save_path = r'/1T/liufangtao/datas/glass_quanmian/test/20240205/images' #保存图片地址
fileType = '.jpg'
class ReadImageName():
    def __init__(self):
        self.path = r'/1T/liufangtao/ultralytics/runs/detect/M10_quanmianglass0.3_16result3' #xml地址
 
    def readname(self):
        filenames = os.listdir(self.path)
        flielist = [] 
        for item in filenames:
            if item.endswith('.jpg'):
                # itemname = os.path.join(self.path, item)
                itemname = item[:-4]
                flielist.append(itemname)
 
       
        for item in flielist:
            try:
                shutil.move(os.path.join(read_path,item+fileType),save_path)#注意修改shutil.copy是复制功能;shutil.movey移动
                    
                print("%s Copy successfully"%(item+fileType))
            except FileNotFoundError:
                continue
            except shutil.Error:
                continue
            except OSError:
                continue
 
 
if __name__ == '__main__':
    log = ReadImageName()
    log.readname()