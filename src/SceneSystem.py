import pygame

class Scene:
    def __init__(self):
        pass

    def update(self):
        pass

    def handleEvents(self):
        pass

    def draw(self, screen):
        pass


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        gameboyFont = pygame.font.Font("assets/Early GameBoy.ttf", 74)
        self.titleText = gameboyFont.render("ShiftMaze", True, (32, 70, 49))
        self.titleTextRect = self.titleText.get_rect(center=(400, 300))


    def update(self):
        pass

    def handleEvents(self):
        pass

    def draw(self, screen):
        screen.fill((174, 196, 64))
        screen.blit(self.titleText, self.titleTextRect)
