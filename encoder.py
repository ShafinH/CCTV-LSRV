#!/usr/bin/env python3

import pytorch_lightning as pl
import hydra
from omegaconf import DictConfig
import cctv_learning
from cctv_learning.models.conv_autoencoder import Autoencoder
from cctv_learning.datasets.cctv import CCTV
from torch.utils.data import DataLoader
import umap
import imageio
import math
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import random
import pylab


@cctv_learning.register_experiment
def cctv(cfg):

    allVideos()
    singleVideo()
    singleCamera()


def allVideos():
    # path to video
    vid_path = r"D:/Github Repos/CCTV-Accidents/scraped_data/Maryland/Frederick_Rd_(MD_355)_at_Germantown_Rd_(MD_118)(CAM_118)/10-03-21_16-34-37.mp4"
    video = imageio.get_reader(vid_path, 'ffmpeg')
    # path to checkpoint
    model = Autoencoder.load_from_checkpoint(
        checkpoint_path="D:\Github Repos\\cctv-learning\\results\cctv\\2021-11-18\\23-55-24\lightning_logs\\version_0\checkpoints\\epoch=24-step=134899.ckpt")

    reducer = umap.UMAP()

    encodings = []
    tensors = []
    distance = []
    order = []

    n = 5000

    averageX = 0
    averageY = 0

    for i in range(n):
        num = i * random.randint(1, 10)
        order.append(num)
        frame = video.get_data(num)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        tensors.append(frame)

    for tensor in tensors:
        encoding = model.encoder(tensor[None, ...]).size()
        encodings.append(encoding)

    embedding = reducer.fit_transform(encodings)

    for e in embedding:
        averageX += e[0]
        averageY += e[1]

    averageX /= len(embedding)
    averageY /= len(embedding)

    for e in embedding:
        distance.append([
            math.sqrt((averageX - e[0]) ** 2 + (averageY - e[1]) ** 2),
            e[0],
            e[1]]
        )

    for i in range(n):
        distance[i].append(order[i])

    distance = sorted(distance)

    for i in range(10):
        image = video.get_data(distance[-i][3])
        fig = pylab.figure()
        pylab.imshow(image)

    pylab.show()

    plt.scatter(embedding[:, 0], embedding[:, 1],)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title('UMAP projection of US_50_AT_EX_16_MD_424_', fontsize=10)
    plt.show()


def singleVideo():
    # path to video
    vid_path = r"D:/Github Repos/CCTV-Accidents/scraped_data/Maryland/I-83_North_past_Padonia_Rd/10-03-21_16-34-47.mp4"
    video = imageio.get_reader(vid_path, 'ffmpeg')
    # path to checkpoint
    model_all_vids = Autoencoder.load_from_checkpoint(
        checkpoint_path="D:\Github Repos\\cctv-learning\\results\cctv\\2021-11-21\\21-56-13\lightning_logs\\version_0\checkpoints\\epoch=4-step=92749.ckpt")
    reducer = umap.UMAP()

    encodings = []
    tensors = []
    distance = []
    order = []

    n = 5000

    averageX = 0
    averageY = 0

    for i in range(n):
        num = i * random.randint(1, 10)
        order.append(num)
        frame = video.get_data(num)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        tensors.append(frame)

    for tensor in tensors:
        encoding = model_all_vids.encoder(tensor[None, ...]).size()
        encodings.append(encoding)

    embedding = reducer.fit_transform(encodings)

    for e in embedding:
        averageX += e[0]
        averageY += e[1]

    averageX /= len(embedding)
    averageY /= len(embedding)

    for e in embedding:
        distance.append([
            math.sqrt((averageX - e[0]) ** 2 + (averageY - e[1]) ** 2),
            e[0],
            e[1]]
        )

    for i in range(n):
        distance[i].append(order[i])

    distance = sorted(distance)

    for i in range(10):
        image = video.get_data(distance[-i][3])
        fig = pylab.figure()
        pylab.imshow(image)

    pylab.show()

    plt.scatter(embedding[:, 0], embedding[:, 1],)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(r'UMAP projection of I-83_North_past_Padonia_Rd', fontsize=10)
    plt.show()


def singleCamera():
    # path to camera
    vid_path = "D:\Github Repos\CCTV-Accidents\scraped_data\Maryland\Connecticut_Ave_(MD_185)_at_East_West_Hwy_(MD_410)(CAM_15)\\01-08-22_12-57-23.mp4"
    video = imageio.get_reader(vid_path, 'ffmpeg')
    # path to checkpoint
    model_all_vids = Autoencoder.load_from_checkpoint(
        checkpoint_path="D:\Github Repos\cctv-learning\\results\cctv\\2022-01-08\\12-46-38\lightning_logs\\version_0\checkpoints\\singlecamera.ckpt")
    reducer = umap.UMAP()

    encodings = []
    tensors = []
    distance = []
    order = []

    n = 5000

    averageX = 0
    averageY = 0

    for i in range(n):
        num = i * random.randint(1, 10)
        order.append(num)
        frame = video.get_data(num)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        tensors.append(frame)

    for tensor in tensors:
        encoding = model_all_vids.encoder(tensor[None, ...]).size()
        encodings.append(encoding)

    embedding = reducer.fit_transform(encodings)

    for e in embedding:
        averageX += e[0]
        averageY += e[1]

    averageX /= len(embedding)
    averageY /= len(embedding)

    for e in embedding:
        distance.append([
            math.sqrt((averageX - e[0]) ** 2 + (averageY - e[1]) ** 2),
            e[0],
            e[1]]
        )

    for i in range(n):
        distance[i].append(order[i])

    distance = sorted(distance)

    for i in range(7):
        image = video.get_data(distance[-i][3])
        print(distance[-i][1], distance[-i][2])
        fig = pylab.figure()
        pylab.imshow(image)

    pylab.show()

    plt.scatter(embedding[:, 0], embedding[:, 1],)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(r'UMAP projection of Connecticut Ave', fontsize=10)
    plt.show()


@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    cctv_learning.run(cfg)


if __name__ == "__main__":
    main()
