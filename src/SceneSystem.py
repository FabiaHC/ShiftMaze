import config
from TileBoard import tileGenerator, generateTileBoard, shiftRow, shiftColumn

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

        self.slideOffset = 0
        self.slideDirection = 1
        self.slidingRow = None
        self.slidingCol = None

    def update(self):
        if self.slideOffset != 0:
            self.slideOffset = abs(self.slideOffset)
            self.slideOffset += 1
            self.slideOffset %= 96
            self.slideOffset *= self.slideDirection
            if self.slideOffset == 0:

                if self.slidingRow != None:
                    if self.slideDirection == 1:
                        shiftRow(self.tileBoard, self.slidingRow, False)
                    elif self.slideDirection == -1:
                        shiftRow(self.tileBoard, self.slidingRow, True)
                    self.slidingRow = None

                elif self.slidingCol != None:
                    if self.slideDirection == 1:
                        shiftColumn(self.tileBoard, self.slidingCol, True)
                    elif self.slideDirection == -1:
                        shiftColumn(self.tileBoard, self.slidingCol, False)
                    self.slidingCol = None

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                x, y = mousePos
                SBSS = 3*16 #shift button shorter size
                x -= 160    #remove offset
                y -= 60     #remove offset

                if self.slideOffset != 0:   #ignore input during sliding animation
                    continue

                if y > 0 and y < 5*96:
                    row = y // 96
                    if x > -SBSS and x < 0:             #right shift arrows
                        self.slidingRow = row
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif x > 5*96 and x < 5*96+SBSS:    #left shift arrows
                        self.slidingRow = row
                        self.slideOffset = -1
                        self.slideDirection = -1

                if x > 0 and x < 5*96:
                    column = x // 96
                    if y > -SBSS and y < 0:             #down shift arrows
                        self.slidingCol = column
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif y > 5*96 and y < 5*96+SBSS:    #up shift arrows
                        self.slidingCol = column
                        self.slideOffset = -1
                        self.slideDirection = -1

    def draw(self, screen):
        screen.fill(config.green3)
        xOffset = 160
        yOffset = 60
        for y in range(5):
            for x in range(5):
                if x == self.slidingCol:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96, yOffset+y*96 + self.slideOffset))
                elif y == self.slidingRow:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96+self.slideOffset, yOffset+y*96))
                else:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96, yOffset+y*96))


        for y in range(5):
            screen.blit(self.tiles[6], (xOffset-3*16, yOffset+y*6*16))
            screen.blit(self.tiles[7], (xOffset+5*96, yOffset+y*6*16))
        for x in range(5):
            screen.blit(self.tiles[8], (xOffset+x*96, yOffset-3*16))
            screen.blit(self.tiles[9], (xOffset+x*96, yOffset+5*96))
