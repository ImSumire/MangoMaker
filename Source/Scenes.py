from Config import *

import glob
import pygame as pg
from pygame import gfxdraw
from time import perf_counter

from Source.Utils import *

from Source.Tile import Tile
from Source.Level import Level
from Source.Camera import Camera
from Source.Eases import bounce_out
from Source.Transition import transition
from Source.Interface import Text, Button


class Scene:
    def __init__(self, game, title: str = ""):
        self.game = game
        self.sceneTitle = title

    def once(self):
        pg.display.set_caption(self.sceneTitle)

        # Fix the animations start
        start = perf_counter()
        [
            tryit(lambda: e.anim.setStart(start))
            for e in self.__dict__.values()
            if hasattr(e, "anim")
        ]

    def render(self, surf):
        ...

    def update(self):
        ...


class MainMenu(Scene):
    def __init__(self, game):
        super().__init__(game, "Main Menu")
        self.title = Text(
            "Super Mango Maker",
            size=64,
            anim=transition(
                (50, -180), (50, H - 160), duration=3.0, delay=2.0, ease=bounce_out
            ),
        )
        self.hero = Text(
            "Press A",
            size=32,
            anim=transition(
                (50, -100), (50, H - 70), duration=2.9, delay=2.0, ease=bounce_out
            ),
        )

    def render(self, surf):
        surf.fill((237, 194, 24))
        self.title.draw(surf)
        self.hero.draw(surf)

    def update(self):
        for event in self.game.events:
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                self.game.currentScene = self.game.chooseStageMenu


