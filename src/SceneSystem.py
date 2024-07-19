import config
from TileBoard import tileGenerator, generateTileBoard, shiftRow, shiftColumn, findRoute
from characters import loadPlayerImgs

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
        self.playerImgs = loadPlayerImgs()
        self.playerDir = "right"
        self.currentPlayerImg = self.playerImgs[self.playerDir][1]
        self.playerImgFrame = 0

        self.scoreTracker = {}
        for scoreMod in config.scores:
            self.scoreTracker[scoreMod] = 0
        self.scoreTracker["INTERMEDIATE_STEPS"] = 0

        self.playerX = 0
        self.playerY = 0
        self.movingRoute = None
        self.movingDelay = 0

        self.slideOffset = 0
        self.slideDirection = 1
        self.slidingRow = None
        self.slidingCol = None

    def update(self):
        if self.movingRoute != None:

            self.movingDelay %= config.playerSpeed

            if self.movingDelay == 0:
                self.playerY, self.playerX = self.movingRoute.pop(0)

                if len(self.movingRoute) == 0:
                    self.movingRoute = None
                    if self.tileBoard[self.playerY][self.playerX] == "goal":
                        self.updateScore("GOAL")
                        quit()
                    return

                endPosY, endPosX = self.movingRoute[-1]
                if (self.tileBoard[endPosY][endPosX] == "goal"):
                    self.updateScore("GOAL_STEPS")
                else:
                    self.updateScore("INTERMEDIATE_STEPS")


                playerDirX = self.movingRoute[0][1] - self.playerX
                playerDirY = self.movingRoute[0][0] - self.playerY
                if playerDirX == 1:
                    self.playerDir = "right"
                elif playerDirX == -1:
                    self.playerDir = "left"
                elif playerDirY == 1:
                    self.playerDir = "down"
                elif playerDirY == -1:
                    self.playerDir = "up"

            if self.movingDelay % config.playerAnimationSpeed == 0:
                self.playerImgFrame += 1
                self.playerImgFrame %= 2
                self.currentPlayerImg = self.playerImgs[self.playerDir][self.playerImgFrame]

            self.movingDelay += 1


        if self.slideOffset != 0:
            self.slideOffset = abs(self.slideOffset)
            self.slideOffset += 1
            self.slideOffset %= 96
            self.slideOffset *= self.slideDirection
            if self.slideOffset == 0: # finish sliding

                self.updateScore("MAZE_SHIFTING")

                if self.slidingRow != None:
                    shiftRow(self.tileBoard, self.slidingRow, (self.slideDirection == -1))
                    if self.playerY == self.slidingRow:
                        self.playerX += self.slideDirection
                        self.updateScore("PLAYER_SHIFTING")
                    self.slidingRow = None

                elif self.slidingCol != None:
                    shiftColumn(self.tileBoard, self.slidingCol, (self.slideDirection == 1))
                    if self.playerX == self.slidingCol:
                        self.playerY += self.slideDirection
                        self.updateScore("PLAYER_SHIFTING")
                    self.slidingCol = None

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                x, y = mousePos
                SBSS = 3*16 #shift button shorter size
                x -= config.xOffset    #remove offset
                y -= config.yOffset     #remove offset

                if self.slideOffset != 0 or self.movingRoute != None: #ignore input during sliding animation
                    continue

                if y > 0 and y < 5*96:
                    row = y // 96
                    if x > -SBSS and x < 0 and not (self.playerY == row and self.playerX == 4): #right shift arrows
                        self.slidingRow = row
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif x > 5*96 and x < 5*96+SBSS and not (self.playerY == row and self.playerX == 0): #left shift arrows
                        self.slidingRow = row
                        self.slideOffset = -1
                        self.slideDirection = -1

                if x > 0 and x < 5*96:
                    column = x // 96
                    if y > -SBSS and y < 0 and not (self.playerX == column and self.playerY == 4): #down shift arrows
                        self.slidingCol = column
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif y > 5*96 and y < 5*96+SBSS and not (self.playerX == column and self.playerY == 0): #up shift arrows
                        self.slidingCol = column
                        self.slideOffset = -1
                        self.slideDirection = -1

                if x > 0 and x < 5*96 and y > 0 and y < 5*96:
                    row = y // 96
                    column = x // 96
                    start = (self.playerY, self.playerX)
                    end = (row, column)
                    self.movingRoute = findRoute(self.tileBoard, start, end)

    def draw(self, screen):
        screen.fill(config.green3)

        xOffset = config.xOffset
        yOffset = config.yOffset

        for y in range(5):
            for x in range(5):
                if x == self.slidingCol:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96, yOffset+y*96 + self.slideOffset))
                elif y == self.slidingRow:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96+self.slideOffset, yOffset+y*96))
                else:
                    screen.blit(self.tiles[self.tileBoard[y][x]], (xOffset+x*96, yOffset+y*96))

        if self.slideOffset != 0:
            if self.slidingCol != None:
                tempTileCol = self.slidingCol                                       #either first or last tile
                tempTileRow = 2 + (self.slideDirection*2)
                tempTileX = tempTileCol*96                                          #96*2 is the median point
                tempTileY = 96*2 - (self.slideDirection*96*3) + self.slideOffset

            elif self.slidingRow != None:
                tempTileCol = 2 + (self.slideDirection*2)                           #either first or last tile
                tempTileRow = self.slidingRow
                tempTileX = 96*2 - (self.slideDirection*96*3) + self.slideOffset    #96*2 is the median point
                tempTileY = tempTileRow*96

            screen.blit(self.tiles[self.tileBoard[tempTileRow][tempTileCol]], (xOffset+tempTileX, yOffset+tempTileY))


        for y in range(5):
            screen.blit(self.tiles["rightArrow"], (xOffset - (3*16 + 3*16), yOffset+y*6*16))   #(3*16 + 3*16) is used because it used to only be half the width
            screen.blit(self.tiles["leftArrow"], (xOffset+5*96, yOffset+y*6*16))
        for x in range(5):
            screen.blit(self.tiles["downArrow"], (xOffset+x*96, yOffset - (3*16 + 3*16)))     #same here
            screen.blit(self.tiles["upArrow"], (xOffset+x*96, yOffset+5*96))

        MR = self.movingRoute
        playerOffsetX = self.playerX*96+32
        playerOffsetY = self.playerY*96+32
        if MR != None:
            playerOffsetX += (MR[0][1] - self.playerX) * 96/config.playerSpeed * self.movingDelay
            playerOffsetY += (MR[0][0] - self.playerY) * 96/config.playerSpeed * self.movingDelay
        elif self.slidingRow == self.playerY:
            playerOffsetX += self.slideOffset
        elif self.slidingCol == self.playerX:
            playerOffsetY += self.slideOffset
        screen.blit(self.currentPlayerImg, (xOffset+playerOffsetX, yOffset+playerOffsetY))

    def updateScore(self, scoreMod):
        self.scoreTracker[scoreMod] += 1

    def calculateScore(self):
        pass
