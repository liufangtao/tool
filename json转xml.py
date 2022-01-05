import os
import json
from lxml import etree as ET
from xml.dom import minidom


def edit_xml(objects, id, dir):
    save_xml_path = os.path.join(dir, "%s.xml" % id)  #加入xml，dir为加入路径

    root = ET.Element("annotation")
    # root.set("version", "1.0")
    folder = ET.SubElement(root, "folder")
    folder.text = "none"
    filename = ET.SubElement(root, "filename")
    filename.text = "none"
    source = ET.SubElement(root, "source")
    source.text = "Unknown"
    # owner = ET.SubElement(root, "owner")
    # owner.text = "YZN"
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(1920)
    height = ET.SubElement(size, "height")
    height.text = str(1080)
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"
    for obj in objects:  #
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")  # number
        # name.text = obj["category"] # "meter"
        name.text = "meter"
        # meaning = ET.SubElement(object, "meaning")  # name
        # meaning.text = inf_value[0]
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(object, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        print(str(obj))
    #     xmin.text = int(obj)
    #     # xmin.text = str(obj["bbox"]["xmin"])
    #     ymin = ET.SubElement(bndbox, "ymin")
    #     ymin.text = str(int(obj["bbox"]["ymin"]))
    #     xmax = ET.SubElement(bndbox, "xmax")
    #     xmax.text = str(int(obj["bbox"]["xmax"]))
    #     ymax = ET.SubElement(bndbox, "ymax")
    #     ymax.text = str(int(obj["bbox"]["ymax"]))
    # tree = ET.ElementTree(root)
    # tree.write(save_xml_path, encoding="UTF-8", xml_declaration=True)
    # root = ET.parse(save_xml_path)
    # file_lines = minidom.parseString(ET.tostring(root, encoding="Utf-8")).toprettyxml(
    #     indent="\t")
    # file_line = open(save_xml_path, "w", encoding="utf-8")
    # file_line.write(file_lines)
    # file_line.close()


def getDirId(dir):  # get the  id list  of id.png
    names = os.listdir(dir)
    ids = []
    for name in names:
        # path = os.path.join(dir, name)
        # img  = cv2.imread(path)
        # w, h, c = img.shape
        # if name.endswith(".jpg") or name.endswith(".png"):
        # ids["%s" % name.split(".")[0]] = [w, h, c]
        ids.append(name.split(".")[0])
    return ids


filedir = "D:\\build\\meter_det\\annotations\\instance_train.json"#json文件的文件路径
annos = json.loads(open(filedir).read())

trainIds = getDirId("D:\\build\\meter_det\\train\\")#用于训练的图片的路径，用于获取图片ID
testIds = getDirId("D:\\build\\meter_det\\test\\")

# dirs = annos.keys()
# print(dirs)


# for dir in dirs:
#     print(dir)
#     # for di in dir
names = annos["images"]
ids = annos["annotations"]  # 读取json文件中的所有图片id .keys()
# print(ids[1])
for name in names:
    # print(name['file_name'].split('.')[0])
    if name['file_name'].split('.')[0] in trainIds:
        for id in ids:
            if len(id["bbox"]) > 0 and id["image_id"] == name['id']:
                objects = id["bbox"]
                # print(objects)
                edit_xml(objects, name['file_name'].split('.')[0], dir="D:\\build\\meter_det\\trainxml")





# for id in ids:
#     print(id,name)
#      # json 中的ID图片，若有待检测目标，且该id图片在 train文件夹中，则生成此图片的xml文件，加入train文件中
#     if len(annos["annotations"][id]["bbox"]) > 0 and (annos["annotations"][id]["image_id"]in trainIds) :
#         objects = annos["annotations"][id]["bbox"]
#         edit_xml(objects, id, dir="D:\\build\\meter_det\\trainxml")

#     elif len(annos["annotations"][id]["objects"]) > 0 and (id in testIds):#同上，将xml文件加入测试文件夹
#         objects = annos["annotations"][id]["objects"]
#         edit_xml(objects, id, dir="D:\\build\\meter_det\\testxml")
