import torch
def get_device(device_name:str):
    device = 'cpu' if device_name is None else torch.device(f'cuda:{device_name}')
    return device
