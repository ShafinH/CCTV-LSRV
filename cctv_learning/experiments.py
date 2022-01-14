#!/usr/bin/env python3

from typing import Callable, Optional
from omegaconf import DictConfig, OmegaConf
import hydra
from hydra.core.hydra_config import HydraConfig
from pathlib import Path
import logging

log = logging.getLogger(__name__)

Experiment = Callable[[DictConfig], None]
_experiment_registry = dict()


def register_experiment(func: Experiment, name: Optional[str] = None):
    _experiment_registry[func.__name__ if name is None else name] = func
    return func


def get_experiment(name: str) -> Experiment:
    if name not in _experiment_registry:
        raise KeyError(f"experiment not registered: {name}")
    return _experiment_registry[name]


def run(cfg: DictConfig) -> None:
    experiment = HydraConfig.get().runtime.choices.experiment
    OmegaConf.resolve(cfg)
    log.info(
        f"running `{experiment}` with config:\n{OmegaConf.to_yaml(cfg.experiment)}"
    )
    get_experiment(experiment)(cfg.experiment)
