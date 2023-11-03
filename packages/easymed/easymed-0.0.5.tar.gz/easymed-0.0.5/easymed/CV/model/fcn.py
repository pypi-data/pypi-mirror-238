import torch
from torch import nn
from tqdm import tqdm
from ..metrics import iou, dice
from ..modules.blocks import *
from ..modules.up import *
from ..modules.down import *
from typing import List, Type
from ..model import binary



__all__ = ['FCN32s', 'FCN16s', 'FCN8s']



class FCN32s(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling):
        super().__init__()
        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.up_bn = nn.ModuleList()
        self.downsamp =  nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.conv = nn.ModuleList()

        self.down_channels = [in_channels] + mid_channels
        self.final_conv = [nn.Conv2d(self.down_channels[-1], 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d(),
                    nn.Conv2d(4096, 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d()]
        self.final_conv = nn.Sequential(*self.final_conv)
 
        for i in range(len(self.down_channels)-1):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.upsamp.append(up(out_channels , out_channels))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.deconv.append(decoder(out_channels , out_channels))#############
        for i in range(len(self.down_channels)-1, 0, -1):
            self.up_bn.append(nn.BatchNorm2d(out_channels))
        for i in range(len(self.down_channels), 1, -1):
            if i==len(self.down_channels):
                self.conv.append(nn.Conv2d(4096, out_channels, kernel_size=1))
                continue
            self.conv.append(nn.Conv2d(self.down_channels[i-1], out_channels, kernel_size=1))

    def forward(self, x):
        y_down = []
        y_up = []
        #encoder
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            x = self.downsamp[i-1](x)
            y_down.append(x)
            print("y_down",end=" ")
            print(i,end=' ')
            print(y_down[i].shape)
        #decoder
        x = self.final_conv(x)
        y_down[-1] = x

        for i in range(len(y_down)):
            y_down[i] = self.conv[len(y_down)-i-1](y_down[i])

        for i in range(len(self.down_channels)-1):
            y_up.append(self.up_bn[i](self.deconv[i](self.upsamp[i](y_up[-1]))))
        return y_up[-1] 
        
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




class FCN16s(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling):
        super().__init__()
        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.up_bn = nn.ModuleList()
        self.downsamp =  nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.conv = nn.ModuleList()

        self.down_channels = [in_channels] + mid_channels
        self.final_conv = [nn.Conv2d(self.down_channels[-1], 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d(),
                    nn.Conv2d(4096, 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d()]
        self.final_conv = nn.Sequential(*self.final_conv)

        for i in range(len(self.down_channels)-1):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.upsamp.append(up(out_channels , out_channels))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.deconv.append(decoder(out_channels , out_channels))#############
        for i in range(len(self.down_channels)-1, 0, -1):
            self.up_bn.append(nn.BatchNorm2d(out_channels))
        for i in range(len(self.down_channels), 1, -1):
            if i==len(self.down_channels):
                self.conv.append(nn.Conv2d(4096, out_channels, kernel_size=1))
                continue
            self.conv.append(nn.Conv2d(self.down_channels[i-1], out_channels, kernel_size=1))

    def forward(self, x):
        y_down = []
        y_up = []
        #encoder
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            x = self.downsamp[i-1](x)
            y_down.append(x)
            print("y_down",end=" ")
            print(i,end=' ')
            print(y_down[i].shape)
        #decoder
        x = self.final_conv(x)
        y_down[-1] = x

        for i in range(len(y_down)):
            y_down[i] = self.conv[len(y_down)-i-1](y_down[i])

        y_up.append(self.up_bn[0](self.deconv[0](self.upsamp[0](y_down[-1]))))
        y_up.append(self.up_bn[1](self.deconv[1](self.upsamp[1](y_up[-1]+y_down[-2]))))
        for i in range(2,len(self.down_channels)-1):
            y_up.append(self.up_bn[i](self.deconv[i](self.upsamp[i](y_up[-1]))))
        return y_up[-1] 
        
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




class FCN8s(nn.Module):
    def __init__(self, in_channels: int=1, 
                 out_channels: int=1, 
                 mid_channels: List[int]=[32, 64, 128, 256], 
                 encoder: Type[nn.Module]=VGGBlock,
                 decoder: Type[nn.Module]=VGGBlock,
                 up: Type[nn.Module]=Bilinear,
                 down: Type[nn.Module]=MaxPooling):
        super().__init__()
        self.enconv = nn.ModuleList()
        self.deconv = nn.ModuleList()
        self.up_bn = nn.ModuleList()
        self.downsamp =  nn.ModuleList()
        self.upsamp = nn.ModuleList()
        self.conv = nn.ModuleList()

        self.down_channels = [in_channels] + mid_channels
        self.final_conv = [nn.Conv2d(self.down_channels[-1], 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d(),
                    nn.Conv2d(4096, 4096, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Dropout2d()]
        self.final_conv = nn.Sequential(*self.final_conv)



        


        for i in range(len(self.down_channels)-1):
            self.enconv.append(encoder(self.down_channels[i], self.down_channels[i+1]))
        for i in range(len(self.down_channels)-2):
            self.downsamp.append(down(self.down_channels[i]))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.upsamp.append(up(out_channels , out_channels))
        for i in range(len(self.down_channels)-1, 0, -1):
            self.deconv.append(decoder(out_channels , out_channels))#############
        for i in range(len(self.down_channels)-1, 0, -1):
            self.up_bn.append(nn.BatchNorm2d(out_channels))
        for i in range(len(self.down_channels), 1, -1):
            if i==len(self.down_channels):
                self.conv.append(nn.Conv2d(4096, out_channels, kernel_size=1))
                continue
            self.conv.append(nn.Conv2d(self.down_channels[i-1], out_channels, kernel_size=1))

    def forward(self, x):
        y_down = []
        y_up = []
        #encoder
        for i in range(len(self.enconv)):
            x = self.enconv[i](x)
            x = self.downsamp[i-1](x)
            y_down.append(x)
            print("y_down",end=" ")
            print(i,end=' ')
            print(y_down[i].shape)
        #decoder
        x = self.final_conv(x)
        y_down[-1] = x

        for i in range(len(y_down)):
            y_down[i] = self.conv[len(y_down)-i-1](y_down[i])

        y_up.append(self.up_bn[0](self.deconv[0](self.upsamp[0](y_down[-1]))))
        y_up.append(self.up_bn[1](self.deconv[1](self.upsamp[1](y_up[-1]+y_down[-2]))))
        y_up.append(self.up_bn[2](self.deconv[2](self.upsamp[2](y_up[-1]+y_down[-3]))))
        for i in range(3,len(self.down_channels)-1):
            y_up.append(self.up_bn[i](self.deconv[i](self.upsamp[i](y_up[-1]))))
        return y_up[-1] 
        
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





