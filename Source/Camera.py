from Config import *


class Camera:
    def __init__(self, level: 'Level', x: float = 0.0, y: float = 0.0):
        self.level = level

        # Position
        self.x = x
        self.y = y

        # Anchor
        self.ax = 0
        self.ay = 0

        # Limits
        self.lx = self.level.w * SIZE - W
        self.ly = self.level.h * SIZE

    def viewToRelative(self, x: int, y: int):
        return (int((x - self.x) // SIZE), int((y - self.y) // SIZE + self.level.h))

    def relativeToView(self, x: int, y: int):
        return x * SIZE + self.x, y * SIZE + self.y - self.ly

