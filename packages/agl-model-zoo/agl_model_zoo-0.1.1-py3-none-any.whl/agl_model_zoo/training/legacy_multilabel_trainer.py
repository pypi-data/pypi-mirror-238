from pytorch_lightning import Trainer
import torch
from agl_model_zoo.models.multilabel_image_classifier import MultilabelImageClassifier
from icecream import ic
from pytorch_lightning.callbacks import EarlyStopping
import json
import random
from agl_model_zoo.dataloaders.image_dataloader import LegacyImageDataset, TrainTransforms, ValTransforms
from torch.utils.data import DataLoader
import argparse
from pathlib import Path

def get_datasets(
    data_dir: str,
    test_train_split: float = 0.8,
    batch_size: int = 32,
    num_workers: int = 0,
    seed: int = 42,
    debug: bool = False,
):
    ds_json_path = Path(data_dir) / "legacy_dataset.jsonl"
    ds_info_json_path = Path(data_dir) / "legacy_dataset_info.json"

    with open(ds_info_json_path, "r") as f:
        info = json.load(f)

    labels = info["labels"]

    dataset_dicts = []
    with open(ds_json_path, "r") as f:
        for line in f:
            dataset_dicts.append(json.loads(line))

    # shuffle the dataset in a reproducible manner so that the train and validation sets are different
    random.seed(seed)
    random.shuffle(dataset_dicts)

    train_dicts = dataset_dicts[:int(test_train_split * len(dataset_dicts))]
    test_dicts = dataset_dicts[int(test_train_split * len(dataset_dicts)):]

    train_transforms = TrainTransforms()
    val_transforms = ValTransforms()

    trainset = LegacyImageDataset(train_dicts, transform=train_transforms, debug=debug, labels = labels)
    trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)

    testset = LegacyImageDataset(test_dicts, transform=val_transforms, debug = debug, labels = labels)
    testloader = DataLoader(testset, batch_size=batch_size, shuffle=False)

    return trainloader, testloader, labels


def get_model(labels):
    model = MultilabelImageClassifier(
        labels=labels,
        train_all_layers=True
    )
    return model

def get_train_callbacks():
    # Initialize the EarlyStopping callback
    early_stopping = EarlyStopping(
        monitor='val_loss',   # Monitor validation loss
        patience=3,           # Number of epochs with no improvement after which training will be stopped
        verbose=True,         # Print logging information
        mode='min'            # Stop training when the monitored metric (validation loss) has stopped decreasing
    )

    callbacks = []
    callbacks.append(early_stopping)

    return callbacks


# sample_batch = next(iter(trainloader))
# x_sample, y_sample = sample_batch

# trainer = Trainer(max_epochs=50, callbacks=[early_stopping])
# trainer.fit(model, trainloader, testloader)

# torch.save(model.state_dict(), 'weights/legacy_multilabel_classifier.pth')
