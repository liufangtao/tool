from PIL import Image
import os
import shutil
img_folder = "E:\\liufangtao\\hat\\hatnews\\train\\images"
newpath = "E:\\liufangtao\\hat\\hatnews\\train\\3"

 
imlist = os.listdir(img_folder)
imlist.sort()

if os.path.exists('test.txt'):
	os.remove('test.txt')

for imagename in imlist:
	imurl = os.path.join(img_folder,imagename)
	# print(imurl)
	im = Image.open(imurl)
	if im.size[0]>1920 or im.size[1]>1080:
		print(imagename)
		print(im.size[0],im.size[1])
		
		with open('test.txt','a+') as f:
			f.write(imagename + '\n')
		im.close()
		shutil.move(imurl, newpath+ '\\'+ imagename)


txtpath = 'E:\\liufangtao\\hat\\hatnews\\train\\labels'
with open("test.txt", "r") as f:
    datas = f.readlines()
    # print(data)
    for i in datas:
    	data = i.replace('\n','').split('.')[0]
    	print(data)
    	shutil.move(txtpath+'\\'+data+'.txt', newpath+ '\\'+data+'.txt')


