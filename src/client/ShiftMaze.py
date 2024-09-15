from SceneSystem import MainMenu

import pygame


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    currentScene = MainMenu()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

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
