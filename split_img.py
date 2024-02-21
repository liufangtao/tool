import os
import codecs
import numpy as np
import math
#from dota_utils import GetFileFromThisRootDir
import cv2
#import shapely.geometry as shgeo
#import dota_utils as util
import copy
class splitimg():
    def __init__(self,
                 basepath,
                 outpath,
                 code = 'utf-8',
                 gap=256,
                 subsize=512,
                 thresh=0.1,
                 ext = '.jpg'
                 ):
        """
        :param basepath: base path for glass data
        :param outpath: output base path for glass data,
        the basepath and outputpath have the similar subdirectory, 'img' and 'label'
        :param code: encodeing format of txt file
        :param gap: overlap between two patches
        :param subsize: subsize of patch
        :param thresh: the thresh determine whether to keep the instance if the instance is cut down in the process of split
        :param ext: ext for the image format
        """
        self.basepath = basepath
        self.outpath = outpath
        self.code = code
        self.gap = gap
        self.subsize = subsize
        self.slide = self.subsize - self.gap
        self.thresh = thresh
        self.imagepath = self.basepath
        self.labelpath = self.basepath
        self.outimagepath = os.path.join(self.outpath, 'img')
        self.outlabelpath = os.path.join(self.outpath, 'label')
        self.ext = ext
        self.w=4096
        self.h=512
        self.thresh=0.7
        self.id='/1T/liufangtao/datas/galss_baoming/8-19/namet.txt'#id list without ext
        if not os.path.exists(self.outimagepath):
            os.makedirs(self.outimagepath)
        if not os.path.exists(self.outlabelpath):
            os.makedirs(self.outlabelpath)
    
    def cal_area(self,obj):
        w,h=[obj[2]-obj[0],obj[3]-obj[1]]
        return w*h
    def calchalf_iou(self, poly, img_poly):
        """
            It is not the iou on usual, the iou is the value of intersection over poly1
        """
        inter_poly = [max(poly[0],img_poly[0]),max(poly[1],img_poly[1]),min(poly[2],img_poly[2]),min(poly[3],img_poly[3])]
        
        inter_area = self.cal_area(inter_poly)
        poly_area = self.cal_area(poly)
        iou = inter_area / poly_area

        return inter_poly, iou

    def saveimagepatches(self, img, subimgname, left, up):
        subimg = copy.deepcopy(img[up: (up + self.subsize), left: (left + self.subsize)])
        outdir = os.path.join(self.outimagepath, subimgname + self.ext)
        cv2.imwrite(outdir, subimg)
    
    def xywhtoxyxy(self,obj):
        x,w=np.dot([obj[0],obj[2]],self.w)
        y,h=np.dot([obj[1],obj[3]],self.h)
        x1,y1=[x-(w/2),y-(h/2)]
        x2,y2=[x+(w/2),y+(h/2)]
        out_=[x1,y1,x2,y2]
        #x1,y1=[w+x,h+y]
        #out_=[x,y,x1,y1]
        return out_
    def xyxytoxywh(self,obj,left,up):
        x1,y1=[obj[0]-left,obj[1]-up]
        x2,y2=[obj[2]-left,obj[3]-up]
        w,h=[(x2-x1),(y2-y1)]
        x,y=[(x2+x1)/2,(y2+y1)/2]
        out_gt=np.dot([x,y,w,h],1/512)
        return out_gt
    def savepatches(self, resizeimg, subimgname, left, up, right, down):
        self.saveimagepatches(resizeimg, subimgname, left, up)

    def SplitSingle(self, name, rate, extent):
        """
            split a single image and ground truth
        :param name: image name
        :param rate: the resize scale for the image
        :param extent: the image format
        :return:
        """
        print(extent)
        name=name.replace("\n","")
        img = cv2.imread(os.path.join(self.imagepath, name + extent))
        if np.shape(img) == ():
            return
        #fullname = os.path.join(self.labelpath, name + '.txt')
        #objs=np.loadtxt(fullname).reshape(-1,5)  
        if (rate != 1):
            resizeimg = cv2.resize(img, None, fx=rate, fy=rate, interpolation = cv2.INTER_CUBIC)
        else:
            resizeimg = img
        outbasename = name + '__' + str(rate) + '__'
        weight = np.shape(resizeimg)[1]
        height = np.shape(resizeimg)[0]

        left, up = 0, 0
        while (left < weight):
            if (left + self.subsize >= weight):
                left = max(weight - self.subsize, 0)
            up = 0
            while (up < height):
                if (up + self.subsize >= height):
                    up = max(height - self.subsize, 0)
                right = min(left + self.subsize, weight - 1)
                down = min(up + self.subsize, height - 1)
                subimgname = outbasename + str(left) + '___' + str(up)
                self.savepatches(resizeimg, subimgname, left, up, right, down)
                if (up + self.subsize >= height):
                    break
                else:
                    up = up + self.slide
            if (left + self.subsize >= weight):
                break
            else:
                left = left + self.slide

    def splitdata(self, rate):
        """
        :param rate: resize rate before cut
        """
        dest_id=self.id 
        with open(dest_id) as f:
            image_ids=f.readlines()
        for image_id in image_ids:
            print(image_id,"is processing ")
            self.SplitSingle(image_id, rate, self.ext)

if __name__ == '__main__':
    split = splitimg(r'/1T/liufangtao/datas/galss_baoming/8-19/',
                       r'/1T/liufangtao/datas/galss_baoming/8-19out')
    split.splitdata(1)
