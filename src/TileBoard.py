import config

import pygame
import random

def tileGenerator():
    tileset = pygame.image.load("assets/fantasy-tileset.png")
    wallTileRect = pygame.Rect(3*32, 1*32, 32, 32)
    wallTileImg = tileset.subsurface(wallTileRect)
    groundTileRect = pygame.Rect(7*32, 3*32, 32, 32)
    groundTileImg = tileset.subsurface(groundTileRect)

    tiles = []

    tileBase = pygame.Surface((96, 96))
    tileBase.fill(config.green2)


    tileTypeA = tileBase.copy()
    tileTypeA.blit(wallTileImg, (0, 0))
    tileTypeA.blit(wallTileImg, (32, 0))
    tileTypeA.blit(wallTileImg, (64, 0))
    tileTypeA.blit(groundTileImg, (0, 32))
    tileTypeA.blit(groundTileImg, (32, 32))
    tileTypeA.blit(groundTileImg, (64, 32))
    tileTypeA.blit(wallTileImg, (0, 64))
    tileTypeA.blit(wallTileImg, (32, 64))
    tileTypeA.blit(wallTileImg, (64, 64))

    tileTypeB = tileTypeA.copy()
    tileTypeA.blit(groundTileImg, (32, 0))
    tileTypeA.blit(groundTileImg, (32, 64))
    tileTypeA.blit(wallTileImg, (0, 32))
    tileTypeA.blit(wallTileImg, (64, 32))

    tileTypeC = tileTypeA.copy()
    tileTypeC.blit(groundTileImg, (0, 32))

    tileTypeD = tileTypeA.copy()
    tileTypeD.blit(groundTileImg, (64, 32))

    tileTypeE = tileTypeB.copy()
    tileTypeE.blit(groundTileImg, (32, 0))

    tileTypeF = tileTypeB.copy()
    tileTypeF.blit(groundTileImg, (32, 64))

    tiles.append(tileTypeA)
    tiles.append(tileTypeB)
    tiles.append(tileTypeC)
    tiles.append(tileTypeD)
    tiles.append(tileTypeE)
    tiles.append(tileTypeF)

    return tiles


def generateTileBoard():
    tileBoard = [[None for _ in range(5)] for _ in range(5)]
    for y in range(5):
        for x in range(5):
            tileBoard[y][x] = random.randint(0, 5)
    return tileBoard
