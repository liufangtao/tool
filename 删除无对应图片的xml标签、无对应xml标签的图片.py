'''windows上执行'''
'''
import os
import os.path
import shutil

h = 0
a = ''
b = ''
dele = []
pathh = r"E:\liufangtao\image\jyz_ps\\"#xml和jpg在同一文件夹
movepath = r"E:\liufangtao\image/"
#dele.remove(1)
for filenames in os.walk(pathh):#for dirpath,dirnames,filenames in os.walk(path)三元组，dirpath为搜索目录，dirnames（list）,为搜索目录下所有文件夹，filenames(list)为搜索目录下所有文件，这里用法其实很不好，filenames其实就是这个三元组，然后再将第三个提取出来，代码可读性太差了。
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:
        # print(filename)
        if h==0:#如果第一次检索到这个名字则放到a里面
            a = filename
            h = 1
        elif h==1:#这是第二次检索了，h=1说明已经存储了一个文件名在a中，然后读取了下一个文件名，然后判断是否一样。这个程序的Bug就是pic和label must put together.而且要贴在一起。
            # print(filename)
            b = filename
            if a[0:a.rfind('.', 1)]==b[0:b.rfind('.', 1)]:#这里用了rfind来给出名字，然后比较，rfind找出字符最后一次出现的位置。这里.前面就是文字，而切片【a:b】不计b。
                h = 0
                # print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print(dele)
print(len(dele))
for file in dele:
    shutil.move(pathh+file, movepath)
    # os.remove(pathh+file)
    print("remove"+file+" is OK!")
    
#再循环一次看看有没有遗漏的单身文件
for filenames in os.walk(pathh):
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:
        # print(filename)
        if h==0:
            a = filename
            h = 1
        elif h==1:
            # print(filename)
            b = filename
            if a[0:a.rfind('.', 1)]==b[0:b.rfind('.', 1)]:
                h = 0
                # print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print (dele)
# 清除单身的xml或者jpg 在Windows运行
'''
import os
import glob

# 获取所有的txt文件
txt_files = glob.glob('/1T/liufangtao/datas/glass_changxin/11monthdatas/1206/1701843253378T侧/1702884323998_长信20231215/*.jpg')

for txt_file in txt_files:
    # 获取对应的图片文件名
    img_file = os.path.splitext(txt_file)[0] + '.xml'
    
    # 检查图片文件是否存在
    if not os.path.exists(img_file):
        # 如果不存在，删除txt文件
        os.remove(txt_file)
        print(f'Deleted {txt_file} because {img_file} does not exist.')
# import os
# import shutil

# def remove_unmatched_files(img_folder, txt_folder):
#     # 获取两个文件夹中的文件列表
#     img_files = set(os.listdir(img_folder))
#     txt_files = set(os.listdir(txt_folder))

#     # 找到没有对应图片的txt文件
#     unmatched_txt_files = txt_files - img_files

#     # 删除没有对应图片的txt文件
#     for file in unmatched_txt_files:
#         os.remove(os.path.join(txt_folder, file))

#     # 找到没有对应txt文件的图片
#     unmatched_img_files = img_files - txt_files

#     # 删除没有对应txt文件的图片
#     for file in unmatched_img_files:
#         os.remove(os.path.join(img_folder, file))

# # 调用函数，传入图片和文本文件夹的路径
# remove_unmatched_files('/1T/liufangtao/ultralytics/runs/detect/M10_glass0.3_result/images', '/1T/liufangtao/ultralytics/runs/detect/M10_glass0.3_result/labels')
