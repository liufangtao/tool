from skimage import data_dir,io,transform,color

import numpy as np

def convert_gray(f,**args):

     rgb=io.imread(f)   

     gray=color.rgb2gray(rgb)     

     dst=transform.resize(gray,(416,416))       

     return dst
str='F:\\Documents\\Desktop\\hat\\'+'/*.jpg'

coll = io.ImageCollection(str,load_func=convert_gray)
for i in range(len(coll)):

    io.imsave('F:\\Documents\\Desktop\\hat\\1\\'+'h'+np.str(i)+'.jpg',coll[i]) 
