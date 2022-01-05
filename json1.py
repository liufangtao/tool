import json
import os

path = 'E:\\s28_l'
dirs = os.listdir(path)

num_flag = 0
for file in dirs: # 循环读取路径下的文件并筛选输出
    if os.path.splitext(file)[1] == ".json": # 筛选csv文件
        num_flag = num_flag +1
        #print(os.path.join(path,file))

        with open(os.path.join(path,file),'r+') as load_f:

            load_dict = json.load(load_f)
            #print(load_dict)
            # n=len(load_dict['imagePath'])
            # print(n)
            print(load_dict['imagePath'])
            a=load_dict['imagePath'].replace("..\\s28_l\\","")
            print(a)
            load_dict['imagePath']=a
            print(load_dict['imagePath'])
            json.dump(load_dict, load_f, ensure_ascii=False, indent=4)
            print('修改完成')

# import os
# import json

# filelist_path = r"C:\Users\86186\Desktop\abc\\"

# for parent, dirnames, filenames in os.walk(filelist_path):
#     for filename in filenames:
#         if filename.endswith(".json"):
#             json_file_path = os.path.join(filelist_path, filename)
#             filename_qianzhui = filename.split(".")[0]
#             print(filename_qianzhui)
#             # exit()
#             # 修改 json文件 imagePath的value
#             with open(json_file_path, 'r+') as f_rw:
#                 json_all = json.load(f_rw)
#                 json_all['imagePath'] = filename_qianzhui+".jpg"
#                 json.dump(json_all, f_rw, ensure_ascii=False, indent=4)
            
#             f_rw.close()
            