class ChooseStageMenu(Scene):
    def __init__(self, game):
        super().__init__(game, "Stage selection")

        pad = 48

        self.profileButton = Button(
            "Assets/profile.png",
            (pad, pad),
            (64, 64),
            lambda: setattr(self.game, "currentScene", self.game.settingsMenu),
        )
        # self.profile = pg.Rect(pad, pad, 64, 64)
        self.hero = Text("Choose a stage :", (pad, 96 + pad), 48)

        w, h = 256, 128
        gap = 16
        wGap = w + gap
        hGap = h + gap
        maxLign = W // wGap
        leftPad = (W - ((maxLign * wGap) - gap)) // 2
        topPad = self.hero.rect.height + gap + gap + (96 + pad)

        self.stages = []

        for i, path in enumerate(sorted(glob.glob("Stages/*.bin"))):
            thumbnail = Button(
                path.replace(".bin", ".png"),
                (leftPad + wGap * (i % maxLign), topPad + hGap * (i // maxLign)),
                (w, h),
                func=lambda: (
                    setattr(self.game, "currentScene", self.game.editingMenu),
                    self.game.currentScene.load(path),
                ),
            )
            # thumbnail = pg.Rect(
            #     leftPad + wGap * (i % maxLign), topPad + hGap * (i // maxLign), w, h
            # )

            title = Text(
                toName(path),
                (
                    leftPad + wGap * (i % maxLign) + gap,
                    topPad + hGap * (i // maxLign) + gap,
                ),
                outlined=True,
            )

            self.stages.append((thumbnail, title))

        self.dt = 0

    def render(self, surf):
        surf.fill((227, 185, 18))

        # Profile
        # pg.draw.rect(surf, (255, 255, 255), self.profile)
        self.profileButton.draw(surf)

        # Choose a stage
        self.hero.draw(surf)

        # Stages
        for thumbnail, title in self.stages:
            # pg.draw.rect(surf, (230, 215, 215), thumbnail)
            thumbnail.draw(surf)
            title.draw(surf)

    def update(self):
        key = pg.key.get_pressed()
        # if key[pg.K_e]:  # A
        #     self.game.currentScene = self.game.editingMenu
        #     self.game.currentScene.load("main")
        if key[pg.K_SPACE]:  # Menu
            self.game.currentScene = self.game.settingsMenu
        elif key[pg.K_b]:
            self.game.currentScene = self.game.mainMenu

        for button, _ in self.stages:
            button.check(self.game.mx, self.game.my, self.game.mouseInput)
        self.profileButton.check(self.game.mx, self.game.my, self.game.mouseInput)

        self.dt += 1


class SettingsMenu(Scene):
    def __init__(self, game):
        super().__init__(game, "Profile / Settings")

    def render(self, surf):
        surf.fill((237, 194, 24))

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_b]:
            self.game.currentScene = self.game.chooseStageMenu


class EditingMenu(Scene):
    def __init__(self, game):
        super().__init__(game, "Editing")
        self.level = Level()
        self.camera = None

        # Menu
        self.slot = 0
        self.menuRect = pg.Rect(25, 25, W - 50, 75)
        self.buttons = [
            Button(
                path.replace("block", "ui"),
                pos=((SIZE * 0.8) * (2 * i + 1), SIZE - 7),
                size=(SIZE, SIZE),
                func=lambda i=i: setattr(self, "slot", i),
                hover="outline",
            )
            for i, path in BLOCKS.items()
        ]

        self.playButton = Button(
            "Assets/ui/play.png", pos=(W - (20 + 64), H - (20 + 64)), size=(64, 64)
        )

        # Editing
        self.grabCamera = False
        self.grabedEntity = None

        self.rx, self.ry = 0, 0  # Relative position

        self.hoverMenu = False
        self.hoverPlay = False
        self.hoverUi = False

    def load(self, path):
        self.level.fromBin(path)
        self.camera = Camera(self.level, y=H)

    def drawParallax(self, surf):
        """Draws parallax scrolling backgrounds"""
        x, y = self.camera.x, self.camera.y

        backX, backY = (x * 0.01) % W, (y - H) * 0.05
        surf.blit(self.level.back, (backX, backY))
        surf.blit(self.level.back, (backX - W, backY))

        farX, farY = (x * 0.04) % W, (y - H) * 0.1
        surf.blit(self.level.far, (farX, farY))
        surf.blit(self.level.far, (farX - W, farY))

        nearX, nearY = (x * 0.16) % W, (y - H) * 0.2
        surf.blit(self.level.near, (nearX, nearY))
        surf.blit(self.level.near, (nearX - W, nearY))

    def drawGrid(self, surf):
        """Draws a grid on the screen"""
        x, y = int(self.camera.x), int(self.camera.y)

        # Draw vertical lines
        [
            pg.draw.line(surf, (119, 222, 224), (_x, 0), (_x, H))
            for _x in range(x % SIZE, W + x % SIZE, SIZE)
        ]

        # Draw horizontal lines
        [
            pg.draw.line(surf, (119, 222, 224), (0, _y), (W, _y))
            for _y in range(y % SIZE, H + y % SIZE, SIZE)
        ]

    def drawMenu(self, surf):
        """Draws the editor menu"""
        gfxdraw.box(surf, self.menuRect, (0, 0, 0, 64))

        for button in self.buttons:
            button.draw(surf)

    def drawPlayButton(self, surf):
        self.playButton.draw(surf)

    def drawPreview(self, surf):
        """Draws a preview of the selected item"""
        if self.hoverUi or self.grabedEntity:
            return

        preview = self.buttons[self.slot].surf.copy()
        preview.set_alpha(128)

        surf.blit(preview, self.camera.relativeToView(self.rx, self.ry))

    def render(self, surf):
        """Renders the current game state"""
        surf.fill((148, 253, 255))
        self.drawParallax(surf)
        self.drawGrid(surf)

        for y, row in enumerate(self.level.grid):
            for x, obj in enumerate(row):
                if obj:
                    surf.blit(obj.sprite, self.camera.relativeToView(x, y))

        player = self.level.player
        surf.blit(player.sprite, self.camera.relativeToView(player.x, player.y))

        self.drawPreview(surf)
        self.drawMenu(surf)
        self.drawPlayButton(surf)

    def update(self):
        mx, my = self.game.mx, self.game.my

        # Convert mouse position to relative coordinates
        self.rx, self.ry = self.camera.viewToRelative(mx, my)

        # Check if mouse is hovering over ui
        self.hoverMenu = self.menuRect.collidepoint(mx, my)
        self.hoverPlay = self.playButton.rect.collidepoint(mx, my)

        self.hoverUi = self.hoverMenu or self.hoverPlay

        self.controls()

        for b in self.buttons:
            b.check(self.game.mx, self.game.my, self.game.mouseInput)

        '''
                        Return to main menu
        Are you sure you want to return to the main menu?
                 All unsaved progress will be lost.

        Return to the main menu without saving
        Save progress
        Cancel
        '''

    def controls(self):
        mx, my = self.game.mx, self.game.my
        mouseInput = self.game.mouseInput

        # Camera mouvement
        if mouseInput[1]:
            tryit(lambda: pg.mouse.set_cursor(self.game.grab))
            if not self.grabCamera:
                self.grabCamera = True
                self.camera.ax = mx - self.camera.x
                self.camera.ay = my - self.camera.y
        else:
            self.grabCamera = False

        if self.grabCamera:
            self.camera.x = clamp(mx - self.camera.ax, -self.camera.lx, 0)
            self.camera.y = clamp(my - self.camera.ay, H, self.camera.ly)

        # Place / Move entity
        if mouseInput[0]:
            if not self.hoverUi:
                # Check if mouse is over an entity
                for entity in self.level.entities:
                    if entity.rect.collidepoint(self.rx, self.ry):
                        self.grabedEntity = entity
                        break

                if self.grabedEntity:
                    self.grabedEntity.move(self.rx, self.ry)

                else:
                    # Place tile
                    try:
                        self.level[self.ry][self.rx] = Tile(
                            path=BLOCKS[self.slot],
                            pos=(self.rx, self.ry),
                            size=SIZE,
                            type=TYPES[self.slot],
                        )
                        self.level.update(self.rx, self.ry)
                    except:
                        pass
        else:
            self.grabedEntity = None

        # Remove tile / entity
        if mouseInput[2]:
            if not self.hoverUi:
                self.level[self.ry][self.rx] = None
                self.level.update(self.rx, self.ry)
