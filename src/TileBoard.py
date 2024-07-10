import config

import pygame

def tileGenerator():
    tileset = pygame.image.load("assets/fantasy-tileset.png")
    cutoutTileRect = pygame.Rect(64, 32, 32, 32)
    cutoutTileIMG = tileset.subsurface(cutoutTileRect)

    tiles = []

    tileBase = pygame.Surface((96, 96))
    tileBase.fill(config.green2)

    tileTypeA = tileBase.copy()
    tileTypeA.blit(cutoutTileIMG, (0, 0))
    tileTypeA.blit(cutoutTileIMG, (32, 0))
    tileTypeA.blit(cutoutTileIMG, (64, 0))
    tileTypeA.blit(cutoutTileIMG, (0, 64))
    tileTypeA.blit(cutoutTileIMG, (32, 64))
    tileTypeA.blit(cutoutTileIMG, (64, 64))

    tileTypeB = pygame.transform.rotate(tileTypeA, 90)

    tiles.append(tileTypeA)
    tiles.append(tileTypeB)

    return tiles
