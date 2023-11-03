from typing import Type
import torch
import torch.nn as nn

def binary(tensor: Type[torch.Tensor], threshold: float=0.5) -> Type[torch.Tensor]:
    func = nn.Sigmoid()
    tensor = func(tensor)
    tensor[tensor >= threshold] = 1
    tensor[tensor < threshold] = 0
    return tensor