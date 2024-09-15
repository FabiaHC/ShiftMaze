import numpy as np
import pygame

def replaceColours(surface, colourMap):
    for oldColour, newColour in colourMap.items():
        arr = pygame.PixelArray(surface)
        arr.replace(oldColour, newColour)
        del arr
