import config

import pygame
import random

def tileGenerator():
    tileset = pygame.image.load("assets/fantasy-tileset.png")
    wallTileRect = pygame.Rect(3*32, 1*32, 32, 32)
    wattTileImg = tileset.subsurface(wallTileRect)
    groundTileRect = pygame.Rect(7*32, 3*32, 32, 32)
    groundTileImg = tileset.subsurface(groundTileRect)

    tiles = []

    tileBase = pygame.Surface((96, 96))
    tileBase.fill(config.green2)


    tileTypeA = tileBase.copy()
    tileTypeA.blit(wattTileImg, (0, 0))
    tileTypeA.blit(wattTileImg, (32, 0))
    tileTypeA.blit(wattTileImg, (64, 0))
    tileTypeA.blit(groundTileImg, (0, 32))
    tileTypeA.blit(groundTileImg, (32, 32))
    tileTypeA.blit(groundTileImg, (64, 32))
    tileTypeA.blit(wattTileImg, (0, 64))
    tileTypeA.blit(wattTileImg, (32, 64))
    tileTypeA.blit(wattTileImg, (64, 64))


    tileTypeB = pygame.transform.rotate(tileTypeA, 90)



    tiles.append(tileTypeA)
    tiles.append(tileTypeB)

    return tiles


def generateTileBoard():
    tileBoard = [None]*25
    for i in range(25):
        tileBoard[i] = random.randint(0, 1)
    return tileBoard
