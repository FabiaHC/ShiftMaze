import json
import numpy as np
import pygame

def replaceColours(surface, colourMap):
    for oldColour, newColour in colourMap.items():
        arr = pygame.PixelArray(surface)
        arr.replace(oldColour, newColour)
        del arr

def loadURL():
    filepath = "RuntimeConfig.json"
    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
        url = config.get('server_url', None)
        return url

    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        return None
