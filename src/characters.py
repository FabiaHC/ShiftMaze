import pygame

def loadPlayerImgs():
    assetDir = "assets/gb-mini-pixel-world/"
    playerImgs = {}

    playerImgs["right"] = []
    playerImgs["left"] = []
    playerImgs["down"] = []
    playerImgs["up"] = []

    for direction in playerImgs:
        for i in range(1, 3):
            img = pygame.image.load("{0}pc-walk-{1}{2}.png".format(assetDir, direction, i))
            upscaledImg = pygame.transform.scale2x(img)
            playerImgs[direction].append(upscaledImg)

    return playerImgs
