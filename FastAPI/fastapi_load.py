#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作者: liufangtao
创建时间: 2024-04-30
最后修改时间: 2024-05-15
脚本功能说明:
    任务对应模型加载。
    模型计数。
    任务对应模型卸载。
"""
import ultralytics

import torch
from typing import List, Dict

# 定义模型缓存字典
model_cache = {}

# 定义模型加载器类
class ModelLoader:
    def __init__(self, task_to_model_map, task_name=None):
        self.task_to_model_map = task_to_model_map
        self.task_name = task_name
        self.loaded_models = self.load_models()

    def load_models(self):
        loaded_models = {}
        model_names = self.task_to_model_map.get(self.task_name, []) if self.task_name else [
            model_name for sublist in self.task_to_model_map.values() for model_name in sublist]

        for model_name in model_names:
            # 检查模型是否已缓存
            if model_name in model_cache:
                loaded_models[model_name] = model_cache[model_name]
            else:
                try:
                    model = ultralytics.YOLO(f'{model_name}.pt')
                    model_cache[model_name] = model
                    loaded_models[model_name] = model
                except MemoryError:
                    self.release_memory()
                    break
        # print(loaded_models)
        return loaded_models

    def check_gpu_memory(self):
        # 获取当前显存使用情况
        mem_allocated = torch.cuda.memory_allocated()
        mem_reserved = torch.cuda.memory_reserved()
        # 获取显存总容量
        mem_total = torch.cuda.get_device_properties(0).total_memory
        # 设置显存使用阈值
        threshold = mem_total * 0.85
        # 如果当前已分配和保留的显存超过阈值，返回False
        return mem_allocated + mem_reserved <= threshold

    def release_memory(self):
        # 释放已加载模型的显存
        for model in list(model_cache.values()):
            del model
        torch.cuda.empty_cache()

# 定义任务到模型映射的字典
task_to_model_map = {
    "行人检测": ["models/yolov8s"],
    "车辆检测": ["models/yolov8s"],
    "没穿反光衣检测": ["models/person_hardhat_head_safetyvest_hand"],
    "没戴安全帽检测": ["models/person_hardhat_head_safetyvest_hand"],
    "灭火器检测": ["models/灭火器_烟_火_口罩_老鼠"],
    "烟火检测": ["models/灭火器_烟_火_口罩_老鼠"],
    "没戴口罩检测": ["models/灭火器_烟_火_口罩_老鼠"],
    "老鼠检测": ["models/灭火器_烟_火_口罩_老鼠"],
    "睡岗检测": ["models/sleep_nosleep"],
    "吸烟检测": ["models/hand","models/cigarette_other_phone_classify"],
    "打电话检测": ["models/hand","models/cigarette_other_phone_classify"],
    "行人跟踪": ["models/yolov8s-seg"],
    "车辆跟踪": ["models/yolov8s-seg"],
    # ... 可以添加更多映射关系 
}

# 定义计数所有任务中模型的函数
def count_all_models_across_tasks(task_names: List[str], task_to_model_map: Dict[str, List[str]]) -> Dict[str, int]:
    model_count = {}
    for task_name in task_names:
        for model in task_to_model_map.get(task_name, []):
            model_count[model] = model_count.get(model, 0) + 1
    return model_count

# 定义卸载特定任务模型的函数
def unload_models_for_task(task_name, model_count):
    for model_name in task_to_model_map.get(task_name, []):
        if model_name in model_count:
            model_count[model_name] -= 1
            if model_count[model_name] == 0:
                del model_cache[model_name]
                torch.cuda.empty_cache()


