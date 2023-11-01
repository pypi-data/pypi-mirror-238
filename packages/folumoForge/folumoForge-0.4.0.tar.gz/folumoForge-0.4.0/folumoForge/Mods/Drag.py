import pygame

from .. import itemBase, modBase, Forge


def modThread(root: Forge, name):
    rn = [-1]
    while root.Running:
        items: list[itemBase] = []
        loopItems = root.Screens[root.Screen].Items.copy()
        loopItems.extend(root.Screens[root.Screen].EventAble.copy())
        for item in loopItems:
            if name in item.mods:
                if item.show:
                    items.append(item)

        keys = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        if keys[0]:
            for index, item in enumerate(items):
                if item.mods[name].draggable:
                    tmp = item.rect
                    tmp.x = item.xy[0]
                    tmp.y = item.xy[1]

                    if tmp.collidepoint(pos) or rn[0] == index:
                        if rn[0] == index or rn[0] == -1:
                            item.config((pos[0]-tmp.w/2, pos[1]-tmp.h/2))
                            rn[0] = index
                            break


        elif not keys[0]:
            rn[0] = -1


class modDrag(modBase):
    def __init__(self, root: Forge):
        super().__init__(root, "modDrag", lambda: modThread(root, "modDrag"))
        self.draggable = True
