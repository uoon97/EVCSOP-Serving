from datetime import datetime
# transform json to model's input
import json
import torch

def get_dt():
    now = datetime.now()
    dt = datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

def json_to_tensor(json_data):
    X = []
    for key in json_data.keys():
        X.append(list(json_data[key].values()))

    return torch.tensor(X)

def tensor_to_json(outputs):
    dict = {}
    for idx, output in enumerate(outputs):
        dict[idx] = int(output)
    
    return json.dumps(dict)