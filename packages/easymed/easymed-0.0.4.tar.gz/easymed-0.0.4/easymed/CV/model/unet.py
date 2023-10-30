import torch
from torch import nn
from tqdm import tqdm
from ..metrics import iou, dice
from ..modules.blocks import *
from ..modules.up import *
from ..modules.down import *
from typing import List, Type
from ..model import binary


__all__ = ['UNet', 'UNet_plus', 'UNet_2plus']

     
class UNet(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 bottom: Type[nn.Module]=None,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling):
        super().__init__()

        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.downsamp = nn.ModuleList()

        if bottom:
            self.bridge = bottom(mid_channels[-2], mid_channels[-1])
        else:
            self.bridge = encoder(mid_channels[-2], mid_channels[-1])
        self.final = nn.Conv2d(mid_channels[0], out_channels, kernel_size=1)
        self.down_channels = [in_channels] + mid_channels
        for i in range(len(self.down_channels)-2):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        for i in range(len(self.down_channels)-1, 1, -1):
            self.deconv.append(decoder(self.down_channels[i] // 2 + self.down_channels[i-1], self.down_channels[i-1]))
        for i in range(len(self.down_channels)-1, 1, -1):
            self.upsamp.append(up(self.down_channels[i]))
        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))

    def forward(self, x):
        y_down = []
        y_up = []
        #encoder
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            y_down.append(x)
            x = self.downsamp[i](x)
        #bridge
        x = self.bridge(x)
        y_up.append(x)#经过bridge的输出放在y_up的第一位
        #decoder
        for i in range(len(self.deconv)):
            temp = self.deconv[i](torch.cat((y_down[::-1][i], self.upsamp[i](y_up[i])), 1))
            y_up.append(temp)
        return self.final(y_up[-1])
    
    def train_net(self, train_iter, loss=nn.BCEWithLogitsLoss(), optimizer=torch.optim.SGD, num_epochs=40, lr=0.0001, **kwargs):#没有修改过
        updater = optimizer(self.parameters(), lr=lr)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        self.train()
        epochs = range(num_epochs)
        if 'progress' in kwargs:
            epochs = kwargs['progress'].tqdm(epochs)
        for epoch in epochs:
            loop = tqdm(train_iter)
            for X, y in loop:
                X = X.to(device)
                y = y.to(device)
                y_hat = self(X)
                l = loss(y_hat, y)
                updater.zero_grad()
                l.backward()
                updater.step()
                y_hat = binary(y_hat)
                y = binary(y)
                loop.set_description(f'Epoch [{epoch+1}/{num_epochs}]')
                loop.set_postfix(loss=l.mean().item(), dice=dice(y, y_hat).item(), iou=iou(y, y_hat).item())

class UNet_plus(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 bottom: Type[nn.Module]=None,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling,
                 deep_supervision: bool=False):
        super().__init__()

        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.downsamp = nn.ModuleList()
        self.deep_supervision = deep_supervision
        self.out_channels = out_channels
        if bottom:
            self.bridge = bottom(mid_channels[-2], mid_channels[-1])
        else:
            self.bridge = encoder(mid_channels[-2], mid_channels[-1])
        if self.deep_supervision:
            self.final = [nn.Conv2d(mid_channels[0], out_channels, kernel_size=1)] * len(mid_channels)
            self.final = nn.ModuleList(self.final)
        else:
            self.final = nn.Conv2d(mid_channels[0], out_channels, kernel_size=1)
        self.down_channels = [in_channels] + mid_channels

        for i in range(len(self.down_channels)-2):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        
        for i in range(2, len(self.down_channels)):
            layer_deconv = nn.ModuleList()
            for j in range(i, 1, -1):
                layer_deconv.append(decoder(self.down_channels[j]//2+self.down_channels[j-1], self.down_channels[j-1]))
            self.deconv.append(layer_deconv)

        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))
        
        for i in range(2, len(self.down_channels)):
            layer_up = nn.ModuleList()
            for j in range(i, 1, -1):
                layer_up.append(up(self.down_channels[j]))
            self.upsamp.append(layer_up)

    def forward(self, x):
        y = []
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            y.append([x])
            x = self.downsamp[i](x)
        y.append([self.bridge(x)])
        
        for i in range(1, len(self.down_channels)-1):
            for j in range(len(self.down_channels)-i-1):
                temp = self.deconv[j+i-1][i-1](torch.cat((y[j][i-1], self.upsamp[j+i-1][i-1](y[j+1][i-1])), 1))
                y[j].append(temp)

        if self.deep_supervision:
            output = []
            for item, f in zip(y[0], self.final):
                output.append(f(item))
            return output
        else:
            return self.final(y[0][-1])

    def train_net(self, train_iter, loss=nn.BCEWithLogitsLoss(), optimizer=torch.optim.SGD, num_epochs=40, lr=0.0001, **kwargs):
        updater = optimizer(self.parameters(), lr=lr)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        self.train()
        epochs = range(num_epochs)
        if 'progress' in kwargs:
            epochs = kwargs['progress'].tqdm(epochs)
        for epoch in epochs:
            loop = tqdm(train_iter)
            for X, y in loop:
                X = X.to(device)
                y = y.to(device)
                if self.deep_supervision:
                    y_hats = self(X)
                    l = 0
                    for y_hat in y_hats:
                        l += loss(y_hat, y)
                    l /= len(y_hats)
                else:
                    y_hat = self(X)
                    l = loss(y_hat, y)
                updater.zero_grad()
                l.backward()
                updater.step()
                if self.deep_supervision:
                    for i in range(len(y_hats)):
                        y_hats[i] = binary(y_hats[i])
                    y = binary(y)
                    loop.set_postfix(loss=l.mean().item(), dice=[dice(y, y_hat).item() for y_hat in y_hats], iou=[iou(y, y_hat).item() for y_hat in y_hats])
                else:
                    y_hat = binary(y_hat)
                    y = binary(y)
                    loop.set_description(f'Epoch [{epoch+1}/{num_epochs}]')
                    loop.set_postfix(loss=l.mean().item(), dice=dice(y, y_hat).item(), iou=iou(y, y_hat).item())

    def pruning(self, num_mid_channels):
        self.down_channels = self.down_channels[:num_mid_channels+1]
        self.enconv = self.enconv[:num_mid_channels]
        self.deconv = self.deconv[:num_mid_channels]
        self.upsamp = self.upsamp[:num_mid_channels]
        self.downsamp = self.downsamp[:num_mid_channels]
        if self.deep_supervision:
            self.final = self.final[:num_mid_channels]

    def activate_deep_supervision(self):
        self.deep_supervision = True
        self.final = [nn.Conv2d(self.down_channels[1], self.out_channels, kernel_size=1)] * (len(self.down_channels[1])-1)
        self.final = nn.ModuleList(self.final)
    
    def cancel_deep_supervision(self):
        self.deep_supervision = False
        self.final = self.final[-1]


