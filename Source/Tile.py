from typing import Tuple

import pygame as pg

from Source.Utils import *

class Tile:
    def __init__(self, path: str, pos: Tuple[int, int], size: int, type: str):
        self.sheet = pg.image.load(path).convert_alpha()

        self.pos = pos

        self.type = type

        pos = [
            self.sheet.subsurface(pg.Rect(x, y, 16, 16))
            for y in range(0, 64, 16)
            for x in range(0, 64, 16)
        ]
        off = [
            (a, b, c, d) for a in [0, 1] for b in [0, 1] for c in [0, 1] for d in [0, 1]
        ]
        ind = [15, 14, 3, 2, 12, 13, 0, 1, 11, 10, 7, 6, 8, 9, 4, 5]

        self.sprites = {}
        for i, e in enumerate(ind):
            self.sprites[off[i]] = pg.transform.scale(pos[e], (size, size))

        self.sprite = self.sprites[(0, 0, 0, 0)]

    def update(self, grid):
        x, y = self.pos

        up = tryit(lambda: bool(grid[y - 1][x]), exc=False)
        down = tryit(lambda: bool(grid[y + 1][x]), exc=False)
        left = tryit(lambda: bool(grid[y][x - 1]), exc=False)
        right = tryit(lambda: bool(grid[y][x + 1]), exc=False)

        self.sprite = self.sprites[(up, right, down, left)]

    def toDict(self):
        """Converts itself to dictionary"""
        return {"type": self.type, "pos": list(self.pos)}
