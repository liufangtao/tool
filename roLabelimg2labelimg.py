import os
import xml.etree.ElementTree as ET
import math


def edit_xml(xml_file):
    """
    修改xml文件
    :param xml_file:xml文件的路径
    :return:
    """
    if xml_file.endswith(".xml"):
        tree = ET.parse(xml_file)
        objs = tree.findall('object')
        for ix, obj in enumerate(objs):
            xmin = ET.Element("xmin") # 创建节点
            ymin = ET.Element("ymin")
            xmax = ET.Element("xmax")
            ymax = ET.Element("ymax")
            obj_type = obj.find('type')
            if obj_type is None:
                pass
            else:
                type = obj_type.text
                print(type)
                print(xml_file)
                if type == 'bndbox':
                    pass
                elif type == 'robndbox':
                    obj_bnd = obj.find('robndbox')
                    obj_bnd.tag = 'bndbox'   # 修改节点名
                    obj_cx = obj_bnd.find('cx')
                    obj_cy = obj_bnd.find('cy')
                    obj_w = obj_bnd.find('w')
                    obj_h = obj_bnd.find('h')
                    obj_angle = obj_bnd.find('angle')
                    cx = float(obj_cx.text)
                    cy = float(obj_cy.text)
                    w = float(obj_w.text)
                    h = float(obj_h.text)
                    angle = float(obj_angle.text)
                    obj_bnd.remove(obj_cx)  # 删除节点
                    obj_bnd.remove(obj_cy)
                    obj_bnd.remove(obj_w)
                    obj_bnd.remove(obj_h)
                    obj_bnd.remove(obj_angle)


                    xmin.text, ymin.text = rotatePoint(cx, cy, cx - w / 2, cy - h / 2, -angle)
                    xmax.text, ymax.text = rotatePoint(cx, cy, cx + w / 2, cy + h / 2, -angle)
                    obj.remove(obj_type)  # 删除节点
                    obj_bnd.append(xmin)  # 新增节点
                    obj_bnd.append(ymin)
                    obj_bnd.append(xmax)
                    obj_bnd.append(ymax)
                    tree.write(xml_file,method='xml', encoding='utf-8')  # 更新xml文件

# 转换成四点坐标
def rotatePoint(xc, yc, xp, yp, theta):
    xoff = xp - xc
    yoff = yp - yc
    cosTheta = math.cos(theta)
    sinTheta = math.sin(theta)
    pResx = cosTheta * xoff + sinTheta * yoff
    pResy = - sinTheta * xoff + cosTheta * yoff
    return str(int(xc + pResx)), str(int(yc + pResy))

if __name__ == '__main__':
    dir=r"F:\jyzall\all\xmls"
    filelist = os.listdir(dir)
    for file in filelist:
        edit_xml(os.path.join(dir,file))
