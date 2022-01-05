import os,sys,glob,shutil,time,matplotlib,cv2,math,yaml,json
import numpy as np
from itertools import combinations
import copy
from skimage import morphology




def pnt2pntdist(pnt1, pnt2):
    """两点之间的距离，输入两点坐标，返回dst距离"""
    deltax = pnt1[0] - pnt2[0]
    deltay = pnt1[1] - pnt2[1]
    squrexy = deltax ** 2 + deltay ** 2
    dst = math.sqrt(squrexy)

    return dst


def get2vectangle(pnt0,pnt1,pnt2):
    """余弦定理算pnt0角度，输入3点坐标，返回角度"""
    vect1 = np.array(pnt1)-np.array(pnt0)
    vect2 = np.array(pnt2)-np.array(pnt0)

    vect1len = np.sqrt(np.sum(vect1*vect1))
    vect2len = np.sqrt(np.sum(vect2*vect2))
    cosval=vect1.dot(vect2) / (vect1len * vect2len)
    angle = np.arccos(cosval)* 360 / 2 / np.pi

    return angle



class LineOpt:
    def __init__(self, pnt1, pnt2):
        if isinstance(pnt1,tuple):
            pnt1=list(pnt1)
        if isinstance(pnt2,tuple):
            pnt2=list(pnt2)
        self.pnt1=pnt1
        self.pnt2=pnt2
        self._support_vector = np.array(pnt1)
        self._direction_vector =np.subtract(pnt2, pnt1)


    def equality(self):
        """方程式系数，返回3个系数"""
        x1, y1 = self.pnt1
        x2, y2 = self.pnt2
        A = y2 - y1
        B = -(x2 - x1)
        C = x2 * y1 - x1 * y2
        linecoef=(A,B,C)
        
        return linecoef


    def pnt2linedist(self, linecoef, pnt):
        """点到直线间的距离，输入系数和一个坐标点，返回距离"""
        A, B, C = linecoef
        x, y = pnt
        dist = math.fabs((A * x + B * y + C) / (math.sqrt(A ** 2 + B ** 2)))

        return dist
    

    def getxlenpnt(self,xlen):
        """x方向的向量长度"""
        directvect=self._direction_vector
        self.unitdirectvect = directvect / np.sqrt(directvect[0] ** 2 + directvect[1] ** 2)
        newpnt=self._support_vector+xlen*self.unitdirectvect
        newpnt=tuple(newpnt.astype(int))

        return newpnt


    def get_intersection_point(self, other):
        t = self._get_intersection_parameter(other)
        return None if t is None else self._get_point(t)


    def _get_point(self, parameter):
        return self._support_vector + parameter * self._direction_vector


    def _get_intersection_parameter(self, other):
        A = np.array([-self._direction_vector, other._direction_vector]).T
        if np.linalg.matrix_rank(A) < 2:
            return None
        b = np.subtract(self._support_vector, other._support_vector)
        x = np.linalg.solve(A, b)
        return x[0]#tuple(np.array(x[0]).astype(int))



    

   



