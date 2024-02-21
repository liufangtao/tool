

import argparse
import numpy as np
import torch

# from models.common import *

if __name__ == '__main__':

    weights_path = '/run/user/1000/gvfs/smb-share:server=10.18.103.158,share=share/private/liufangtao/models/打电话/weights/best.pt'
    is_half = True

    # Load pytorch model
    model = torch.load(weights_path, map_location=torch.device('cuda'))

    net = model['model']

    if is_half:
        net.half() # 把FP32转为FP16

    # print(model)

    ckpt = {'epoch': -1,
            'best_fitness': model['best_fitness'],
            'training_results': None,
            'model': net,
            'optimizer': None}

    # Save .pt
    torch.save(ckpt, '/run/user/1000/gvfs/smb-share:server=10.18.103.158,share=share/private/liufangtao/models/打电话/weights/test.pt')
    # for name, parameters in model.named_parameters():
    #     # print(name,':',parameters.size())
    #     print(parameters.dtype)
