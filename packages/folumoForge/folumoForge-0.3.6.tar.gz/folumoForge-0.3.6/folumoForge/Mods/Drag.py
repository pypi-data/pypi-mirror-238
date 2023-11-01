import pygame

from .. import itemBase, modBase, Forge


def modThread(root: Forge, name):
    rn = [-1]
    while root.Running:
        items: list[itemBase] = []
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                items.append(item)

        keys = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()

        if keys[0]:
            for index, item in enumerate(items):
                if item.rect.collidepoint(pos):
                    if rn[0] == index or rn[0] == -1:
                        item.config(xy=(pos[0]-25, pos[1]-25))
                        rn[0] = index
                        break

        elif not keys[0]:
            rn[0] = -1
            break


class modDrag(modBase):
    def __init__(self, root: Forge):
        super().__init__(root, "modDrag", lambda: modThread(root, "modDrag"))
