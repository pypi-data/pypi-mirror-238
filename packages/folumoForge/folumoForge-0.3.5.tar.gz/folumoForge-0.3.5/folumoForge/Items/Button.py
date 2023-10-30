import pygame

from .. import itemBase


class Button(itemBase):
    def __init__(self, look: itemBase, down=None, up=None, wheel=None, motion=None, hover=None):
        super().__init__("Button")
        self.rect = pygame.Rect((0, 0), (0, 0))

        look.screen.EventAble.append(self)

        self.down = down
        self.up = up
        self.wheel = wheel
        self.motion = motion
        self.hover = hover

        self.look = look

    def config(self, look, down=None, up=None, wheel=None, motion=None, hover=None):
        self.down = down
        self.up = up
        self.wheel = wheel
        self.motion = motion
        self.hover = hover

        self.look = look

    def update(self, event=None):
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN and self.look.rect.collidepoint(event.pos):
                if self.down:
                    self.down(self)

            elif event.type == pygame.MOUSEBUTTONUP and self.look.rect.collidepoint(event.pos):
                if self.up:
                    self.up(self)

            elif event.type == pygame.MOUSEWHEEL and self.look.rect.collidepoint(event.pos):
                if self.wheel:
                    self.wheel(self)

            elif event.type == pygame.MOUSEMOTION:
                if self.look.rect.collidepoint(event.pos):
                    if self.motion:
                        self.motion(self)

                if self.hover:
                    self.hover(self, self.look.rect.collidepoint(event.pos))

        else:
            self.rect = self.look.rect
