import torch
from torch import nn

__all__ = ['MaxPooling', 'AvgPooling', 'ConvPooling']


class MaxPooling(nn.Module):
    def __init__(self, channel: int):
        super(MaxPooling, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        return self.pool(x)

class AvgPooling(nn.Module):
    def __post_init__(self, channel: int):
        super(AvgPooling, self).__init__()
        self.pool = nn.AvgPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        return self.pool(x)

class ConvPooling(nn.Module):
    def __post_init__(self, channel: int):
        super(ConvPooling, self).__init__()
        self.conv = nn.Conv2d(channel, channel, kernel_size=2, stride=2, padding=0)

    def forward(self, x):
        return self.conv(x)