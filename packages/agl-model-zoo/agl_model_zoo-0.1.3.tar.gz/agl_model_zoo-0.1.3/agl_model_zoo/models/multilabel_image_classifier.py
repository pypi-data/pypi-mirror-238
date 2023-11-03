# Import required libraries
import pytorch_lightning as pl
import torch
from torch import nn
from torch.nn import functional as F
from torchvision import models
from icecream import ic
from torch.optim.lr_scheduler import StepLR
import random
import os
from PIL import Image
import pandas as pd
import cv2
from ..utils import IMAGE_NORMALIZATION_MEAN, IMAGE_NORMALIZATION_STD, LABELS
import numpy as np

# labels are: "appendix", "ileocecal_valve", "polyp", "water_jet", "digital_chromo_endoscopy", "instrument", "wound", "blood", "ileum", "low_quality", "clip", "outside"


class MultilabelImageClassifier(pl.LightningModule):
    def __init__(self, labels = LABELS, train_all_layers=False):
        super(MultilabelImageClassifier, self).__init__()

        self.labels = labels
        num_classes = len(labels)
        
        # Load a pre-trained ResNet model
        # self.model = models.resnet18(weights="DEFAULT")
        self.model = models.regnet_x_400mf(weights="DEFAULT")
        
        # If you want to freeze the layers of the pre-trained model
        if not train_all_layers:
            for param in self.model.parameters():
                param.requires_grad = False
        
        # Replace the classifier part of the ResNet model
        # Assuming that the feature extractor produces 512 features and we are dealing with CIFAR-10 dataset with 10 classes
        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes),
            nn.Sigmoid()
        )
        
        self.num_classes = num_classes
        self.training_step_outputs = []
        self.validation_step_outputs = []

    def label_to_idx(self, label):
        return self.labels.index(label)
    
    def idx_to_label(self, idx):
        return self.labels[idx]
        
    def forward(self, x):
        # Forward pass
        x = self.model(x)
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.binary_cross_entropy(y_hat, y)
        self.log('train_loss', loss, on_step=True, on_epoch=True)
        return loss

    def on_validation_epoch_start(self):
        self.validation_samples = []

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.binary_cross_entropy(y_hat, y)
        self.log('val_loss', loss, on_step=False, on_epoch=True)
        y_hat = y_hat > 0.5
        correct = (y_hat == y).sum().item()
        total = y.numel()
        self.log('val_acc', correct / total, on_step=False, on_epoch=True)
        if len(self.validation_samples) < 20:
            self.validation_samples.append((x.cpu().detach(), y, y_hat))
        return loss
    
    def on_validation_epoch_end(self):
        # Randomly select 10 samples and save them
        selected_samples = random.sample(self.validation_samples, min(10, len(self.validation_samples)))
        for i, (x, y, y_hat) in enumerate(selected_samples):
            self.save_random_images(x, y, y_hat, "val", i, self.current_epoch)
        
        # free up memory
        self.validation_samples = []


    def save_random_images(self, x, y, y_hat, step_type, index, epoch):
        # Create a directory for each epoch
        epoch_dir = f"epoch_{epoch}"
        dir_path = os.path.join(step_type + "_images", epoch_dir)
        os.makedirs(dir_path, exist_ok=True)
        
        img_path = os.path.join(dir_path, f"{index}.png")
        img = x[0]

        # Reverse normalization
        # Assuming mean and std are the values used for the original normalization
        mean = np.array(IMAGE_NORMALIZATION_MEAN)
        std = np.array(IMAGE_NORMALIZATION_STD)
        img = ((img.permute(1, 2, 0).numpy() * std + mean) * 255).astype(np.uint8)

        img_path = os.path.join(dir_path, f"{index}.png")

        # Save the image
        cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))  # Convert from RGB to BGR format for OpenCV

        csv_path = os.path.join(dir_path, "image_data.csv")
        df = pd.DataFrame({
            "path": [img_path], 
            "label": [y[0].cpu().numpy().tolist()],
            "prediction": [y_hat[0].cpu().detach().numpy().tolist()]
        })
        
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        scheduler = StepLR(optimizer, step_size=30, gamma=0.1)
        return [optimizer], [scheduler]


