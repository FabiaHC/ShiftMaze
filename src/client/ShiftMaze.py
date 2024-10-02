from SceneSystem import MainMenu
from GameUtils import loadMutedState

import pygame


def setMuted(muted):    #mute or unmute the BGM
    pygame.mixer.music.set_volume(0 if muted else 1)


def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    pygame.mixer.music.load("assets//Memoraphile - Spooky Dungeon.ogg")
    muted = loadMutedState()
    if muted:
        setMuted(muted)

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    currentScene = MainMenu()
    running = True

    pygame.mixer.music.play(loops=-1)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    muted = not muted
                    setMuted(muted)

        # update scene
        changeScene = currentScene.handleEvents(events)
        if changeScene:
            currentScene = changeScene
        currentScene.update()
        currentScene.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
