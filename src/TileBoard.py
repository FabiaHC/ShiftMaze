import config

import pygame
import random

def tileGenerator():
    tileset = pygame.image.load("assets/fantasy-tileset.png")
    wallTileRect = pygame.Rect(3*32, 1*32, 32, 32)
    wallTileImg = tileset.subsurface(wallTileRect)

    groundTileRect = pygame.Rect(7*32, 3*32, 32, 32)
    groundTileImg = tileset.subsurface(groundTileRect)
    groundTileImg.fill(config.green2)

    arrowTileRect = pygame.Rect(4*16, 47*16, 16, 16)
    arrowTileImg = tileset.subsurface(arrowTileRect)


    tiles = {}
    tileBase = pygame.Surface((96, 96))
    tileBase.fill(config.green2)


    straightNSTile = tileBase.copy()
    straightNSTile.blit(wallTileImg, (0, 0))
    straightNSTile.blit(wallTileImg, (32, 0))
    straightNSTile.blit(wallTileImg, (64, 0))
    straightNSTile.blit(groundTileImg, (0, 32))
    straightNSTile.blit(groundTileImg, (32, 32))
    straightNSTile.blit(groundTileImg, (64, 32))
    straightNSTile.blit(wallTileImg, (0, 64))
    straightNSTile.blit(wallTileImg, (32, 64))
    straightNSTile.blit(wallTileImg, (64, 64))

    straightEWTile = straightNSTile.copy()
    straightEWTile.blit(groundTileImg, (32, 0))
    straightEWTile.blit(groundTileImg, (32, 64))
    straightEWTile.blit(wallTileImg, (0, 32))
    straightEWTile.blit(wallTileImg, (64, 32))

    TTileNES = straightNSTile.copy()
    TTileNES.blit(groundTileImg, (0, 32))

    TTileNWS = straightNSTile.copy()
    TTileNWS.blit(groundTileImg, (64, 32))

    TTileNEW = straightEWTile.copy()
    TTileNEW.blit(groundTileImg, (32, 0))

    TTileEWS = straightEWTile.copy()
    TTileEWS.blit(groundTileImg, (32, 64))


    rightArrowTile = pygame.Surface((3*16 + 3*16, 96))
    rightArrowTile.fill(config.green4)
    rightArrowTile.blit(arrowTileImg, (3*16 + 1*16, 1*16))
    rightArrowTile.blit(arrowTileImg, (3*16 + 1*16, 2*16))
    rightArrowTile.blit(arrowTileImg, (3*16 + 1*16, 3*16))
    rightArrowTile.blit(arrowTileImg, (3*16 + 1*16, 4*16))
    pygame.draw.rect(rightArrowTile, config.green1, (3*16, 0, 3*16+3*16, 6*16), 1)
    pygame.draw.rect(rightArrowTile, config.green3, (0, 0, 3*16, 96), 0)

    leftArrowTile = pygame.transform.flip(rightArrowTile, True, False)
    upArrowTile = pygame.transform.rotate(rightArrowTile, 90)
    downArrowTile = pygame.transform.flip(upArrowTile, False, True)


    tiles["straight_ns"] = straightNSTile
    tiles["straight_ew"] = straightEWTile
    tiles["T_nes"] = TTileNES
    tiles["T_nws"] = TTileNWS
    tiles["T_new"] = TTileNEW
    tiles["T_ews"] = TTileEWS
    tiles["leftArrow"] = leftArrowTile
    tiles["rightArrow"] = rightArrowTile
    tiles["downArrow"] = downArrowTile
    tiles["upArrow"] = upArrowTile

    return tiles


def generateTileBoard():
    tileBoard = [[None for _ in range(5)] for _ in range(5)]
    for y in range(5):
        for x in range(5):
            tileBoard[y][x] = random.choice(list(config.tileTypes.keys()))
    return tileBoard

def shiftRow(tileBoard, row, left=True):
    rowList = tileBoard[row]
    tileBoard[row] = rowList[1:] + [rowList[0]] if left else [rowList[-1]] + rowList[:-1]

def shiftColumn(tileBoard, column, down=True):
    if down:
        lastValue = tileBoard[-1][column]  #save the last value of the column
        for row in range(4, 0, -1):
            tileBoard[row][column] = tileBoard[row - 1][column]
        tileBoard[0][column] = lastValue
    else:
        firstValue = tileBoard[0][column]  #save the first value of the column
        for row in range(4):
            tileBoard[row][column] = tileBoard[row + 1][column]
        tileBoard[-1][column] = firstValue
