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
        self.startText = gameboyFontSmall.render("Press SPACE To Start!", True, config.green4)
        self.startTextRect = self.startText.get_rect(center=(400, 500))
        self.leaderboardText = gameboyFontSmall.render("Press TAB To Show Leaderboard!", True, config.green4)
        self.leaderboardTextRect = self.leaderboardText.get_rect(center=(400, 550))

    def update(self):
        pass

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return GamePlay()
                if event.key == pygame.K_TAB:
                    return Leaderboard()

    def draw(self, screen):
        screen.fill(config.green3)
        screen.blit(self.titleText, self.titleTextRect)
        screen.blit(self.startText, self.startTextRect)
        screen.blit(self.leaderboardText, self.leaderboardTextRect)


class Leaderboard(Scene):
    def __init__(self):
        super().__init__()
        gameboyFontSmall = pygame.font.Font("assets/Early GameBoy.ttf", 20)
        self.mainmenuText = gameboyFontSmall.render("Press TAB To Return To Main Menu!", True, config.green4)
        self.mainmenuTextRect = self.mainmenuText.get_rect(center=(400, 550))

        self.scores = [
            {"name" : "UserA", "score" : 34},
            {"name" : "UserB", "score" : 21},
            {"name" : "UserC", "score" : 13},
            {"name" : "UserD", "score" : 8},
            {"name" : "UserE", "score" : 5},
            {"name" : "UserF", "score" : 3},
            {"name" : "UserG", "score" : 2},
            {"name" : "UserH", "score" : 1},
            {"name" : "UserI", "score" : 1},
            {"name" : "UserJ", "score" : 0}
        ]
        self.drawUpScores()

    def drawUpScores(self):
        self.leaderboardImg = pygame.Surface((800, 600))
        self.leaderboardImgRect = self.leaderboardImg.get_rect(center=(400, 300))
        self.leaderboardImg.fill(config.green3)
        scoreFont = pygame.font.Font("assets/Early GameBoy.ttf", 30)

        scoreY = 50
        placeCounter = 1
        for score in self.scores:
            placeCounterText = scoreFont.render(str(placeCounter), True, config.green4)
            nameText = scoreFont.render(score["name"], True, config.green4)
            scoreValueText = scoreFont.render(str(score["score"]), True, config.green4)

            placeCounterX = 50
            nameX = 150
            scoreX = 500

            placeCounterRect = placeCounterText.get_rect(midleft=(placeCounterX, scoreY))
            nameRect = nameText.get_rect(midleft=(nameX, scoreY))
            scoreValueRect = scoreValueText.get_rect(midleft=(scoreX, scoreY))

            self.leaderboardImg.blit(placeCounterText, placeCounterRect)
            self.leaderboardImg.blit(nameText, nameRect)
            self.leaderboardImg.blit(scoreValueText, scoreValueRect)

            placeCounter += 1
            scoreY += 40

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    return MainMenu()

    def draw(self, screen):
        screen.blit(self.leaderboardImg, self.leaderboardImgRect)
        screen.blit(self.mainmenuText, self.mainmenuTextRect)


