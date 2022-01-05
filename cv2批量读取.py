
import cv2
import os

file_root = 'E:\\liufangtao\\home\\fwj_difficultims-2\\'#当前文件夹下的所有图片
file_list = os.listdir(file_root)
save_out = "E:\\liufangtao\\home\\fwj_difficultims-2yp\\"#保存图片的文件夹名称
for img_name in file_list:

    if img_name.endswith('.jpg'):

        img_path = file_root + img_name
        I = cv2.imread(img_path, -1)
            # image = sitk.ReadImage(".dcm")#读dcm
            # inputImg = np.squeeze(sitk.GetArrayFromImage(image))#读dcm
        # M, N = I.shape
        out_name = img_name.split('.')[0]
        save_path = save_out + out_name+'.jpg' 
        cv2.imwrite(save_path,I)
