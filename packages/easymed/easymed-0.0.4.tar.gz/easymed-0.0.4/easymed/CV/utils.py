import os
import torch
from torch import nn
from torch.utils import data
import torchvision.transforms as transforms
from zipfile import ZipFile
import cv2


class ImageDataset(data.Dataset):
    def __init__(self, path: str, color: str = 'gray', mode: str = 'train'):
        self.path = path
        self.color = color
        self.mode = mode
        self.name = os.listdir(self.path + '/image')
        self.transform = transforms.ToTensor()
    
    def __getitem__(self, idx):
        if self.mode == 'train':
            if self.color == 'gray':
                image = cv2.imread(self.path + '/image/' + self.name[idx], cv2.IMREAD_GRAYSCALE)
                mask = cv2.imread(self.path + '/mask/' + self.name[idx], cv2.IMREAD_GRAYSCALE)
            elif self == 'RGB':
                image = cv2.imread(self.path + '/image/' + self.name[idx])
                mask = cv2.imread(self.path + '/mask/' + self.name[idx])
            image = self.transform(image)
            mask = self.transform(mask)
            return image, mask
        elif self.mode == 'test':
            if self.color == 'gray':
                image = cv2.imread(self.path + '/image/' + self.name[idx], cv2.IMREAD_GRAYSCALE)
            elif self == 'RGB':
                image = cv2.imread(self.path + '/image/' + self.name[idx])
            image = self.transform(image)
            return image

    def __len__(self):
        return len(self.name)


def show_img(tensor):
    unloader = transforms.ToPILImage()
    image = tensor.clone()
    image = image.squeeze(0)
    image = unloader(image)
    return image

def show_mask(img, mask, transparency=0.5):
    color = torch.tensor([30/255, 144/255, 255/255]).reshape(-1, 1, 1)
    transform = transforms.ToTensor()
    img = transform(img)
    mask = transform(mask)
    front = img * mask
    back = img - front
    result = back + (mask * color * (1 - transparency) + front * transparency)
    return show_img(result)

