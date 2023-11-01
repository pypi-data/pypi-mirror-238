from time import sleep

from .. import modBase, Forge


def modThread(root: Forge, name):
    while root.Running:
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                mod = item.mods[name]
                if mod.Fading or mod.loop:
                    dTime = root.delta_time / 1000

                    mod.lastIndex += mod.speed

                    try:
                        item.Alpha = mod.fromTo[mod.lastIndex]
                    except IndexError:
                        mod.Fading = False
                        mod.postAni()

                    sleep(dTime)


class modFade(modBase):
    def __init__(self, root: Forge, speed=1, fromTo=None, loop=False, postAnimation=None):
        super().__init__(root, "modFade", lambda: modThread(root, "modFade"))

        if fromTo is None:
            fromTo = list(range(1, 256))

        self.Fading = True

        self.lastIndex = -1

        self.speed = speed
        self.fromTo = fromTo
        self.postAni = postAnimation

        self.loop = loop

    def postAnimation(self):
        if self.postAni:
            self.postAni(self)
