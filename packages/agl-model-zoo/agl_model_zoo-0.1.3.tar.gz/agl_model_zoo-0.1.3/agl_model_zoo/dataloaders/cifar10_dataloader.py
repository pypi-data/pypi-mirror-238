from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import torch
import numpy as np

class OneHotCIFAR10(datasets.CIFAR10):
    def __init__(self, *args, **kwargs):
        super(OneHotCIFAR10, self).__init__(*args, **kwargs)

    def __getitem__(self, index):
        img, target = super(OneHotCIFAR10, self).__getitem__(index)
        
        # One-hot encode the target label
        one_hot_target = np.zeros(10, dtype=np.float32)
        one_hot_target[target] = 1.0
        
        return img, torch.tensor(one_hot_target)

# Data Augmentation for the training set
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Normalization for the validation set
val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

trainset = OneHotCIFAR10(root='./data', train=True, download=True, transform=train_transforms)
trainloader = DataLoader(trainset, batch_size=32, shuffle=True)

testset = OneHotCIFAR10(root='./data', train=False, download=True, transform=val_transforms)
testloader = DataLoader(testset, batch_size=32, shuffle=False)