class UNet_2plus(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 bottom: Type[nn.Module]=None,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling,
                 deep_supervision: bool=False):
        super().__init__()

        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.downsamp = nn.ModuleList()
        self.deep_supervision = deep_supervision
        self.out_channels = out_channels
        if bottom:
            self.bridge = bottom(mid_channels[-2], mid_channels[-1])
        else:
            self.bridge = encoder(mid_channels[-2], mid_channels[-1])
        if self.deep_supervision:
            self.final = [nn.Conv2d(mid_channels[0], out_channels, kernel_size=1)] * len(mid_channels)
            self.final = nn.ModuleList(self.final)
        else:
            self.final = nn.Conv2d(mid_channels[0], out_channels, kernel_size=1)
        self.down_channels = [in_channels] + mid_channels

        for i in range(len(self.down_channels)-2):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        
        for i in range(2, len(self.down_channels)):
            layer_deconv = nn.ModuleList()
            for j in range(i, 1, -1):
                layer_deconv.append(decoder(self.down_channels[j]//2+self.down_channels[j-1]*(i+1-j), self.down_channels[j-1]))
            self.deconv.append(layer_deconv)

        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))
        
        for i in range(2, len(self.down_channels)):
            layer_up = nn.ModuleList()
            for j in range(i, 1, -1):
                layer_up.append(up(self.down_channels[j]))
            self.upsamp.append(layer_up)

    def forward(self, x):
        y = []
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            y.append([x])
            x = self.downsamp[i](x)
        y.append([self.bridge(x)])
        
        for i in range(1, len(self.down_channels)-1):
            for j in range(len(self.down_channels)-i-1):
                temp = self.deconv[j+i-1][i-1](torch.cat(y[j][0:i]+[self.upsamp[j+i-1][i-1](y[j+1][i-1])], 1))
                y[j].append(temp)

        if self.deep_supervision:
            output = []
            for item, f in zip(y[0], self.final):
                output.append(f(item))
            return output
        else:
            return self.final(y[0][-1])
    
    def train_net(self, train_iter, loss=nn.BCEWithLogitsLoss(), optimizer=torch.optim.SGD, num_epochs=40, lr=0.0001, **kwargs):
        updater = optimizer(self.parameters(), lr=lr)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        self.train()
        epochs = range(num_epochs)
        if 'progress' in kwargs:
            epochs = kwargs['progress'].tqdm(epochs)
        for epoch in epochs:
            loop = tqdm(train_iter)
            for X, y in loop:
                X = X.to(device)
                y = y.to(device)
                if self.deep_supervision:
                    y_hats = self(X)
                    l = 0
                    for y_hat in y_hats:
                        l += loss(y_hat, y)
                    l /= len(y_hats)
                else:
                    y_hat = self(X)
                    l = loss(y_hat, y)
                updater.zero_grad()
                l.backward()
                updater.step()
                if self.deep_supervision:
                    for i in range(len(y_hats)):
                        y_hats[i] = binary(y_hats[i])
                    y = binary(y)
                    loop.set_postfix(loss=l.mean().item(), dice=[dice(y, y_hat).item() for y_hat in y_hats], iou=[iou(y, y_hat).item() for y_hat in y_hats])
                else:
                    y_hat = binary(y_hat)
                    y = binary(y)
                    loop.set_description(f'Epoch [{epoch+1}/{num_epochs}]')
                    loop.set_postfix(loss=l.mean().item(), dice=dice(y, y_hat).item(), iou=iou(y, y_hat).item())

    def pruning(self, num_mid_channels):
        self.down_channels = self.down_channels[:num_mid_channels+1]
        self.enconv = self.enconv[:num_mid_channels]
        self.deconv = self.deconv[:num_mid_channels]
        self.upsamp = self.upsamp[:num_mid_channels]
        self.downsamp = self.downsamp[:num_mid_channels]
        if self.deep_supervision:
            self.final = self.final[:num_mid_channels]

    def activate_deep_supervision(self):
        self.deep_supervision = True
        self.final = [nn.Conv2d(self.down_channels[1], self.out_channels, kernel_size=1)] * (len(self.down_channels[1])-1)
        self.final = nn.ModuleList(self.final)
    
    def cancel_deep_supervision(self):
        self.deep_supervision = False
        self.final = self.final[-1]