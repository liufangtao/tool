def main(args):
    # 获取待预测图像列表
    # image_file_list = get_image_file_list(args.image_dir)
    ######################################
    # 读取摄像头数据流
    cap = cv2.VideoCapture(0)
    # 加载OCR模型系统
    text_sys = TextSystem(args)
    # 是否开启可视化
    is_visualize = True
    # 遍历待预测图像列表
    # for image_file in image_file_list:
        # 检查图像
        # img, flag = check_and_read_gif(image_file)
        # 若为出错则读取图像
        # if not flag:
        #     img = cv2.imread(image_file)
        # 如果图像为空报错并继续
        # if img is None:
        #     logger.info("error in loading image:{}".format(image_file))
        #     continue
    ######################################
    while True:
        # 读取视频帧
        success, img = cap.read()
        # 计时开始
        starttime = time.time()
        # 模型预测
        dt_boxes, rec_res = text_sys(img)
        # 计算预测时间
        elapse = time.time() - starttime
        # 打印预测时间
        # print("Predict time of %s: %.3fs" % (image_file, elapse))
        # 设置丢弃分数
        drop_score = 0.5
        # 计算预测框数量
        dt_num = len(dt_boxes)
        # 遍历预测结果若大于阈值则打印
        for dno in range(dt_num):
            text, score = rec_res[dno]
            if score >= drop_score:
                text_str = "%s, %.3f" % (text, score)
                print(text_str)
        # 可视化
        if is_visualize:
            # 图像格式转换
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # 获取预测框、文本结果和分数
            boxes = dt_boxes
            txts = [rec_res[i][0] for i in range(len(rec_res))]
            scores = [rec_res[i][1] for i in range(len(rec_res))]
            
            # 结果绘制
            draw_img = draw_ocr_box_txt(image, boxes, txts)
            ######################################
            # 窗口显示
            cv2.imshow('img', draw_img[:, :, ::-1])
            # 显示等待
            k = cv2.waitKey(1)
            # 如果按下Esc键则退出程序
            if k==27:
                break
            # 结果图像保存路径
            # draw_img_save = "./inference_results/"
            # 若保存目录不存在则创建
            # if not os.path.exists(draw_img_save):
            #     os.makedirs(draw_img_save)
            # 保存结果图像
            # cv2.imwrite(
            #     os.path.join(draw_img_save, os.path.basename(image_file)),
            #     draw_img[:, :, ::-1])
            # 打印日志
            # print("The visualized image saved in {}".format(
            #     os.path.join(draw_img_save, os.path.basename(image_file))))