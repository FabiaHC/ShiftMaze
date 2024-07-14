import config
from TileBoard import tileGenerator, generateTileBoard, shiftRow

import pygame


class Scene:
    def __init__(self):
        pass

    def update(self):
        pass

    def handleEvents(self, events):
        pass

    def draw(self, screen):
        pass


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        gameboyFontLarge = pygame.font.Font("assets/Early GameBoy.ttf", 74)
        gameboyFontSmall = pygame.font.Font("assets/Early GameBoy.ttf", 20)
        self.titleText = gameboyFontLarge.render("ShiftMaze", True, config.green4)
        self.titleTextRect = self.titleText.get_rect(center=(400, 300))
        self.startText = gameboyFontSmall.render("Press Anything To Start!", True, config.green4)
        self.startTextRect = self.startText.get_rect(center=(400, 500))


    def update(self):
        pass

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                return GamePlay()

    def draw(self, screen):
        screen.fill(config.green3)
        screen.blit(self.titleText, self.titleTextRect)
        screen.blit(self.startText, self.startTextRect)


class GamePlay(Scene):
    def __init__(self):
        super().__init__()
        self.tileBoard = generateTileBoard()
        self.tiles = tileGenerator()
        self.selectedRow = 0

    def update(self):
        pass

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYUP:  #shift rows
                if event.key == pygame.K_LEFT:
                    shiftRow(self.tileBoard, self.selectedRow)
                elif event.key == pygame.K_RIGHT:
                    shiftRow(self.tileBoard, self.selectedRow, False)
                elif event.key == pygame.K_DOWN:
                    self.selectedRow = (self.selectedRow + 1) % 5
                elif event.key == pygame.K_UP:
                    self.selectedRow = (self.selectedRow - 1) % 5
                    if self.selectedRow < 0:
                        self.selectedRow = 4

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                x, y = mousePos
                SBW = 3*16  #shift button width
                x -= 160
                y -= 60
                if y < 5*96:
                    row = y // 96
                    if x > -SBW and x < 0:
                        shiftRow(self.tileBoard, row, False)
                    elif x > 5*96 and x < 5*96+SBW:
                        shiftRow(self.tileBoard, row, True)

    def draw(self, screen):
        screen.fill(config.green3)
        xOffset = 160
        yOffset = 60
        for y in range(5):
            for x in range(5):
                screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96, yOffset+y*96))

        for y in range(5):
            screen.blit(self.tiles[6], (xOffset-3*16, yOffset+y*6*16))
            screen.blit(self.tiles[7], (xOffset+5*96, yOffset+y*6*16))
        for x in range(5):
            screen.blit(self.tiles[8], (xOffset+x*96, yOffset-3*16))
            screen.blit(self.tiles[9], (xOffset+x*96, yOffset+5*96))
