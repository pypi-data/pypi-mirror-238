import pygame

from .. import itemBase, Screen


class Button(itemBase):
    def __init__(self, screen: Screen, look, down=None, up=None, wheel=None, motion=None):
        super().__init__("Button")
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.screen = screen
        screen.EventAble.append(self)

        self.down = down
        self.up = up
        self.wheel = wheel
        self.motion = motion

        self.look = look

    def config(self, look, down=None, up=None, wheel=None, motion=None):
        self.down = down
        self.up = up
        self.wheel = wheel
        self.motion = motion

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

            elif event.type == pygame.MOUSEMOTION and self.look.rect.collidepoint(event.pos):
                if self.motion:
                    self.motion(self)

        else:
            self.look.update()
            self.rect = self.look.rect
