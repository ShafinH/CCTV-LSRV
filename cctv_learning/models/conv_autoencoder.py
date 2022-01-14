#!/usr/bin/env python3

import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image
import pytorch_lightning as pl
import os
import torch.nn.functional as F


class Autoencoder(pl.LightningModule):
    def __init__(self, hidden_dim=128, learning_rate=0.001):
        super(Autoencoder, self).__init__()
        self.save_hyperparameters()
        self.loss = nn.MSELoss()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=3, padding=1),  # b, 16, 10, 10
            nn.ReLU(True),
            nn.MaxPool2d(2, stride=2),  # b, 16, 5, 5
            nn.Conv2d(16, 8, 3, stride=2, padding=1),  # b, 8, 3, 3
            nn.ReLU(True),
            nn.MaxPool2d(2, stride=1)  # b, 8, 2, 2
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(8, 16, 3, stride=2),  # b, 16, 5, 5
            nn.ReLU(True),
            nn.ConvTranspose2d(16, 8, 5, stride=3, padding=1),  # b, 8, 15, 15
            nn.ReLU(True),
            nn.ConvTranspose2d(8, 3, 2, stride=2, padding=1),  # b, 1, 28, 28
        )

    def forward(self, x):
        x = F.interpolate(x, size=220)
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def training_step(self, batch, batch_idx):
        x = batch
        x = F.interpolate(x, size=220)
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        return loss

    def validation_step(self, batch, batch_idx):
        x = batch
        x = F.interpolate(x, size=220)
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        self.log("valid_loss", loss)

    def test_step(self, batch, batch_idx):
        x = batch
        x = F.interpolate(x, size=220)
        x_hat = self(x)
        loss = self.loss(x_hat, x)
        self.log("test_loss", loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
