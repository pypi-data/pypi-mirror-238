import pygame
import requests
from io import BytesIO

from pygame import Surface

from .. import itemBase, Screen


class WebImage(itemBase):
    def __init__(self, screen: Screen, url, xy, wh=None):
        super().__init__("WebImage")
        self.screen = screen
        screen.Items.append(self)
        self.xy = xy

        response = requests.get(url)
        image_data = BytesIO(response.content)

        self.img = pygame.image.load(image_data)
        if wh:
            self.wh = wh
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def config(self, url=None, xy=None, wh=None):
        if xy:
            self.xy = xy

        if url:
            response = requests.get(url)
            image_data = BytesIO(response.content)
            self.img = pygame.image.load(image_data)

        if wh:
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))

        if self.Alpha:
            tmp.set_alpha(self.Alpha)

        tmp.blit(self.img, (0, 0))
        self.rect = self.screen.root.MainRoot.blit(tmp, self.xy)
