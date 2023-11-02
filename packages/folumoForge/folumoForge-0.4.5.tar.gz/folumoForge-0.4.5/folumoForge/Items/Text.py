import pygame
from OpenGL.GL import *
from PIL import Image
import freetype

from .. import itemBase, Screen


class Text(itemBase):
    def __init__(self, screen: Screen, font_path="arial.ttf", text="Sample Text.", color=(255, 255, 255), size=12, xy=(0, 0)):
        super().__init__("Text")
        self.screen = screen
        screen.Items.append(self)
        self.xy = xy
        self.font_path = font_path
        self.text = text
        self.color = color
        self.size = size
        self.texture = None
        self.rect = pygame.Rect(xy[0], xy[1], 0, 0)
        self.create_texture()

    def create_texture(self):
        font = freetype.Face(self.font_path)
        font.set_pixel_sizes(0, self.size)

        width, height = 0, 0
        for char in self.text:
            font.load_char(char)
            bitmap = font.glyph.bitmap
            width += bitmap.width
            height = max(height, bitmap.rows)

        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        x = 0
        for char in self.text:
            font.load_char(char, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
            bitmap = font.glyph.bitmap
            image.paste(bitmap.buffer, (x, height - bitmap.rows), bitmap.buffer)
            x += bitmap.width

        img_data = list(image.tobytes())

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def config(self, font_path=None, text=None, color=None, size=None, xy=None):
        if xy:
            self.xy = xy
        if font_path:
            self.font_path = font_path
            self.create_texture()
        if text:
            self.text = text
            self.create_texture()
        if color:
            self.color = color
        if size:
            self.size = size
            self.create_texture()

    def update(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2fv(self.xy)

        glTexCoord2f(1, 0)
        glVertex2f(self.xy[0] + self.rect.width, self.xy[1])

        glTexCoord2f(1, 1)
        glVertex2fv((self.xy[0] + self.rect.width, self.xy[1] + self.rect.height))

        glTexCoord2f(0, 1)
        glVertex2fv((self.xy[0], self.xy[1] + self.rect.height))

        glEnd()
