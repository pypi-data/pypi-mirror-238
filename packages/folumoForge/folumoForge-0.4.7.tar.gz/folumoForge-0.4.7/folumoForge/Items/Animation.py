import numpy as np
import pygame
import imageio
from pygame import Surface

from folumoForge import itemBase, Screen


class Animation(itemBase):
    def __init__(self, screen: Screen, path, isWeb, xy, wh=None):
        super().__init__("Animation")

        self.screen = screen
        screen.Items.append(self)
        self.xy = xy

        if isWeb:
            # For web-based videos
            video_bytes = imageio.get_reader(path, 'ffmpeg')
        else:
            # For local video files
            video_bytes = imageio.get_reader(path)

        self.video = video_bytes.iter_data()

        if wh:
            self.wh = wh

        self.rect = pygame.Rect(0, 0, 0, 0)

    def config(self, path, xy, wh=None):
        # Your configuration logic here
        pass

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))

        if self.Alpha:
            tmp.set_alpha(self.Alpha)

        try:
            video_image = next(self.video)
            video_surf = pygame.surfarray.make_surface(
                np.rot90(video_image, axes=(1, 0)))
            tmp.blit(video_surf, self.xy)
        except StopIteration:
            # Handle end of video
            pass

        self.rect = self.screen.root.MainRoot.blit(tmp, self.xy)
