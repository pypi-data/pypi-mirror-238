import pygame
from pygame import Surface

from .. import itemBase, Screen


class Rect(itemBase):
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white", opacity=0):
        super().__init__("Rect")
        self.screen = screen
        screen.Items.append(self)

        self.xy = xy
        self.wh = wh
        self.color = color
        self.Alpha = opacity

        self.rect = pygame.Rect(xy, wh)

    def config(self, xy=None, wh=None, color=None, opacity=None):
        if color:
            self.color = color

        if opacity:
            self.Alpha = opacity
        if xy:
            self.xy = xy
            self.rect = pygame.Rect(xy, self.wh)
        if wh:
            self.wh = wh
            self.rect = pygame.Rect(self.xy, wh)

    def update(self):
        tmp = Surface((self.rect.w, self.rect.h))
        if self.Alpha:
            tmp.set_alpha(self.Alpha)
        pygame.draw.rect(tmp, self.color, pygame.Rect((0, 0), self.wh))
        self.screen.root.MainRoot.blit(tmp, self.xy)
