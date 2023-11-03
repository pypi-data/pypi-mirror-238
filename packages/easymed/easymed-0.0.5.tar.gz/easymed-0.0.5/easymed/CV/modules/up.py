import torch
from torch import nn

__all__ = ['Bilinear', 'ConvTranspose']


class Bilinear(nn.Module):
    def __init__(self, in_channel: int,
                 out_channel: int):
        super(Bilinear, self).__init__()
        self.Up = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 1, 1),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        )

    def forward(self, x):
        return self.Up(x)


class ConvTranspose(nn.Module):
    def __init__(self, in_channel: int,
                 out_channel: int):
        super(ConvTranspose, self).__init__()
        self.Up = nn.ConvTranspose2d(in_channel , out_channel, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1)

    def forward(self, x):
        return self.Up(x)