class GamePlay(Scene):
    def __init__(self):
        super().__init__()
        self.tiles = tileGenerator()
        self.playerImgs = loadPlayerImgs()

        self.scoreTracker = {}
        for scoreMod in config.scores:
            self.scoreTracker[scoreMod] = 0
        self.scoreTracker["INTERMEDIATE_STEPS"] = 0

        self.gameboyFont = pygame.font.Font("assets/Early GameBoy.ttf", 30)

        self.countdown = 30.00
        self.reset()

    def reset(self):
        self.tileBoard = generateTileBoard()

        self.countdown += 30
        if self.countdown > 99.99:
            self.countdown = 99.99

        self.playerDir = "right"
        self.currentPlayerImg = self.playerImgs[self.playerDir][1]
        self.playerImgFrame = 0

        self.playerX = 0
        self.playerY = 0
        self.movingRoute = None
        self.movingDelay = 0

        self.goalX = 4
        self.goalY = 4

        self.slideOffset = 0
        self.slideDirection = 1
        self.slidingRow = None
        self.slidingCol = None

    def updateCountdown(self):
        self.countdown -= 1/60
        if self.countdown < 0:
            self.countdown = 0
        countdownStr = "{0:.2f}".format(self.countdown)
        self.countdownImg = self.gameboyFont.render(countdownStr, True, config.green4)
        self.countdownImgRect = self.countdownImg.get_rect(left=10, top=0)

    def update(self):
        self.updateCountdown()

        if self.movingRoute != None:

            self.movingDelay %= config.playerSpeed

            if self.movingDelay == 0:
                self.playerY, self.playerX = self.movingRoute.pop(0)

                if len(self.movingRoute) == 0:
                    self.movingRoute = None
                    if self.playerY == self.goalY and self.playerX == self.goalX:
                        self.updateScore("GOAL")
                        self.reset()
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
                    elif self.goalY == self.slidingRow:
                        self.goalX += self.slideDirection
                        self.updateScore("GOAL_SHIFTING")
                    self.slidingRow = None

                elif self.slidingCol != None:
                    shiftColumn(self.tileBoard, self.slidingCol, (self.slideDirection == 1))
                    if self.playerX == self.slidingCol:
                        self.playerY += self.slideDirection
                        self.updateScore("PLAYER_SHIFTING")
                    elif self.goalX == self.slidingCol:
                        self.goalY += self.slideDirection
                        self.updateScore("GOAL_SHIFTING")
                    self.slidingCol = None

    def handleEvents(self, events):
        if (self.countdown <= 0):
            return GameOverScene(self.scoreTracker)

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
                        if (self.goalY == row and self.goalX == 4):
                            continue
                        self.slidingRow = row
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif x > 5*96 and x < 5*96+SBSS and not (self.playerY == row and self.playerX == 0): #left shift arrows
                        if (self.goalY == row and self.goalX == 0):
                            continue
                        self.slidingRow = row
                        self.slideOffset = -1
                        self.slideDirection = -1

                if x > 0 and x < 5*96:
                    column = x // 96
                    if y > -SBSS and y < 0 and not (self.playerX == column and self.playerY == 4): #down shift arrows
                        if (self.goalX == column and self.goalY == 4):
                            continue
                        self.slidingCol = column
                        self.slideOffset = 1
                        self.slideDirection = 1
                    elif y > 5*96 and y < 5*96+SBSS and not (self.playerX == column and self.playerY == 0): #up shift arrows
                        if (self.goalX == column and self.goalY == 0):
                            continue
                        self.slidingCol = column
                        self.slideOffset = -1
                        self.slideDirection = -1

                if x > 0 and x < 5*96 and y > 0 and y < 5*96:
                    row = y // 96
                    column = x // 96
                    start = (self.playerY, self.playerX)
                    end = (row, column)
                    self.movingRoute = findRoute(self.tileBoard, start, end)
                    if self.movingRoute != None:
                        goalLoc = (self.goalY, self.goalX)
                        if goalLoc in self.movingRoute:
                            goalRouteIndex = self.movingRoute.index(goalLoc)
                            self.movingRoute = self.movingRoute[:goalRouteIndex+1]

    def draw(self, screen):
        screen.fill(config.green3)

        screen.blit(self.countdownImg, self.countdownImgRect)

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


class GameOverScene(Scene):
    def __init__(self, scoreTracker):
        super().__init__()

        gameoverFont = pygame.font.Font("assets/Early GameBoy.ttf", 74)
        self.gameoverText = gameoverFont.render("Game Over", True, config.green4)
        self.gameoverTextRect = self.gameoverText.get_rect(center=(400, 200))

        score = self.calculateScore(scoreTracker)
        scoreText = "score: {0}".format(score)
        scoreFont = pygame.font.Font("assets/Early GameBoy.ttf", 32)
        self.scoreText = scoreFont.render(scoreText, True, config.green4)
        self.scoreTextRect = self.scoreText.get_rect(center=(400, 400))

        startFont = pygame.font.Font("assets/Early GameBoy.ttf", 20)
        self.playAgainText = startFont.render("Press SPACE To Play Again!", True, config.green4)
        self.playAgainTextRect = self.playAgainText.get_rect(center=(400, 500))

    def calculateScore(self, scoreTracker):
        score = 0
        for scoreMod in scoreTracker:
            score += config.scores[scoreMod] * scoreTracker[scoreMod]
        return score

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return GamePlay()

    def draw(self, screen):
        screen.fill(config.green3)
        screen.blit(self.gameoverText, self.gameoverTextRect)
        screen.blit(self.scoreText, self.scoreTextRect)
        screen.blit(self.playAgainText, self.playAgainTextRect)
