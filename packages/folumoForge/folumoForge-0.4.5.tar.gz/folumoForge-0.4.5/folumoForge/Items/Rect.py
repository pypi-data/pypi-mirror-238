from OpenGL.GL import *

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

        self.vertices = [
            (xy[0], xy[1]),
            (xy[0] + wh[0], xy[1]),
            (xy[0] + wh[0], xy[1] + wh[1]),
            (xy[0], xy[1] + wh[1])
        ]

    def config(self, xy=None, wh=None, color=None, opacity=None):
        if color:
            self.color = color

        if opacity:
            self.Alpha = opacity
        if xy:
            self.xy = xy
            self.vertices = [
                (xy[0], xy[1]),
                (xy[0] + self.wh[0], xy[1]),
                (xy[0] + self.wh[0], xy[1] + self.wh[1]),
                (xy[0], xy[1] + self.wh[1])
            ]
        if wh:
            self.wh = wh
            self.vertices = [
                (self.xy[0], self.xy[1]),
                (self.xy[0] + wh[0], self.xy[1]),
                (self.xy[0] + wh[0], self.xy[1] + wh[1]),
                (self.xy[0], self.xy[1] + wh[1])
            ]

    def update(self):
        glBegin(GL_QUADS)
        if self.Alpha:
            glColor4f(*self.color, self.Alpha)
        else:
            glColor3fv(self.color)

        for vertex in self.vertices:
            glVertex2fv(vertex)

        glEnd()
