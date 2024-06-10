import pygame as pg


class Player:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.sheet = pg.image.load("Assets/entity/Player.png")
        self.sprite = self.sheet.subsurface((0, 0, 17, 15))
        self.sprite = pg.transform.scale(self.sprite, (51, 45))

        self.rect = pg.Rect(0, 0, 1, 1)

        self.move(x, y)

    def move(self, x: float, y: float):
        """Moves the player to a new position"""
        self.x = x
        self.y = y
        self.rect.topleft = x, y

    def toDict(self):
        """Converts itself to dictionary"""
        return {"pos": [self.x, self.y]}
