from io import BytesIO

import numpy as np
import pygame
import requests
from pygame import Surface

from folumoForge import itemBase, Forge, Screen
import cv2


class Animation(itemBase):
    def __init__(self, screen: Screen, path, isWeb, xy, wh=None):
        super().__init__("Animation")

        self.screen = screen
        screen.Items.append(self)
        self.xy = xy

        if isWeb:
            response = requests.get(path)
            video_bytes = BytesIO(response.content)

            self.video = cv2.VideoCapture(video_bytes)
        else:
            self.video = cv2.VideoCapture(path)

        if wh:
            self.wh = wh

        self.rect = pygame.Rect(0, 0, 0, 0)

    def config(self, path, xy, wh=None):
        ...

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))

        if self.Alpha:
            tmp.set_alpha(self.Alpha)

        success, video_image = self.video.read()
        if success:
            video_surf = pygame.surfarray.make_surface(
                np.rot90(cv2.cvtColor(video_image, cv2.COLOR_BGR2RGB)))
            tmp.blit(video_surf, self.xy)

        self.rect = self.screen.root.MainRoot.blit(tmp, self.xy)
