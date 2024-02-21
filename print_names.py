
import torch
from models.experimental import attempt_load

def get_names(modelfile):
    model = attempt_load(modelfile, map_location=torch.device('cpu'))
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    return names
    

if __name__=="__main__":
    modelfile = '/home/liufangtao/下载/bj安全帽/model.pt'
    names = get_names(modelfile)
    print(names)
