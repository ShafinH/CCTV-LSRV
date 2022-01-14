#!/usr/bin/env python3

from typing import Optional
import logging
import pytorch_lightning as pl
from torch.utils.data import random_split, DataLoader
from torchvision.datasets import MNIST
from torchvision import transforms
import os
import cv2
import imageio
import math
import torch

log = logging.getLogger(__name__)

class CCTV(object):
    def __init__(self, frames_per_video=50):
        super().__init__()

        self.mp4_dirs = []
        self.num_of_mp4 = 0
        self.path = "D:/Github Repos/CCTV-Accidents/scraped_data/Maryland"
        self.mp4s = []
        self.jsons = []
        self.frames_per_video = frames_per_video

        for file in os.listdir(self.path):
            d = os.path.join(self.path, file)
            if os.path.isdir(d):
                self.mp4_dirs.append(d)

        for dir in self.mp4_dirs:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    if file.endswith('.mp4'):
                        self.mp4s.append(os.path.join(root, file))
                    if file.endswith('.JSON'):
                        self.jsons.append(os.path.join(root, file))

        self.mp4s = sorted(self.mp4s)
        self.jsons = sorted(self.jsons)

        self.num_of_mp4 = len(self.mp4s)

    def __getitem__(self, index):
        video_index = index // self.frames_per_video
        frame_index = index % self.frames_per_video

        video = imageio.get_reader(self.mp4s[video_index], 'ffmpeg')

        meta = video.get_meta_data()
        n = meta['nframes']
        if math.isinf(n):
            n = int(meta['fps'] * meta['duration'])

        spacing = n // self.frames_per_video

        frame = video.get_data(spacing * frame_index)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
        frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2RGB)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        return frame

    def __len__(self):

        return self.num_of_mp4 * self.frames_per_video


class CCTVOneCamera(object):
    def __init__(self, camera_path="D:\Github Repos\CCTV-Accidents\scraped_data\Maryland\Connecticut_Ave_(MD_185)_at_East_West_Hwy_(MD_410)(CAM_15)", frames_per_video=200):
        super().__init__()

        self.num_of_mp4 = 0
        self.path = camera_path
        self.mp4s = []
        self.jsons = []
        self.frames_per_video = frames_per_video

        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.mp4'):
                    self.mp4s.append(os.path.join(root, file))
                if file.endswith('.JSON'):
                    self.jsons.append(os.path.join(root, file))

        self.mp4s = sorted(self.mp4s)
        self.jsons = sorted(self.jsons)

        self.num_of_mp4 = len(self.mp4s)

    def __getitem__(self, index):
        video_index = index // self.frames_per_video
        frame_index = index % self.frames_per_video

        video = imageio.get_reader(self.mp4s[video_index], 'ffmpeg')

        meta = video.get_meta_data()
        n = meta['nframes']
        if math.isinf(n):
            n = int(meta['fps'] * meta['duration'])

        spacing = n // self.frames_per_video

        frame = video.get_data(spacing * frame_index)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
        frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2RGB)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        return frame

    def __len__(self):

        return self.num_of_mp4 * self.frames_per_video


class CCTVOneVideo(object):
    def __init__(self, vid_path="D:/Github Repos/CCTV-Accidents/scraped_data/Maryland\Columbia_Pk_(US_29)_at_Fairland_Rd_(CAM_130)\\09-10-21_19-34-39.mp4"):
        super().__init__()

        self.vid_path = vid_path

    def __getitem__(self, idx):

        video = imageio.get_reader(self.vid_path, 'ffmpeg')
        frame = video.get_data(idx * 10)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
        frame[:, :, 0] = cv2.equalizeHist(frame[:, :, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_YCrCb2RGB)
        frame = torch.tensor(frame)
        frame = frame.permute(2, 0, 1)
        frame = frame.to(torch.float32) / 255

        return frame

    def __len__(self):

        meta = imageio.get_reader(self.vid_path, 'ffmpeg').get_meta_data()
        n = meta['nframes']

        if math.isinf(n):
            n = int(meta['fps'] * meta['duration'])

        return int(n / 10)
