import os

YOLOV5_LABEL_ROOT = r"/1T/liufangtao/yolov5_crossplatform/inference/txts/"  # yolov5 导出的推理图片的 txt
DATASET_LABEL_ROOT = r"/run/user/1000/gvfs/sftp:host=10.18.97.155/home/ainnovation/disk/DATASETS/MatrixVision/佩戴口罩/mask_detect_voc_yolo_7959_20230612/mask/labels5unmask_6mask/"  # 数据集的路径

if __name__ == '__main__':
    yolo_file = os.listdir(YOLOV5_LABEL_ROOT)

    # 遍历文件里面有 .txt 结尾的
    for file_name in yolo_file:

        # 判断 txt 文件才进行读取
        if not file_name.endswith(".txt"):
            continue

        file_path = YOLOV5_LABEL_ROOT + file_name
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r") as f:
            for line in f.readlines():

                # 只需要提取 0 -> person 的数据
                # if line.split()[0] != '0':
                #     continue

                data_path = DATASET_LABEL_ROOT + file_name
                print(data_path)
                # 汇总到数据集的标注文件
                with open(data_path, "a") as fd:
                    fd.write(line)
