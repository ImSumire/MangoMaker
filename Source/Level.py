import pickle
import yaml
import json

import pygame as pg

from Config import *

from Source.Utils import *
from Source.Player import Player


class Level:
    def __init__(self):
        self.isLoaded = False

        self.w = 0
        self.h = 0

        self.player = None
        self.grid = []
        self.entities = []

        self.back = pg.transform.scale(
            pg.image.load("Assets/parallax/3.png").convert_alpha(), (W, H)
        )
        self.far = pg.transform.scale(
            pg.image.load("Assets/parallax/2.png").convert_alpha(), (W, H)
        )
        self.near = pg.transform.scale(
            pg.image.load("Assets/parallax/1.png").convert_alpha(), (W, H)
        )

    def fromBin(self, path):
        with open(path, "rb") as s:
            stage = pickle.load(s)

            self.w, self.h = stage["size"]
            self.player = Player(*stage["player"])
            self.grid = [[None for _ in range(self.w)] for _ in range(self.h)]
            self.entities = [self.player]

        self.isLoaded = True

    def __getitem__(self, key: int):
        return self.grid[key]

    def update(self, x: int, y: int):
        tryit(lambda: self[y - 1][x].update(self))
        tryit(lambda: self[y + 1][x].update(self))
        tryit(lambda: self[y][x - 1].update(self))
        tryit(lambda: self[y][x + 1].update(self))
        tryit(lambda: self[y][x].update(self))

    def toDict(self):
        return {
            "size": [self.w, self.h],
            "player": [int(self.player.x), int(self.player.y)],
            "grid": {
                f"{x} {y}": self[y][x].toDict()
                for x in range(self.w)
                for y in range(self.h)
                if self[y][x] is not None
            },
            "entities": [
                entity.toDict()
                for entity in self.entities
                if not isinstance(entity, Player)
            ],
        }

    def toYaml(self, path: str = "Stages/main.yml"):
        data = self.toDict()

        with open(path, "w+") as f:
            yaml.dump(data, f, allow_unicode=True)

    def toJson(self, path: str = "Stages/main.json"):
        data = self.toDict()

        with open(path, "w+") as f:
            json.dump(data, f)

    def toBin(self, path: str = "Stages/main.bin"):
        data = self.toDict()

        with open(path, "wb") as f:
            pickle.dump(data, f)
