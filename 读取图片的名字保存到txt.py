import os
 
 
class ReadImageName():
    def __init__(self):
        self.path = r'/1T/liufangtao/datas/galss_baoming/8-19'
 
    def readname(self):
        filenames = os.listdir(self.path)
        flielist = []
 
        for item in filenames:
            if item.endswith('.jpg'):
                # itemname = os.path.join(self.path, item)
                itemname = item[:-4]
                flielist.append(itemname)
 
        fo = open(r"/1T/liufangtao/datas/galss_baoming/8-19/namet.txt", "w")
        for item in flielist:
            fo.write(str(item) + "\n")
 
 
if __name__ == '__main__':
    log = ReadImageName()
    log.readname()