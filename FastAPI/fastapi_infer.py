#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作者: liufangtao
创建时间: 2024-04-30
最后修改时间: 2024-05-15
脚本功能说明:
    任务对应模型对图片batch推理。  
    
"""
from typing import List, Dict, Any
from fastapi_load import *
from fastapi_utils import *
class Inferencer:
    # 定义中英文任务名称映射表
    task_map = {
        '行人检测': 'infer_person_from_cache',
        '没穿反光衣检测': 'infer_nosafetyvest_from_cache',
        '没戴安全帽检测': 'infer_head_from_cache',
        '车辆检测': 'infer_bus_from_cache',
        '灭火器检测': 'infer_extinguisher_from_cache',
        '烟火检测': 'infer_smokefire_from_cache',
        '没戴口罩检测': 'infer_unmask_from_cache',
        '老鼠检测': 'infer_rat_from_cache',
        '睡岗检测': 'infer_sleep_from_cache',
        '吸烟检测': 'infer_cigarette_from_cache',
        '打电话检测': 'infer_phone_from_cache',
        '行人跟踪' : 'infer_person_track_from_cache',
        '车辆跟踪' : 'infer_bus_track_from_cache',
    }

    def __init__(self, image_paths: List[str], task_name: str):
        self.image_paths = image_paths
        self.task_name = task_name

    def infer(self) -> Dict[str, Any]:
        method_name = self.task_map.get(self.task_name)
        if not method_name:
            raise ValueError(f"不支持的任务名称: {self.task_name}")

        method = getattr(self, method_name, None)
        if not method:
            raise ValueError(f"方法不存在: {method_name}")

        return method()

    # 抽象通用检测推理方法
    def _infer_from_cache(self, task_name: str, class_id: int, conf: float =0.45) -> Dict[str, Any]:
        task_result = {
            "task_name": task_name,
            "results": []
        }

        model_names_for_task = task_to_model_map.get(task_name, [])
        for model_name in model_names_for_task:
            model = model_cache.get(model_name)
            if not model:
                continue
            if model.model.task== 'detect':
                for i in range(0, len(self.image_paths), 8):
                    source_group = self.image_paths[i:i+8]
                    # print(source_group)
                    for result in model(source=source_group, conf=conf, imgsz=640, device=0, classes=class_id):
                        re_all = {
                            "cls": (result.boxes.cls).tolist(),
                            "conf": (result.boxes.conf).tolist(),
                            "boxes": (result.boxes.xywh).tolist()
                        }
                        task_result["results"].append(re_all)
            elif model.model.task== 'segment':
                for i in range(0, len(self.image_paths), 8):
                    source_group = self.image_paths[i:i+8]
                    # print(source_group)
                    for result in model.track(source=source_group, conf=conf, persist=True, imgsz=640, device=0, classes=class_id):
                        re_all = {
                            "cls": (result.boxes.cls).tolist(),
                            "conf": (result.boxes.conf).tolist(),
                            "boxes": (result.boxes.xywh).tolist()
                        }
                        task_result["results"].append(re_all)
        return task_result
    # 抽象通用跟踪推理方法
    def _infer_track_from_cache(self, task_name: str, class_id: int, conf: float =0.45) -> Dict[str, Any]:
        task_result = {
            "task_name": task_name,
            "results": []
        }

        model_names_for_task = task_to_model_map.get(task_name, [])
        for model_name in model_names_for_task:
            model = model_cache.get(model_name)
            if not model:
                continue
            if model.model.task== 'detect':
                for i in range(0, len(self.image_paths), 8):
                    source_group = self.image_paths[i:i+8]
                    # print(source_group)
                    for result in model.track(source=source_group, conf=conf, persist=True, imgsz=640, device=0, classes=class_id):
                        re_all = {
                            "cls": (result.boxes.cls).tolist(),
                            "conf": (result.boxes.conf).tolist(),
                            "boxes": (result.boxes.xywh).tolist()
                        }
                        task_result["results"].append(re_all)
        return task_result
    # 抽象通用串行检测推理方法
    def _infer_serial_from_cache(self, task_name: str, class1_id: int, class2_id: int, conf: float = 0.45) -> Dict[str, Any]:
        task_result = {
            "task_name": task_name,
            "results": []
        }

        model_names_for_task = task_to_model_map.get(task_name, [])
        yolov8s_model_name, yolov8s_cls_model_name = model_names_for_task
        print(yolov8s_model_name, yolov8s_cls_model_name)

        yolov8s_model = model_cache.get(yolov8s_model_name)
        yolov8s_cls_model = model_cache.get(yolov8s_cls_model_name)

        if not yolov8s_model or not yolov8s_cls_model:
            return task_result

        # 使用yolov8s模型进行检测
        for i in range(0, len(self.image_paths), 8):
            source_group = self.image_paths[i:i+8]
            # print(source_group)
            detections = yolov8s_model(source=source_group, conf=conf, imgsz=640, device=0, classes=class1_id)
            
            # 遍历检测结果
            for detection in detections:
                re_all = {"cls": [], "conf": [], "boxes": []} 
                # 裁剪图片
                cropped = crop_image(detection.orig_img, detection.boxes.xywh.tolist()) #expand_mvboxes(detection.orig_img,box,1.5)
                
                # 使用yolov8s-cls模型进行分类
                classification_results = yolov8s_cls_model(source=cropped, device=0)

                # 遍历分类结果
                for i, result in enumerate(classification_results):
                    if result.probs.top1 == class2_id:  # 如果分类结果是0类
                        re_all["cls"].append(detection.boxes.cls[i].tolist())
                        re_all["conf"].append(detection.boxes.conf[i].tolist())
                        re_all["boxes"].append(detection.boxes.xywh[i].tolist())
                     
                task_result["results"].append(re_all)
        return task_result




    # 特定任务的推理方法 
    def infer_person_from_cache(self):
        return self._infer_from_cache('行人检测', 0)

    def infer_head_from_cache(self):
        return self._infer_from_cache('没戴安全帽检测', 2, conf=0.3)

    def infer_nosafetyvest_from_cache(self):
        task_result = self._infer_from_cache('没穿反光衣检测', [0, 3], conf=0.3)
        
        # 过滤结果，只保留检测到0类而没检测到3类的情况
        filtered_results = []
        for result in task_result["results"]:
            if any(cls == 0 for cls in result["cls"]) and not any(cls == 3 for cls in result["cls"]):
                filtered_results.append(result)
            if not any(cls == 0 for cls in result["cls"]) and not any(cls == 3 for cls in result["cls"]):
                filtered_results.append(result)

        task_result["results"] = filtered_results
        return task_result


    def infer_bus_from_cache(self):
        return self._infer_from_cache('车辆检测', [1,2,3,5,7]) #1：自行车 2：汽车 3：摩托车 5:公交车 7：卡车

    def infer_extinguisher_from_cache(self):
        return self._infer_from_cache('灭火器检测', 0)
    
    def infer_smokefire_from_cache(self):
        return self._infer_from_cache('烟火检测', [1,2])
    
    def infer_unmask_from_cache(self):
        return self._infer_from_cache('没戴口罩检测', 3)
    
    def infer_rat_from_cache(self):
        return self._infer_from_cache('老鼠检测', 5)
    
    def infer_sleep_from_cache(self):
        return self._infer_from_cache('睡岗检测', 0)
    
    def infer_cigarette_from_cache(self):
        return self._infer_serial_from_cache('吸烟检测', class1_id=0, class2_id=0)
    
    def infer_phone_from_cache(self):
        return self._infer_serial_from_cache('打电话检测', class1_id=0, class2_id=2)
    
    def infer_person_track_from_cache(self):
        return self._infer_from_cache('行人跟踪', 0)
    
    def infer_bus_track_from_cache(self):
        return self._infer_from_cache('车辆跟踪', [1,2,3,5,7]) #1：自行车 2：汽车 3：摩托车 5:公交车 7：卡车