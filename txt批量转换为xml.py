from xml.dom.minidom import Document
import os
import cv2

'''
  dict = {'0': "person",#字典对类型进行转换
                '1': "hardhat",
                '2': "head",
                '3': "safetyvest",
                '4': "hand",
                '5': "unmask",
                '6': "mask"
                }
                {'0': "extinguisher",#字典对类型进行转换{ '0':'broken','1':'burr','2':'chip','3':'crack','4':'brokenbat','5':'burrbat','6':'chipbat','7':'crackbat'}
                '1': "smoke",
                '2': "fire",
                '3': "rat"
                }{ '0':'aodian','1':'kajiawei','2':'dantudian','3':'heneiyiwu','4':'shenhuashang','5':'weihuashang','6':'jingshujingsuan','7':'yejingbuling','8':'yejingqipao','9':'zangwu','10':'shuibowen'}
{ '0':'aodian','0.0':'aodian','1':'kajiawei','1.0':'kajiawei','2':'dantudian','2.0':'dantudian','3':'heneiyiwu','3.0':'heneiyiwu','4':'shenhuashang','4.0':'shenhuashang','5':'weihuashang','5.0':'weihuashang','6':'jingshujingsuan','6.0':'jingshujingsuan','7':'yejingbuling','7.0':'yejingbuling','8':'yejingqipao','8.0':'yejingqipao','9':'zangwu','9.0':'zangwu','10':'shuibowen','10.0':'shuibowen'}
                
                '''

def makexml(txtPath,xmlPath,picPath): #读取txt路径，xml保存路径，数据集图片所在路径
        dict = { '0':'aodian','0.0':'aodian','1':'kajiawei','1.0':'kajiawei','2':'dantudian','2.0':'dantudian','3':'heneiyiwu','3.0':'heneiyiwu','4':'shenhuashang','4.0':'shenhuashang','5':'weihuashang','5.0':'weihuashang','6':'jingshujingsuan','6.0':'jingshujingsuan','7':'yejingbuling','7.0':'yejingbuling','8':'yejingqipao','8.0':'yejingqipao','9':'zangwu','9.0':'zangwu','10':'shuibowen','10.0':'shuibowen'}
        files = os.listdir(txtPath)
        for i, name in enumerate(files):
          xmlBuilder = Document()
          annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
          xmlBuilder.appendChild(annotation)
          print(name)
          txtFile=open(txtPath+name)
          txtList = txtFile.readlines()
          img = cv2.imread(picPath+name[0:-4]+".jpg")
          Pheight,Pwidth,Pdepth=img.shape
          for i in txtList:
             oneline = i.strip().split(" ")
 
             folder = xmlBuilder.createElement("folder")#folder标签
             folderContent = xmlBuilder.createTextNode("VOC2007")
             folder.appendChild(folderContent)
             annotation.appendChild(folder)
 
             filename = xmlBuilder.createElement("filename")#filename标签
             filenameContent = xmlBuilder.createTextNode(name[0:-4]+".jpg")
             filename.appendChild(filenameContent)
             annotation.appendChild(filename)
 
             size = xmlBuilder.createElement("size")  # size标签
             width = xmlBuilder.createElement("width")  # size子标签width
             widthContent = xmlBuilder.createTextNode(str(Pwidth))
             width.appendChild(widthContent)
             size.appendChild(width)
             height = xmlBuilder.createElement("height")  # size子标签height
             heightContent = xmlBuilder.createTextNode(str(Pheight))
             height.appendChild(heightContent)
             size.appendChild(height)
             depth = xmlBuilder.createElement("depth")  # size子标签depth
             depthContent = xmlBuilder.createTextNode(str(Pdepth))
             depth.appendChild(depthContent)
             size.appendChild(depth)
             annotation.appendChild(size)
 
             object = xmlBuilder.createElement("object")
             picname = xmlBuilder.createElement("name")

             print(oneline[0])
             if len(oneline[0])== 0: continue
             nameContent = xmlBuilder.createTextNode(dict[oneline[0]])
             picname.appendChild(nameContent)
             object.appendChild(picname)
             pose = xmlBuilder.createElement("pose")
            #  poseContent = xmlBuilder.createTextNode("Unspecified")
             poseContent = xmlBuilder.createTextNode("0")
             pose.appendChild(poseContent)
             object.appendChild(pose)
             truncated = xmlBuilder.createElement("truncated")
             truncatedContent = xmlBuilder.createTextNode("0")
             truncated.appendChild(truncatedContent)
             object.appendChild(truncated)
             difficult = xmlBuilder.createElement("difficult")
             difficultContent = xmlBuilder.createTextNode("0")
             difficult.appendChild(difficultContent)
             object.appendChild(difficult)
             bndbox = xmlBuilder.createElement("bndbox")
             xmin = xmlBuilder.createElement("xmin")
             mathData=int(((float(oneline[1]))*Pwidth+1)-(float(oneline[3]))*0.5*Pwidth)
             xminContent = xmlBuilder.createTextNode(str(mathData))
             xmin.appendChild(xminContent)
             bndbox.appendChild(xmin)
             ymin = xmlBuilder.createElement("ymin")
             mathData = int(((float(oneline[2]))*Pheight+1)-(float(oneline[4]))*0.5*Pheight)
             yminContent = xmlBuilder.createTextNode(str(mathData))
             ymin.appendChild(yminContent)
             bndbox.appendChild(ymin)
             xmax = xmlBuilder.createElement("xmax")
             mathData = int(((float(oneline[1]))*Pwidth+1)+(float(oneline[3]))*0.5*Pwidth)
             xmaxContent = xmlBuilder.createTextNode(str(mathData))
             xmax.appendChild(xmaxContent)
             bndbox.appendChild(xmax)
             ymax = xmlBuilder.createElement("ymax")
             mathData = int(((float(oneline[2]))*Pheight+1)+(float(oneline[4]))*0.5*Pheight)
             ymaxContent = xmlBuilder.createTextNode(str(mathData))
             ymax.appendChild(ymaxContent)
             bndbox.appendChild(ymax)
             object.appendChild(bndbox)
 
             annotation.appendChild(object)
 
          f = open(xmlPath+name[0:-4]+".xml", 'w')
          xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
          f.close()



txtPath = '/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/ManuVision/new_gls/labels/'
xmlPath = '/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/ManuVision/new_gls/annotations/'
picPath = '/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/ManuVision/new_gls/images/'
makexml(txtPath,xmlPath,picPath)