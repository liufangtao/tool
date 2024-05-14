#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作者: liufangtao
创建时间: 2024-04-30
最后修改时间: 2024-05-15
脚本功能说明:
    fastapi三个post接口：任务对应模型加载、模型推理、模型卸载；
"""
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Any
import base64
import uvicorn
from PIL import Image
import io
from fastapi_infer import Inferencer
from fastapi_load import *
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

app = FastAPI()

class TaskInfo(BaseModel):
    task_name: str

class TasksModel(BaseModel):
    task_info: List[TaskInfo]

# class ImageData(BaseModel): 
#     task_name: str
#     image: List[str] = Field(..., description="List of base64 encoded images")
class ImageData(BaseModel):
    task_name: str
    image: List[Union[UploadFile, str]]

class InferenceRequest(BaseModel):
    data_info: List[ImageData]

class InferImageRequest(BaseModel):
    task_name: str = Field(..., description="任务名称")
    files: List[UploadFile] = Field(..., description="上传的文件列表")

loaded_tasks = set()

@app.post("/matrix/model_load/")
async def load_models(request: TasksModel):
    global model_count
    try:
        t_names = set(item.task_name for item in request.task_info)
        # print(t_names)

        duplicate_models = [t_name for t_name in t_names if t_name in loaded_tasks]
        message = "Models loaded successfully"
        for t_name in t_names:
            if t_name not in task_to_model_map:
                message += f", Task: {t_name} not found in the tasks list"
        
            else:
                ModelLoader(task_to_model_map, t_name)
                loaded_tasks.add(t_name)
    
              
        model_count = count_all_models_across_tasks(loaded_tasks, task_to_model_map)
        

        
        if duplicate_models:
            message += f", 这任务已经存在列表中: {', '.join(duplicate_models)}"

        return {"message": message, "Existing tasks": loaded_tasks, "Total_models_loaded": model_count}
    except MemoryError:
        raise HTTPException(status_code=400, detail="Memory error occurred while loading models")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/matrix/infer_image/")
# async def infer_image(request: InferenceRequest):
#     try:
#         data_info = {"data_info": []}
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             futures = []
#             for item in request.data_info:
#                 task_n = item.task_name
#                 images = item.image

#                 image_paths = []
#                 for img in images:
#                     if isinstance(img, UploadFile):
#                         # 处理 UploadFile 格式的图像
#                         img_data = await img.read()
#                         image = Image.open(io.BytesIO(img_data))
#                     elif isinstance(img, str):
#                         # 处理 base64 编码的图像
#                         image_data = base64.b64decode(img)
#                         image = Image.open(io.BytesIO(image_data))
#                     else:
#                         raise HTTPException(status_code=400, detail="不支持的图像格式")

#                     image_paths.append(image)

#                 future = executor.submit(Inferencer(image_paths, task_n).infer)
#                 futures.append(future)

#             for future in futures:
#                 task_result = future.result()
#                 data_info["data_info"].append(task_result)

#         return data_info
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/matrix/infer_image/")
# async def infer_image(request: InferenceRequest):
#     try:
#         data_info = {"data_info": []}
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             futures = []
#             for item in request.data_info:
#                 task_n = item.task_name
#                 images = item.image

#                 image_paths = []
#                 for img in images:
#                     # 检查图像是否为 base64 编码
#                     if isinstance(img, BytesIO):
#                         # 处理 BytesIO 格式的图像
#                         # print(img)
#                         img_data = await img.read()
#                         image = Image.open(BytesIO(img_data))
#                     else:
#                         # 处理 base64 编码的图像
#                         image_data = base64.b64decode(img)
#                         image = Image.open(io.BytesIO(image_data))

#                     image_paths.append(image)

#                 future = executor.submit(Inferencer(image_paths, task_n).infer)
#                 futures.append(future)

#             for future in futures:
#                 task_result = future.result()
#                 data_info["data_info"].append(task_result)

#         return data_info
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/matrix/infer_image/")
# async def infer_image(task_list: List[Dict[str, Any]]):
#     try:
#         data_info = {"data_info": []}

#         for task in task_list:
#             task_name = task["task_name"]
#             files = task["image"]
#             images = []
#             for file in files:
#                 print(file)
#                 image_data = await file.read()
#                 image = Image.open(BytesIO(image_data))
#                 images.append(image)

#             inferencer = Inferencer(images, task_name)
#             with ThreadPoolExecutor(max_workers=10) as executor:
#                 future = executor.submit(inferencer.infer)
#                 task_result = future.result()
#                 data_info["data_info"].append(task_result)

#         return data_info
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/matrix/infer_image/")
# async def infer_image(task_name: str, files: List[UploadFile] = File(...)):
#     try:
#         data_info = {"data_info": []}
#         image_paths = []

#         for file in files:
#             image_data = await file.read()
#             image = Image.open(BytesIO(image_data))
#             image_paths.append(image)

#         # 假设 Inferencer 可以处理多个图像
#         inferencer = Inferencer(image_paths, task_name)
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             future = executor.submit(inferencer.infer)
#             task_result = future.result()
#             data_info["data_info"].append(task_result)

#         return data_info
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@app.post("/matrix/infer_image/")
async def infer_image(request: InferenceRequest):
    try:
        data_info = {"data_info": []}
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for item in request.data_info:
                task_n = item.task_name
                image_base64 = item.image

                image_paths = []
                for img_base64 in image_base64:
                    image_data = base64.b64decode(img_base64)
                    image = Image.open(io.BytesIO(image_data))
                    image_paths.append(image)
                
                future = executor.submit(Inferencer(image_paths, task_n).infer)
                futures.append(future)

            for future in futures:
                task_result = future.result()
                data_info["data_info"].append(task_result)

        return data_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/matrix/model_unload/")
async def unload_models(request: TasksModel):
    try:
        unt_names = [item.task_name for item in request.task_info if item.task_name in loaded_tasks]

        for unt_name in unt_names:
            unload_models_for_task(unt_name, model_count)
            loaded_tasks.remove(unt_name)

        return {"message": "Models unloaded successfully", "Residual tasks": loaded_tasks, "Residual models": model_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="10.18.97.96", port=7300, log_level="info", reload=True)

