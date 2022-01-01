#!/usr/bin/env python3
# 30.4 GB
import os
import cv2
import imageio


class Preprocessing:
    def __init__(self, path="D:/Github Repos/CCTV-Accidents/scraped_data/Maryland"):
        self.path = path
        self.count = 0
        self.mp4_dirs = []
        self.mp4s = []
        self.good_mp4s = []
        self.bad_mp4s = []
        
        for file in os.listdir(self.path):
            d = os.path.join(self.path, file)
            if os.path.isdir(d):
                self.mp4_dirs.append(d)

        for dir in self.mp4_dirs:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    if file.endswith('.mp4'):
                        self.mp4s.append(os.path.join(root, file))

        self.mp4s = sorted(self.mp4s)
        self.num_of_mp4 = len(self.mp4s)

    def find(self):
        for mp4 in self.mp4s:
            keep_mp4 = False
            video = imageio.get_reader(mp4, 'ffmpeg')
            frame = video.get_data(15)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    pixel = frame[i][j]
                    if pixel > 10:
                        keep_mp4 = True
                        break
                if keep_mp4:
                    self.good_mp4s.append(mp4)
                    break
        
    def remove(self):
        self.bad_mp4s = [x for x in p.mp4s if x not in p.good_mp4s]
        for mp4 in self.bad_mp4s:
            os.remove(mp4)
            json = mp4.replace('.mp4', '.JSON')
            os.remove(json)

if __name__ == "__main__":
    p = Preprocessing()
    p.find()
    p.remove()