class FJSegPostProc:
    def __init__(self):
        pass

    def morphopen(self, im, modesize=(5, 5)):
        """开运算"""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, modesize)
        im = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)

        return im


    def polygon2approxpolygon(self,polygon,epsilonratio=0.001):
        """绘制轮廓"""
        polygon = self.tovalidpolygon(polygon)
        epsilon = epsilonratio * cv2.arcLength(polygon, True)
        approxpolygon = cv2.approxPolyDP(polygon, epsilon, True)
        approxpolygon = np.squeeze(approxpolygon)

        return approxpolygon


    def polygon2convexhull(self,polygon):
        """绘制凸包轮廓"""
        convexhull=np.squeeze(cv2.convexHull(polygon))

        return convexhull


    def polygon2bndbox(self,polygon):
        """绘制外接矩形"""
        x, y, w, h = cv2.boundingRect(polygon)
        bndbox = [x, y, x + w, y + h]
        npbndbox = np.array(bndbox)
        maxval = np.max(npbndbox)
        bndbox = np.clip(npbndbox, 0, maxval).tolist()

        return bndbox


    def polygon2minrectinfo(self, polygon, borders):
        """计算矩形的四个点和中心点坐标"""
        #borders=[(low,up),(low,up)]
        rotrect = cv2.minAreaRect(polygon)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        rotbox=np.int0(cv2.boxPoints(rotrect))
        for i,(low,up) in enumerate(borders):
            np.clip(rotbox[:,i], low, up)
        boxlen1 = pnt2pntdist(rotbox[0], rotbox[1])
        boxlen2 = pnt2pntdist(rotbox[1], rotbox[2])
        if boxlen1 < boxlen2:
            rotbox = rotbox[[0, 3, 2, 1]]
        # if rect[1][0] > rect[1][1]:
        #     rotbox = rotbox[[0, 3, 2, 1]]

        cpnts = []
        # combs = list(zip((0, 2, 1, 3), (1, 3, 2, 0)))
        combs = list(zip((0, 1, 2, 3), (1, 2, 3, 0)))
        for (i, j) in combs:
            cpnt = (rotbox[i] + rotbox[j]) / 2
            cpnts.append(tuple(cpnt.astype(int)))

        newrotrect=[]
        for item in rotrect[:-1]:
            newrotrect.append(tuple(np.round(np.array(item)).astype(np.int32)))
        newrotrect.append(np.round(rotrect[-1],2))
        rotrect=tuple(newrotrect)

        rotbox = rotbox.tolist()
        minrectinfo = {'rotrect': rotrect, 'rotbox': rotbox, 'cpnts': cpnts}

        return minrectinfo


    def getobjregionskeletonxys(self,im,bwthresh=20,offset=(0,0)):
        imhwc=im.shape
        if len(imhwc)>2:
            im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(im, bwthresh, 1, cv2.THRESH_BINARY)#二值化函数
        skeleton = morphology.skeletonize(bw)#骨架提取函数
        yxs=np.where(skeleton)#满足条件返回x
        skeletonyxs=np.squeeze(np.dstack((yxs[0], yxs[1])))+np.array([offset[1],offset[0]])#删除一维条目
        skeletonxys=skeletonyxs[:,::-1]#列转置

        return skeletonxys


    def getskeletonfitline(self, skeletonxys):
        vx, vy, x0, y0 = cv2.fitLine(skeletonxys, cv2.DIST_L2, 0, 0.01, 0.01)#直线拟合

        return (vx[0], vy[0], x0[0], y0[0])


    def extendobjregioninfos(self,objregioninfos,borders,maskim,bwthresh=20):
        objregioninfos0 = copy.deepcopy(objregioninfos)
        for clsname in objregioninfos0.keys():
            for i, objregioninfo in enumerate(objregioninfos0[clsname]):
                minrectinfo = self.polygon2minrectinfo(objregioninfo['polygon'], borders)
                objregioninfos[clsname][i]['minrectinfo'] = minrectinfo

                x1,y1,x2,y2=objregioninfo['bndbox']
                regionmaskim=maskim[y1:y2+1,x1:x2+1,:]
                skeletonxys=self.getobjregionskeletonxys(regionmaskim, bwthresh=bwthresh, offset=(x1,y1))
                objregioninfos[clsname][i]['skeletonxys'] = skeletonxys

                vx, vy, x0, y0=self.getskeletonfitline(skeletonxys)
                unitdirectvect = np.array((vx, vy)) / np.sqrt(vx ** 2 + vy ** 2)
                expandlen=max(list(minrectinfo['rotrect'][1]))//2+100
                pnt0=np.array((x0,y0))
                pnt1=pnt0-expandlen * unitdirectvect
                pnt2=pnt0+expandlen * unitdirectvect
                skeletonfitlineinfo=[(vx, vy, x0, y0),tuple(pnt1),tuple(pnt2)]
                objregioninfos[clsname][i]['skeletonfitlineinfo'] = skeletonfitlineinfo




    def getcaxisintersectinfos(self,objregioninfos):
        def getminrectcaxisline(regioninfo):
            cpnts=regioninfo['minrectinfo']['cpnts']
            line= LineOpt(cpnts[1], cpnts[3])

            return line

        def getypcaxisintersectinfos(yp_regioninfos):
            ypcaxisintersectinfos=[]
            ypnum=len(yp_regioninfos)
            linecombids = list(combinations(list(range(ypnum)), 2))
            for (i,j) in linecombids:
                line_i=getminrectcaxisline(yp_regioninfos[i])
                line_j = getminrectcaxisline(yp_regioninfos[j])
                intersectpnt = line_i.get_intersection_point(line_j)
                if intersectpnt is not None:
                    ypcaxisintersectinfo=[(i,j),tuple(np.round(intersectpnt).astype(np.int32))]
                    ypcaxisintersectinfos.append(ypcaxisintersectinfo)

            return ypcaxisintersectinfos


        def get2objcaxisintersectinfos(regioninfos1,regioninfos2):
            objcaxisintersectinfos=[]
            for i,regioninfo_i in enumerate(regioninfos1):
                line_i = getminrectcaxisline(regioninfo_i)
                for j,regioninfo_j in enumerate(regioninfos2):
                    line_j = getminrectcaxisline(regioninfo_j)
                    intersectpnt = line_i.get_intersection_point(line_j)
                    if intersectpnt is not None:
                        objcaxisintersectinfo = [(i, j), tuple(np.round(intersectpnt).astype(np.int32))]
                        objcaxisintersectinfos.append(objcaxisintersectinfo)

            return objcaxisintersectinfos


        caxisintersectinfos={}
        caxisintersectinfos['yp_yp']=getypcaxisintersectinfos(objregioninfos['yp'])
        caxisintersectinfos['jc_yp']=get2objcaxisintersectinfos(objregioninfos['jc'], objregioninfos['yp'])

        return caxisintersectinfos



    



    def getmintersectpnt(self,caxisintersectinfos, skipkeys=()):
        intersectpnts = []
        for key in caxisintersectinfos.keys():
            if key in skipkeys:
                continue
            for _, intersectpnt in caxisintersectinfos[key]:
                intersectpnts.append(intersectpnt)

        mintersectpnt = tuple(np.mean(np.array(intersectpnts),axis=0).astype(np.int))
        # pntnum=len(intersectpnts)
        # pntnumcombids = list(combinations(list(range(pntnum)), 2))
        # for i,j in pntnumcombids:
        #     pntdist=pnt2pntdist(intersectpnts[i],intersectpnts[j])
            # print(pntdist)

        return mintersectpnt




    def drawkeyinfos(self,im,allinfos,impath,solveintersectmethod=2):
        objregioninfos = allinfos['objregioninfos']
        caxisintersectinfos =allinfos['caxisintersectinfos']
        mintersectpnt=allinfos['mintersectpnt']

        def drawregionminrectkeyinfos(im,objregioninfos):
            for key in objregioninfos.keys():
                for objregioninfo in objregioninfos[key]:
                    minrectinfo = objregioninfo['minrectinfo']
                    PolygonDraw().linepolygon(im, minrectinfo['rotbox'], linecolor=(255, 0, 0), linew=2)
                    for i in (1,3):
                        cv2.circle(im,minrectinfo['cpnts'][i],5,(0,255,0))
                    cv2.circle(im, minrectinfo['rotrect'][0], 5, (255, 0,0),-1)


        def drawregioncaxis(im,objregioninfos,caxisintersectinfos):
            def drawarrowline(im,intersectpnt,cpnts):
                dist1 = pnt2pntdist(intersectpnt, cpnts[1])
                dist2 = pnt2pntdist(intersectpnt, cpnts[3])
                pnt = cpnts[1]
                dist = dist1
                if dist2 > dist1:
                    pnt = cpnts[3]
                    dist = dist2
                # print(dist)
                if dist > 500:
                    tipLength = 0.04
                else:
                    tipLength = 0.2
                cv2.arrowedLine(im, intersectpnt, pnt, (255, 125, 255), 1, tipLength=tipLength)


            for key in caxisintersectinfos.keys():
                clsnames=key.split('_')
                for regionids, intersectpnt in caxisintersectinfos[key]:
                    cv2.circle(im, intersectpnt, 10, (255, 125, 255),-1)
                    for k,clsname in enumerate(clsnames):
                        if clsname=='yp':
                            if solveintersectmethod==1:
                                cpnts = objregioninfos[clsname][regionids[k]]['minrectinfo']['cpnts']
                            elif solveintersectmethod==2:
                                pnt1,pnt2 = objregioninfos[clsname][regionids[k]]['skeletonfitlineinfo'][1:]
                                cpnts=[(0,0),pnt1,(0,0),pnt2]
                        else:
                            cpnts = objregioninfos[clsname][regionids[k]]['minrectinfo']['cpnts']

                        drawarrowline(im, intersectpnt, cpnts)


        def drawskeleton(im,objregioninfos,color=(255, 255, 255)):
            for key in objregioninfos.keys():
                for objregioninfo in objregioninfos[key]:
                    skeletonxys= objregioninfo['skeletonxys']
                    for pnt in skeletonxys[::4]:
                        pnt=tuple(pnt)
                        cv2.circle(im, pnt, 1,color, -1)


        def drawskeletonfitline(im,objregioninfos,color=(0, 255, 255)):
            for key in objregioninfos.keys():
                for objregioninfo in objregioninfos[key]:
                    x0, y0=objregioninfo['skeletonfitlineinfo'][0][2:]
                    pnt = (x0,y0)
                    cv2.circle(im, pnt, 10, color)
                    pnt1,pnt2=objregioninfo['skeletonfitlineinfo'][1:]
                    cv2.line(im,pnt1,pnt2,(255,0,255),1)


        def drawxyaxis(im,pnt0):
            imhwc=im.shape
            x0,y0=pnt0
            xaxispnt1=(100,y0)
            xaxispnt2=(imhwc[1]-100, y0)
            yaxispnt1 = (x0, 100)
            yaxispnt2 = (x0, imhwc[0] - 100)
            tipLength=0.01
            cv2.arrowedLine(im, xaxispnt1, xaxispnt2, (255, 125, 255), 1, tipLength=tipLength)
            tipLength = 0.01
            cv2.arrowedLine(im, yaxispnt1, yaxispnt2, (255, 125, 255), 1, tipLength=tipLength)





        cv2.circle(im, mintersectpnt, 15, (0, 0, 255),-1)
        # drawregionminrectkeyinfos(im, objregioninfos)
        drawregioncaxis(im, objregioninfos, caxisintersectinfos)
        # drawskeleton(im, objregioninfos)
        # drawskeletonfitline(im, objregioninfos)
        drawxyaxis(im, mintersectpnt)

        cv2.imwrite(impath,im)





    def fangweijiaoprocess(self,objregioninfos,borders,im):
        self.extendobjregioninfos(objregioninfos, borders,im)

        #line intersectpnts
        caxisintersectinfos=self.getcaxisintersectinfos(objregioninfos)
        #
        mintersectpnt=self.getmintersectpnt(caxisintersectinfos, skipkeys=())

        #
        allinfos = {'objregioninfos': objregioninfos, 'caxisintersectinfos': caxisintersectinfos,
                    'mintersectpnt': mintersectpnt}


        # angle=get2vectangle(meancpnt, newjc_rotboxwc1c2c, meancpnt+np.array([0,-200]))
        return allinfos


    def testfangweijiaoprocess(self,segim):
        def getobjregioninfo(im,minpolygonarea=60*60):
            polygons,hierarchy=cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            objregioninfo = []
            for polygon in polygons:
                polygonarea=cv2.contourArea(polygon)
                if polygonarea>minpolygonarea:
                    regioninfo = {}
                    regioninfo['bndbox'] = FJSegPostProc().polygon2bndbox(polygon)
                    regioninfo['detscore'] = 1
                    regioninfo['polygon']=polygon

                    objregioninfo.append(regioninfo)

            return objregioninfo


        imhwc=segim.shape
        borders=[(0,imhwc[1]),(0,imhwc[0])]
        objregioninfos = {}
        objregioninfos['yp']=getobjregioninfo(segim[:, :, 1])
        objregioninfos['jc'] = getobjregioninfo(segim[:, :, 2])

        allinfos=self.fangweijiaoprocess(objregioninfos,borders,segim)
        impath='./test.jpg'
        self.drawkeyinfos(segim, allinfos, impath)











    def results2xml(self,results,xmlpath):
        pass



if __name__ == '__main__':
    impath='/data/project/AADQ/dev-dengqi2/SemSeg/FengJiObjprocess/testim/DJI_20210319163317_0002_Z_04680.png'
    segim=cv2.imread(impath)
    fj=FJSegPostProc()
    fj.testfangweijiaoprocess(segim)

