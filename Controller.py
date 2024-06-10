# sudo apt-get install xboxdrv
from math import cos, sin
import pygame as pg

W, H = 1280, 720

pg.init()
pg.joystick.init()
screen = pg.display.set_mode((W, H), 0, 32)
clock = pg.time.Clock()
pg.display.set_caption("Controller")


class Player:
    def __init__(self, x=100.0, y=H // 2 - 10.0):
        self.x, self.y = x, y
        self.ix, self.iy = 0.0, 0.0

    def draw(self, surf):
        pg.draw.rect(
            surf,
            (255, 255, 255),
            (self.x + self.ix * 20.0, self.y + self.iy * 20.0, 20, 20),
        )


controllers = set([pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())])


buttons = [
    "A",
    "B",
    "unknow(1)",
    "X",
    "Y",
    "unknow(2)",
    "LB",
    "RB",
    "3unknow",
    "4unknow",
    "View",
    "Menu",
    "Xbox",
    "LEFT",
    "RIGHT",
]

left = Player()
left2 = Player(y=H // 2 - 80.0)
right = Player(x=W - 120.0)
right2 = Player(x=W - 120.0, y=H // 2 - 80.0)
hat = Player(x=W // 4 - 10.0, y=H // 2 + 50.0)

while True:
    screen.fill((0, 0, 0))

    left.draw(screen)
    left2.draw(screen)
    right.draw(screen)
    right2.draw(screen)
    hat.draw(screen)

    for event in pg.event.get():
        ### Buttons
        if event.type == pg.JOYBUTTONDOWN:
            print(f"{buttons[event.button]} pressed")

        elif event.type == pg.JOYBUTTONUP:
            print(f"{buttons[event.button]} unpressed")

        ### Axis
        if event.type == pg.JOYAXISMOTION:
            # Prevent joystick drift
            if abs(event.value) < 0.1:
                event.value = 0.0

            if event.axis == 0:
                left.ix = event.value
            elif event.axis == 1:
                left.iy = event.value
            elif event.axis == 2:
                right.ix = event.value
            elif event.axis == 3:
                right.iy = event.value
            elif event.axis == 4:
                right2.iy = event.value
            elif event.axis == 5:
                left2.iy = event.value

        ### Hat
        if event.type == pg.JOYHATMOTION:
            hat.ix, hat.iy = event.value
            hat.iy *= -1

        ### Add device
        if event.type == pg.JOYDEVICEADDED:
            _controllers = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for c in _controllers:
                if c not in controllers:
                    print(f'{c.get_name()} added !')
            controllers = set(_controllers)

        ### Remove device
        if event.type == pg.JOYDEVICEREMOVED:
            _controllers = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for c in controllers:
                if c not in _controllers:
                    print(f'{c.get_name()} removed !')
            controllers = set(_controllers)

        if event.type == pg.QUIT:
            pg.quit()
            exit()

    pg.display.update()
    clock.tick(60)
