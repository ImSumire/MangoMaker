from typing import Tuple, Callable
import pygame as pg


class Text:
    def __init__(
        self,
        text="Lorem Ipsum",
        pos=(0, 0),
        size=32,
        color=(1, 1, 1),
        anim: Callable = None,
        outlined: bool = False,
    ):
        self.text = text

        self.x, self.y = pos
        self.size = size
        self.color = color

        self.anim = anim

        self.font = pg.font.Font("Assets/Round9x13.ttf", size)
        self.surf = self.font.render(text, True, color)
        if outlined:
            self.surf = self.makeOutlines(self.surf)
        self.rect = self.surf.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    @staticmethod
    def makeOutlines(surf):
        w, h = surf.get_size()
        outlined = pg.Surface((w + 4, h + 4))
        outlined.set_colorkey((0, 0, 0))
        mask = pg.mask.from_surface(surf)
        wmask = mask.to_surface()
        wmask.set_colorkey((0, 0, 0))
        outlined.blit(wmask, (1, 2))
        outlined.blit(wmask, (1, 0))
        outlined.blit(wmask, (2, 1))
        outlined.blit(wmask, (0, 1))
        outlined.blit(surf, (1, 1))
        return outlined

    def draw(self, surf):
        if self.anim:
            self.rect.x, self.rect.y = self.anim()
        surf.blit(self.surf, self.rect)


class Button:
    def __init__(
        self,
        path: str,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        func: Callable = lambda: None,
        hover: str = ''
    ):
        self.x, self.y = pos
        self.w, self.h = size
        self.id = id
        self.func = func

        try:
            self.surf = pg.image.load(path).convert_alpha()
        except:
            self.surf = pg.Surface((self.w, self.h))
            
        self.rect = pg.Rect((self.x, self.y, self.w, self.h))
        self.rect.topleft = pos

        self.surfHover = self.surf.copy()
        self.rectHover = self.rect.copy()

        if 'outline' in hover:
            self.surfHover = self.makeOutlines(self.surf)
            self.surfHover = pg.transform.scale(self.surfHover, (self.w + 12, self.h + 12))
            self.rectHover = pg.Rect((self.x - 3, self.y - 3, self.w + 12, self.h + 12))
        else:
            self.surfHover = pg.transform.scale(self.surfHover, (self.w, self.h))
        
        self.surf = pg.transform.scale(self.surf, (self.w, self.h))

        self.display = self.surf
        self.displayRect = self.rect

        self.pressed = False

    @staticmethod
    def makeOutlines(surf):
        w, h = surf.get_size()
        outlined = pg.Surface((w + 4, h + 4))
        outlined.set_colorkey((0, 0, 0))
        mask = pg.mask.from_surface(surf)
        wmask = mask.to_surface()
        wmask.set_colorkey((0, 0, 0))
        outlined.blit(wmask, (1, 2))
        outlined.blit(wmask, (1, 0))
        outlined.blit(wmask, (2, 1))
        outlined.blit(wmask, (0, 1))
        outlined.blit(surf, (1, 1))
        return outlined

    def draw(self, surf: pg.Surface):
        surf.blit(self.display, self.displayRect)

    def check(self, mx: int, my: int, mi: Tuple[bool, bool, bool]):
        if self.rect.collidepoint((mx, my)):
            # Hover
            self.display = self.surfHover
            self.displayRect = self.rectHover

            if mi[0]:
                # Clicked
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    self.func()
                    # return True
        else:
            self.display = self.surf
            self.displayRect = self.rect
