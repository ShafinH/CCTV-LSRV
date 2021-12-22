#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="cctv_learning",
    version="0.1.1",
    description="Code for \"CCTV Camera Latent Representations for Reducing Accident Response Time\"",
    author="Shafin Haque",
    author_email="shafin1025@gmail.com",
    url="https://github.com/ShafinH/cctv-learning",
    install_requires=[
        "torch",
        "torchvision",
        "pytorch-lightning",
        "hydra-core",
        "omegaconf",
        "rich",
        "numpy",
        "opencv-python",
        "imageio",
        "imageio-ffmpeg",
        "torch",
        "seaborn",
        "matplotlib",
    ],
    packages=find_packages(),
)
