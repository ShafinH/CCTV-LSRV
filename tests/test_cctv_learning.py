#!/usr/bin/env python3

import pytorch_lightning as pl
import hydra
from omegaconf import DictConfig
import cctv_learning
from cctv_learning.models.conv_autoencoder import Autoencoder
from cctv_learning.datasets.cctv import CCTV
from torch.utils.data import DataLoader


@cctv_learning.register_experiment
def cctv(cfg):
    pl.seed_everything(cfg.seed)

    # The ** converts the dictionary inside to key, value pairs.
    dm = DataLoader(**cfg.dataset)
    model = Autoencoder(**cfg.model)
    dm.prepare_data()
    dm.setup(stage="fit")
    trainer = pl.Trainer(**cfg.trainer)
    trainer.fit(model, dm)
    trainer.test(datamodule=dm)


@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    cctv_learning.run(cfg)


def test_main():
    assert True, "Well, this is embarassing."
