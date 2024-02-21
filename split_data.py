import os
import random

train_percent = 0.85
trainval_percent = 0.0
test_percent = 0.0
val_percent = 0.15
xmlfilepath = '/1T/liufangtao/datas/glass_quanmian/20140116/train_val/labels'
txtsavepath = '/1T/liufangtao/datas/glass_quanmian/20140116/train_val'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(num * train_percent)
tx = int(num * test_percent)
tl = int(num * val_percent)
trainval = random.sample(list, tv)
train = random.sample(list, tr)
test = random.sample(list, tx)
val =random.sample(list, tl)

# ftrainval = open(txtsavepath+'/trainval.txt', 'w')#test and val data ids
# ftest = open(txtsavepath+'/test.txt', 'w')
ftrain = open(txtsavepath+'/train.txt', 'w')# train data ids
fval = open(txtsavepath+'/val.txt', 'w')

for i in list:
    name = os.path.join(txtsavepath,'images', total_xml[i][:-4] +'.jpg'+'\n')
    name_txt = os.path.join(txtsavepath,'labels', total_xml[i][:-4] +'.txt')
   
    if i in train or os.path.getsize(name_txt) == 0:
        ftrain.write(name)
    # if i in trainval:
    #     ftrainval.write(name)
    #     if i in train:
    #         ftest.write(name)
    #     else:
    #         fval.write(name)
    else:
        fval.write(name)

# ftrainval.close()
ftrain.close()
fval.close()
# ftest.close()