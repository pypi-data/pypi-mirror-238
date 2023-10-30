import torch
from torch import nn

__all__ = ['Bilinear']


class Bilinear(nn.Module):
    def __init__(self, channel: int):
        super(Bilinear, self).__init__()
        self.Up = nn.Sequential(
            nn.Conv2d(channel, channel // 2, 1, 1),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        )

    def forward(self, x):
        return self.Up(x)