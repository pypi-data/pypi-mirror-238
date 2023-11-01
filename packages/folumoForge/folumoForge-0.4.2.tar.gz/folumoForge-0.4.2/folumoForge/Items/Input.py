import pygame

from folumoForge import itemBase, Screen


class Input(itemBase):
    def __init__(self, screen: Screen, xy=(0, 0), wh=(200, 50), InputType="text", color="white", textColor="black"):
        super().__init__("Input")
        self.screen = screen
        screen.EventAble.append(self)

        self.xy = xy
        self.wh = wh
        self.color = color
        self.textColor = textColor
        self.IT = InputType
        self.press = False
        self.text = ""

        self.rect = pygame.Rect(xy, wh)

    def config(self, xy=None, wh=None, color=None):
        if color:
            self.color = color

        if xy:
            self.xy = xy
            self.rect = pygame.Rect(xy, self.wh)
        if wh:
            self.wh = wh
            self.rect = pygame.Rect(self.xy, wh)

    def _text(self):
        if self.IT == "text":
            return pygame.font.SysFont("Ariel", self.wh[1]-20, True).render(self.text, False, self.textColor)
        elif self.IT == "password":
            return pygame.font.SysFont("Ariel", self.wh[1]-20, True).render("*"*len(self.text), False, self.textColor)

    def update(self, event=None):
        if event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.press = True
                else:
                    self.press = False

            if self.press:
                if event.type == pygame.KEYDOWN:
                    if event.key == 8:  # back
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
        else:
            tmp = pygame.Surface((self.rect.w, self.rect.h))

            if self.Alpha:
                tmp.set_alpha(self.Alpha)

            pygame.draw.rect(tmp, self.color, pygame.Rect((0, 0), self.wh))

            tmp.blit(self._text(), (10, self.wh[1]/4))

            self.screen.root.MainRoot.blit(tmp, self.xy)
