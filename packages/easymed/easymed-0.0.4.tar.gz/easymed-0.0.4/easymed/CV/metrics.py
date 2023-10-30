from typing import Union
import numpy as np
import torch

def dice(a: Union[np.ndarray, torch.Tensor], b: Union[np.ndarray, torch.Tensor]) -> float:
    return 2 * (a.bool() & b.bool()).long().sum() / (a.sum() + b.sum())

def iou(a: Union[np.ndarray, torch.Tensor], b: Union[np.ndarray, torch.Tensor]) -> float:
    return (a.bool() & b.bool()).long().sum() / (a.bool() | b.bool()).long().sum()