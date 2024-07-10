import pygame
import config

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
        tileset = pygame.image.load("assets/fantasy-tileset.png")
        cutoutTileRect = pygame.Rect(64, 32, 32, 32)
        self.cutoutTileIMG = tileset.subsurface(cutoutTileRect)

    def update(self):
        pass

    def handleEvents(self, events):
        pass

    def draw(self, screen):
        screen.fill(config.green2)
        xOffset = 160
        yOffset = 60
        for x in range(15):
            for y in range(15):
                screen.blit(self.cutoutTileIMG, (xOffset+x*32, yOffset+y*32))
