#!/usr/bin/env python3

import pytorch_lightning as pl
import hydra
from omegaconf import DictConfig
import cctv_learning
from cctv_learning.models.conv_autoencoder import Autoencoder
from cctv_learning.datasets.cctv import CCTV, CCTVOneVideo
from torch.utils.data import DataLoader


@cctv_learning.register_experiment
def cctv(cfg):
    pl.seed_everything(cfg.seed)

    train_loader = DataLoader(CCTV())
    trainer = pl.Trainer(max_epochs=25, devices=1, accelerator="gpu")
    model = Autoencoder()

    trainer.fit(model, train_loader)


@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    cctv_learning.run(cfg)


if __name__ == "__main__":
    main()
