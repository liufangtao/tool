import os
import shutil


cl = 2  #类别

dir1 = r'/1T/liufangtao/datas/glass_changxin/train_val'

img_dir1 = os.path.join(dir1,'images')
txt_dir1 = os.path.join(dir1,'labels')
txt_list = os.listdir(txt_dir1)
last_name = os.path.basename(dir1)
img_save = os.path.join(dir1,last_name,str(cl),'images')
txt_save = os.path.join(dir1,last_name,str(cl),'labels')
os.makedirs(img_save , exist_ok=True)
os.makedirs(txt_save , exist_ok=True)
count = []

for name in txt_list:
    
    if os.path.splitext(name)[1] == ".txt":
        img_file_path = os.path.join(img_dir1, os.path.splitext(name)[0]) + '.jpg'
        xml_file_path = os.path.join(txt_dir1, os.path.splitext(name)[0]) + '.txt'
        print(name)

        with open(txt_dir1 + "/" + name, 'r', encoding='utf-8') as f1:
            lines1 = f1.readlines()
            for line1 in lines1:
                line1 = [float(x) for x in line1.split()]
                try:
                    if int(line1[0]) in [cl]:
                        shutil.move(img_file_path, img_save)
                        shutil.move(xml_file_path, txt_save)
                        
                    # if line1[0] in ['1']:
                    #     shutil.move(img_file_path, bjyzpssave)
                    #     shutil.move(xml_file_path, bjyzpssave)
                    # if line1[0] in ['2']:
                    #     shutil.move(img_file_path, cjyzpssave)
                    #     shutil.move(xml_file_path, cjyzpssave)
                except FileNotFoundError:
                    continue
                except shutil.Error:
                    continue
                except PermissionError:
                    continue
                    
                    


