import os
import shutil

read_path = r'/1T/liufangtao/datas/glass/test/1208/12线236G0VE000缺陷数据1210/1210/out1_512'#原图
save_path = r'/1T/liufangtao/datas/glass/test/1208/12线236G0VE000缺陷数据1210/1210/images_512' #保存图片地址
fileType = '.jpg'
class ReadImageName():
    def __init__(self):
        self.path = r'/1T/liufangtao/ultralytics/runs/predict/exp/visuals' #xml地址
    def readname(self):
        flielist = []
        flieimg = []
        for root, dirs, files in os.walk(self.path, topdown=False):
            for item in files:
                if item.endswith('.jpg'):
                    itemname = item[:-4]
                    flielist.append(itemname)
        for root, dirs, files in os.walk(read_path, topdown=False):
            print(root)
            for it in files:
                ite = it[:-4]
                # print(ite)
                if ite in flielist:
                    # print(ite)
                    for root, dirs, files in os.walk(read_path, topdown=False):

                        # for name in dirs:
                        # if not os.path.exists(os.path.join(save_path,name)):
                        #         os.makedirs(os.path.join(save_path,name))
                        try:
                            imagesb = os.path.join(root,ite+fileType)
                            print(imagesb)
                            imagesc = os.path.join(save_path,ite+fileType)
                            shutil.move(imagesb,imagesc)#注意修改shutil.copy是复制功能;shutil.move移动
                        except FileNotFoundError:
                            continue
                            # for root1, dirs1, files1 in os.walk(self.path, topdown=False):
                            #     for name1 in dirs1:
                            #         try:
                            #             imagesd = os.path.join(os.path.join(root1,name1),ite+'.xml')
                            #             imagese = os.path.join(os.path.join(save_path,name),ite+'.xml')
                            #             shutil.copy(imagesd,imagese) #注意修改shutil.copy是复制功能;shutil.move移动               
                            #         except FileNotFoundError:
                            #             continue   
                    # print("%s Copy successfully"%(item+fileType))
if __name__ == '__main__':
    log = ReadImageName()
    log.readname()




