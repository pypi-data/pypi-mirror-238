# Import required libraries
import re
from torch.utils.data import DataLoader, Dataset
import json
from PIL import Image
from torchvision import transforms
from icecream import ic
import torch
import random
import cv2
from ..utils import IMAGE_NORMALIZATION_MEAN, IMAGE_NORMALIZATION_STD, resize_image

TARGET_IMG_SIZE = 512


class TrainTransforms:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.RandomResizedCrop(TARGET_IMG_SIZE, (0.8,1)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(30),
            transforms.ColorJitter(brightness=0.5, contrast=0.5),
            transforms.GaussianBlur(3, sigma=(0.1, 2.0)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGE_NORMALIZATION_MEAN, std=IMAGE_NORMALIZATION_STD)
        ])

    def __call__(self, img):
        return self.transform(img)

class ValTransforms:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGE_NORMALIZATION_MEAN, std=IMAGE_NORMALIZATION_STD)
        ])

    def __call__(self, img):
        return self.transform(img)

class LegacyImageDataset(Dataset):
    def __init__(self, img_dicts, transform = None, debug = False, labels = None):
        # Implement code to read the JSONL file and store the image paths and labels in self.image_paths and self.labels
        self.transform = transform

        assert labels is not None, "labels must be provided"

        self.image_paths = []
        self.labels = []
        self.unique_labels = labels
        for img_dict in img_dicts:
            self.image_paths.append(img_dict["path"])
            self.labels.append(img_dict["labels"])

        self.label_to_idx = {
            label: idx for idx, label in enumerate(self.unique_labels)
        }

        # if debug is true, only use the first 100 images
        if debug:
            self.image_paths = self.image_paths[:100]
            self.labels = self.labels[:100]
        

    def __len__(self):
        return len(self.image_paths)

    def read_image(self, image_path):
        # read image using cv2
        img = Image.open(image_path)
        img = self.resize_image(img)
        return img
    
    def resize_image(self, image:Image.Image, init_height=1080, target_height=TARGET_IMG_SIZE):
        resized_image = resize_image(image, init_height, target_height)

        return resized_image

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        image = self.read_image(path)
        label = self.labels[idx]

        if self.transform:
            image_tensor = self.transform(image)

        # Implement code to convert the labels to a one-hot encoded vector            
        label = torch.tensor(label, dtype=torch.float32)

        return image_tensor, label
