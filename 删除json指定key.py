import json
import os

path = 'E:\\liufangtao\\home'
dirs = os.listdir(path)

num_flag = 0
for file in dirs: # 循环读取路径下的文件并筛选输出
    if os.path.splitext(file)[1] == ".json": # 筛选csv文件
        num_flag = num_flag +1

        
        # print(os.path.join(path,file))
        with open(os.path.join(path,file),'r') as load_f:

            load_dict = json.load(load_f)
            # print(load_dict)

        n=len(load_dict['shapes'])
        print(n)
        list= []
        for i in range (0,n):
            
            if load_dict['shapes'][i]['label'] == 'yp':
                # del load_dict['shapes'][i]
                # print("删除成功",file)
                
                n = len(load_dict['shapes'][i]['points'])
                list.append(n)       
            else:
                continue
           # if load_dict['shapes'][i]['label'] == 'interstice':
             #   load_dict['shapes'][i]['label'] = 'cleft'
            with open(os.path.join(path,file),'w') as dump_f:
                json.dump(load_dict, dump_f)
        print(min(list))

if(num_flag == 0):
    print('所选文件夹不存在json文件，请重新确认要选择的文件夹')
else:
    print('共{}个json文件'.format(num_flag))