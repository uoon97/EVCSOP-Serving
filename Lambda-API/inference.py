# model inference API
import torch
from utils import json_to_tensor, tensor_to_json

def handler(event, context):
    """
    event = {
        "0": {
            "latitude": 39.7145,
            "longitude": 127.9425,
            ...
        },
    }
    """
    model = torch.jit.load('model.pt')
    sids, inputs =  json_to_tensor(event)
    outputs = model(inputs)

    return tensor_to_json(sids, outputs)

