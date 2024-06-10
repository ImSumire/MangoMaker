from random import uniform, randint
from typing import Callable, Any
from noise import snoise2
from math import sqrt
import pygame as pg


W, H = 1280, 720

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
pg.display.set_caption("Wata")


def dist(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def tryit(target: Callable, args: Any = None, exc: Any = None):
    try:
        if args is None:
            return target()
        return target(args)
    except:
        return exc


class Hitbox:
    def __init__(self, x=0, y=0, r=30):
        self.x = x
        self.y = y
        self.r = r

        self.vx = 0
        self.vy = 0

    def move(self, x, y):
        self.vx = self.x - x
        self.vy = self.y - y

        self.x = x
        self.y = y


class Node:
    def __init__(self, x, y, wata: 'Wata'):
        self.wata = wata

        self.x = x
        self.y = y

        self.vy = 0

    def update(self, h, r, l):
        self.vy += (h - self.y) * 0.009

        self.vy += (r - self.y) * 0.07
        self.vy += (l - self.y) * 0.07

        self.y += self.vy

        self.vy *= 0.9

        if self.vy < -10 and not randint(0, 6):
            self.wata.drips.append(Drip(
                x=self.x,
                y=self.y,
                vx=uniform(-10.0, 10.0),
                vy=self.vy * 1.12,
                wata=self.wata
            ))

class Drip:
    def __init__(self, x, y, vx, vy, wata: 'Wata'):
        self.wata = wata

        self.r = randint(1, 3)

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.9
        # self.vy *= 0.9
        self.vy += 0.75  # Gravity

        if self.y > self.wata.bottomLeft[1]:
            self.wata.drips.remove(self)


class Wata:
    def __init__(self, gap=15, num=80):
        # Simulation constants
        self.h = H // 2  # Base height
        self.s = uniform(-2e3, 2e3)  # Noise seed
        self.r = range(num)  # Range of nodes

        # Style
        self.leftPad = W // 2 - (num * gap) // 2
        self.bottomRight = W - self.leftPad - gap, self.h + 200
        self.bottomLeft = self.leftPad, self.h + 200
        self.bottom = [self.bottomRight, self.bottomLeft]
        self.c = (50, 150, 255)  # Color of wata

        # Nodes / Particules
        self.nodes = [
            Node(
                self.leftPad + gap * i,
                self.h + snoise2(i * 0.03, self.s) * 180,
                self
            )
            for i in range(num)
        ]
        self.drips = []

    def __getitem__(self, key: int):
        return self.nodes[key]

    def draw(self, surf):
        # [pg.draw.circle(surf, self.c, (n.x, n.y), 4) for n in self.nodes]
        # [tryit(lambda: pg.draw.line(surf, self.c, (self[i].x, self[i].y), (self[i + 1].x, self[i + 1].y))) for i in self.r]
        pg.draw.polygon(surf, self.c, self.polygon)
        [pg.draw.circle(surf, self.c, (d.x, d.y), d.r) for d in self.drips]

    @property
    def polygon(self):
        return [(n.x, n.y) for n in self.nodes] + self.bottom

    def update(self):
        [
            self[i].update(
                self.h,
                tryit(lambda: self[i - 1].y, exc=self[i].y),
                tryit(lambda: self[i + 1].y, exc=self[i].y),
            )
            for i in self.r
        ]
        [d.update() for d in self.drips]

    def perturbe(self, hitbox):
        x, y, vx, vy, r = hitbox.x, hitbox.y, hitbox.vx, hitbox.vy, hitbox.r
        for i in self.r:
            if dist(self[i].x, self[i].y, x, y) < r:
                self[i].vy -= (y - self[i].y) * 0.07 * sqrt(abs(vx + vy))


wata = Wata()
mouse = Hitbox()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                wata.__init__()

    mx, my = pg.mouse.get_pos()
    mouse.move(mx, my)
    wata.update()
    wata.perturbe(mouse)

    screen.fill(0)
    wata.draw(screen)
    pg.draw.circle(screen, (255, 255, 255), (mx, my), mouse.r, 1)

    pg.display.flip()
    clock.tick(60)
