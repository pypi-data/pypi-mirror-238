import pygame
from pygame import Surface

from .. import itemBase, Screen


class Image(itemBase):
    def __init__(self, screen: Screen, path, xy, wh=None):
        super().__init__("Image")
        self.screen = screen
        screen.Items.append(self)
        self.xy = xy

        self.img = pygame.image.load(path)
        if wh:
            self.wh = wh
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def config(self, path, xy, wh=None):
        self.xy = xy

        self.img = pygame.image.load(path)
        if wh:
            self.wh = wh
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))

        if self.Alpha:
            tmp.set_alpha(self.Alpha)

        tmp.blit(self.img, (0, 0))
        self.rect = self.screen.root.MainRoot.blit(tmp, self.xy)
