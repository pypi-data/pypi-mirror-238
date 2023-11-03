# EasyMed

EasyMed is a one-stop medical Python advanced package based on the PyTorch framework. It allows you to easily and conveniently create some commonly used models by simply editing parameters. In the initial version, you can create UNet models and variants suitable for image segmentation tasks.

## Features

- Fast UNet model creation
- Customizable encoder blocks
- Selectable bridge
- Flexible and adjustable number of channels

## Installation

You can install EasyMed using pip:

```bash
pip install easymed
```

# Quick Start

```bash
from torch.utils import data
from easymed.CV.utils import ImageDataset
from easymed.CV.model.unet import UNet_2plus

# Here we use the default parameters
# in_channels=1 out_channels=1 mid_channels=[32, 64, 128, 256]
# encoder=double_conv  bridge =DilatedConv

net = UNet_2plus()

train_data = ImageDataset({your_path})

# Here we use the default parameters
# batch_size=4  shuffle=True
train_iter = data.DataLoader(train_data, batch_size=4, shuffle=True)

# Here we use the default parameters
#loss=nn.BCEWithLogitsLoss()  optimizer=torch.optim.SGD  epochs=40  lr=0.0001
net.train_net(train_iter=train_iter)
```

# Parameter Description
Here are the parameters you can customize when creating a UNet model using MyPyTorchUNet:

- in_channels: Input the number of input channels.

- outchannels: Input the number of output channels.

- mid_channels：Input the number of feature channels of the hidden layers as a list.

- encoder:    Different kinds of blocks such as sigle_VGG,double_VGG,triple_VGG,sigle_Residual,double_Resudual, triple_Residual are provided to build the encoder.

- bridge:  DilatedConv,APSS,bridges from sota models in many well-known public datasets.

- decoder:    Different kinds of blocks such as sigle_VGG,double_VGG,triple_VGG,sigle_Residual,double_Resudual, triple_Residual are provided to build the decoder.

- ...







# Contributions
If you are interested in contributing to MyPyTorchUNet by adding code or suggesting improvements, please feel free to submit issues or pull requests.

