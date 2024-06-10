import os
from time import perf_counter

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

from Config import *

from Source.Utils import *
from Source.Scenes import *
from Source.Eases import power4_inOut
from Source.Transition import transition


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()

        self.events = []

        # Cursors
        self.pointerSprite = pg.transform.scale2x(
            pg.image.load("Assets/pointer.png").convert_alpha()
        )
        self.pointer = pg.cursors.Cursor((0, 0), self.pointerSprite)

        self.grabSprite = pg.transform.scale2x(
            pg.image.load("Assets/grab.png").convert_alpha()
        )
        self.grab = pg.cursors.Cursor((0, 0), self.grabSprite)

        self.clickSprite = pg.transform.scale2x(
            pg.image.load("Assets/click.png").convert_alpha()
        )
        self.click = pg.cursors.Cursor((8, 8), self.clickSprite)

        tryit(lambda: pg.mouse.set_cursor(self.pointer))

        # Scenes
        self.mainMenu = MainMenu(self)
        self.chooseStageMenu = ChooseStageMenu(self)

        self.settingsMenu = SettingsMenu(self)

        self.editingMenu = EditingMenu(self)
        self.playingMenu = Scene(self)

        # Scenes management
        self.anim = transition((0,), (-W,), ease=power4_inOut)
        self.lastScene = None
        self.lastSceneSurf = pg.Surface((W, H))
        self._currentScene = self.mainMenu
        self.currentScene = self.mainMenu


    @property
    def currentScene(self):
        return self._currentScene

    @currentScene.setter
    def currentScene(self, value):
        self.lastScene = self.currentScene
        self.lastScene.render(self.lastSceneSurf)

        self._currentScene = value
        self.currentScene.once()

        self.anim.setStart(perf_counter())

    def transition(self):
        _x = self.anim()[0]
        if _x != -W:
            self.screen.blit(self.lastSceneSurf, (_x, 0))


    def loop(self):

        while True:
            self.events = pg.event.get()
            for event in self.events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            # Get mouse position and state
            self.mx, self.my = pg.mouse.get_pos()
            self.mouseInput = pg.mouse.get_pressed()

            pg.mouse.set_cursor((self.pointer, self.click)[self.mouseInput[0]])

            # Update
            self.currentScene.update()

            # Render
            self.currentScene.render(self.screen)
            self.transition()

            pg.display.flip()
            self.clock.tick(60)

Game().loop()
