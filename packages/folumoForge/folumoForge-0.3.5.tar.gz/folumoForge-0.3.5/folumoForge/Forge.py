from os import environ

from pygame import Surface
from pygame.event import Event
from threading import Thread
from StorageAllocator import Allocator

if "PYGAME_HIDE_SUPPORT_PROMPT" in environ:
    import pygame
else:
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame

del environ


class Screen:
    def __init__(self, root, name, size, title, fullScreen, monitorNum):
        self.title = title
        self.press = {}
        self.fullScreen = fullScreen
        self.root: Forge = root
        self.name = name
        self.size = size
        self.EventAble = []
        self.Items = []
        self.OnF = {}
        self.monitorNum = monitorNum

    def SwitchScreen(self):
        if self.fullScreen:
            self.root.MainRoot = pygame.display.set_mode(self.size, pygame.FULLSCREEN, 0, self.monitorNum)
        else:
            self.root.MainRoot = pygame.display.set_mode(self.size, display=self.monitorNum)

        pygame.display.set_caption(self.title)

        self.root.Screen = self.name

    def BindKey(self, unicodeID, func):
        self.press[unicodeID] = func

    def DeleteScreen(self):
        del self.root.Screens[self.name]

    def OnFrame(self, _id, func):
        self.OnF[_id] = func

    def render(self, event=None):
        if event:
            if event.type == pygame.QUIT:
                self.root.Running = False

            elif event.type == pygame.KEYUP:
                unicodeID = event.key
                for code in self.press:
                    if unicodeID == code:
                        self.press[code](self, event)

            for item in self.EventAble:
                item.update(event)
        else:
            for fr in self.OnF:
                self.OnF[fr]()

            for item in self.Items:
                item.update()

            for item in self.EventAble:
                item.update()


class Forge:
    def __init__(self, title, wh, icon=None, defaultScreen="start", fullScreen=False, monitor=0):
        pygame.init()
        pygame.font.init()

        self.var = {"mods": {}, "allocator": Allocator(0)}

        self.Screens = {}
        self.Running = True
        self.modThreads = {}

        self.EventRunF = []

        self.NewEventList: list[Event] = []
        self.InEvent = False

        self.delta_time = 0

        self.wh = wh
        self.MainRoot = Surface((0, 0))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)

        self.display_number = monitor

        self.Screens[defaultScreen] = Screen(self, defaultScreen, wh, title, fullScreen, self.display_number)

        self.Screen = defaultScreen

        self.Screens[self.Screen].SwitchScreen()

        if icon:
            if type(icon) == str:
                pygame.display.set_icon(pygame.image.load(icon))
            elif isinstance(icon, itemBase):
                if icon.type in ["WebImage", "Image"]:
                    pygame.display.set_icon(icon.img)

    def addOnEvent(self, func):
        self.EventRunF.append(func)

    def GetScreen(self, name):
        return self.Screens.get(name)

    def NewScreen(self, screen):
        self.Screens[screen.name] = screen

    def Run(self):
        while True:
            try:
                self._run()
                break
            except RuntimeError:
                pass

    def _run(self):
        while self.Running:
            self.delta_time = self.clock.tick(60)
            self.MainRoot.fill((0, 0, 0))
            self.Screens[self.Screen].render()

            for event in pygame.event.get():
                for onEvent in self.EventRunF:
                    onEvent(self, event)
                self.Screens[self.Screen].render(event)

            pygame.display.update()

        pygame.quit()
        pygame.font.quit()


class modBase:
    def __init__(self, root: Forge, name, threadFunc):
        self.name = name
        if name not in root.modThreads:
            t = Thread(target=threadFunc)
            t.start()
            root.modThreads[name] = t

    def preRender(self, data):
        ...

    def postRender(self, data):
        ...

    def Fail(self, data, error):
        print(f"[ERROR-{self.name}]  : This item has failed to finish loading due to {error}; data PKG: {data}")

    def Success(self, data):
        print(f"[INFO-{self.name}]   : This item has successfully finished loading; data PKG: {data}")


class itemBase:
    def __init__(self, type_):
        self.Alpha = 255
        self.img = None
        self.type = type_
        self.mods = {}
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.screen: Screen = Screen(None, None, None, None, None, None)
        self.xy = (0, 0)
        self.wh = ()
        self.color = "blue"

    def delete(self):
        for item in self.screen.Items:
            if item == self:
                self.screen.Items.remove(self)

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod
            if not self.screen.root.var["mods"].get(mod.name, False):
                self.screen.root.var["mods"][mod.name] = {}

    def update(self):
        pass


def centerOf(i1: itemBase, i2: itemBase):
    w1, h1 = i1.rect.w, i1.rect.h
    w2, h2 = i2.rect.w, i2.rect.h
    return (w1/2)-(w2/2), (h1/2)-(h2/2)
