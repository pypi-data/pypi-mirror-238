import torch
from torch import nn
from torch.nn import functional as F

__all__ = ['VGGBlock', 'ResidualBlock', 'BottleNeck', 'Attention', 'DilatedConv']


class VGGBlock(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 num: int = 2):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num = num
        super(VGGBlock, self).__init__()
        self.layers_groups = nn.ModuleList()
        channels = [self.out_channels for _ in range(self.num * 2)]
        channels[0] = self.in_channels
        for n in range(self.num):
            layers = nn.Sequential(
                nn.Conv2d(channels[n * 2], channels[n * 2 + 1], kernel_size=3, padding=1),
                nn.BatchNorm2d(channels[n * 2 + 1]),
                nn.ReLU(inplace=True)
            )
            self.layers_groups.append(layers)

    def forward(self, X):
        for layers in self.layers_groups:
            X = layers(X)
        return X

class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 num: int = 2):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num = num
        super(ResidualBlock, self).__init__()
        self.layers_groups = nn.ModuleList()
        self.conv = nn.Conv2d(self.in_channels, self.out_channels, kernel_size=1, padding=0)
        self.RELU = nn.ReLU(inplace=True)
        channels = [self.out_channels for _ in range(self.num * 2)]
        channels[0] = self.in_channels
        for n in range(self.num):
            layers = nn.Sequential(
                nn.Conv2d(channels[n * 2], channels[n * 2 + 1], kernel_size=3, padding=1),
                nn.BatchNorm2d(channels[n * 2 + 1]),
                nn.ReLU(inplace=True),
                nn.Conv2d(channels[n * 2 + 1], channels[n * 2 + 1], kernel_size=3, padding=1),
                nn.BatchNorm2d(channels[n * 2 + 1])
            )
            self.layers_groups.append(layers)

    def forward(self, X):
        for n in range(len(self.layers_groups)):
            if n == 0:
                X = self.RELU(self.layers_groups[n](X) + self.conv(X))
            else:
                X = self.RELU(self.layers_groups[n](X) + X)
        return X

class BottleNeck(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 num: int = 2):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num = num
        super(BottleNeck, self).__init__()
        self.layers_groups = nn.ModuleList()
        self.conv = nn.Conv2d(self.in_channels, self.out_channels, kernel_size=1, padding=0)
        self.RELU = nn.ReLU(inplace=True)
        channels = [self.out_channels for _ in range(self.num * 2)]
        channels[0] = self.in_channels
        for n in range(self.num):
            layers = nn.Sequential(
                nn.Conv2d(channels[n * 2], channels[n * 2 + 1], kernel_size=1, padding=0),
                nn.BatchNorm2d(channels[n * 2 + 1]),
                nn.ReLU(inplace=True),
                nn.Conv2d(channels[n * 2 + 1], channels[n * 2 + 1], kernel_size=3, padding=1),
                nn.BatchNorm2d(channels[n * 2 + 1]),
                nn.ReLU(inplace=True),
                nn.Conv2d(channels[n * 2 + 1], channels[n * 2 + 1], kernel_size=1, padding=0)
            )
            self.layers_groups.append(layers)

    def forward(self, X):
        for n in range(len(self.layers_groups)):
            if n == 0:
                X = self.RELU(self.layers_groups[n](X) + self.conv(X))
            else:
                X = self.RELU(self.layers_groups[n](X) + X)
        return X

class Attention(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int):
        self.in_channels = in_channels
        self.out_channels = out_channels
        super(Attention, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
    
    def forward(self, x):
        y1 = torch.mean(x, dim=1, keepdim=True)
        y2, _ = torch.max(x, 1, keepdim=True)
        x3 = x * y1
        x4 = x * y2
        x = torch.cat((x3, x4), dim=1)
        x = torch.sigmoid(x)
        return x

class DilatedConv(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int):
        self.in_channels = in_channels
        self.out_channels = out_channels
        super(DilatedConv, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.c1 = nn.Sequential(
            nn.Conv2d(self.in_channels, self.out_channels, kernel_size=3, padding=1, dilation=1),
            nn.BatchNorm2d(self.out_channels),
            nn.ReLU()
        )

        self.c2 = nn.Sequential(
            nn.Conv2d(self.in_channels, self.out_channels, kernel_size=3, padding=3, dilation=3),
            nn.BatchNorm2d(self.out_channels),
            nn.ReLU()
        )

        self.c3 = nn.Sequential(
            nn.Conv2d(self.in_channels, self.out_channels, kernel_size=3, padding=6, dilation=6),
            nn.BatchNorm2d(self.out_channels),
            nn.ReLU()
        )

        self.c4 = nn.Sequential(
            nn.Conv2d(self.in_channels, self.out_channels, kernel_size=3, padding=9, dilation=9),
            nn.BatchNorm2d(self.out_channels),
            nn.ReLU()
        )

        self.c5 = nn.Sequential(
            nn.Conv2d(self.out_channels * 4, self.out_channels, kernel_size=1, padding=0),
            nn.BatchNorm2d(self.out_channels),
            nn.ReLU()
        )

    def forward(self, x):
        x1 = self.c1(x)
        x2 = self.c2(x)
        x3 = self.c3(x)
        x4 = self.c4(x)
        x = torch.cat([x1, x2, x3, x4], axis=1)
        x = self.c5(x)
        return x