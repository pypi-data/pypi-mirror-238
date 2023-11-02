from OpenGL.GL import *
from PIL import Image as Img

from .. import itemBase, Screen


class Image(itemBase):
    def __init__(self, screen: Screen, path, xy, wh=None):
        super().__init__("Image")
        self.screen = screen
        screen.Items.append(self)
        self.xy = xy
        self.path = path

        img = Img.open(path)
        img_data = list(img.tobytes())

        if wh:
            self.wh = wh
            img = img.resize(wh)
            img_data = list(img.tobytes())

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def config(self, path=None, xy=None, wh=None):
        if xy:
            self.xy = xy

        if path:
            self.path = path

            img = Img.open(path)
            img_data = list(img.tobytes())

            if self.wh:
                img = img.resize(self.wh)
                img_data = list(img.tobytes())

            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        if wh:
            self.wh = wh

    def update(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2fv(self.xy)

        glTexCoord2f(1, 0)
        glVertex2f(self.xy[0] + self.wh[0], self.xy[1])

        glTexCoord2f(1, 1)
        glVertex2fv((self.xy[0] + self.wh[0], self.xy[1] + self.wh[1]))

        glTexCoord2f(0, 1)
        glVertex2fv((self.xy[0], self.xy[1] + self.wh[1]))

        glEnd()
