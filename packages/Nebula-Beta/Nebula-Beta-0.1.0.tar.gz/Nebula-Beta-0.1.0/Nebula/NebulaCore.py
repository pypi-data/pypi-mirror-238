import time, datetime, pytz,re, math, pygame, pygame_gui, random, copy, sys, json, os, pygame.gfxdraw, pygame.freetype, platform, subprocess
from csv import reader
from pygame.locals import *
from functools import partial
from collections import deque
from dataclasses import dataclass
from os import walk, sep, listdir
from screeninfo import get_monitors
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer

pygame.init()
PYRECT = pygame.Rect
VECTOR2 = pygame.math.Vector2
PYSURFACE = pygame.Surface
SCALE = pygame.transform.scale
FLIPTRANSFORM = pygame.transform.flip
ROTTRANSFORM = pygame.transform.rotate

""" DECORATORS """
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"\n~|\tEntering {func.__name__}")
        result = func(*args, **kwargs)
        print(f"\n~|\tExiting {func.__name__}")
        return result
    return wrapper


def logDebugReturn(func, path:str="C:\\.NebulaLog\\nebula.log"):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(path, 'a') as log:
            log.write(f"\n~|\tFunction {func.__name__} returned:\n{result}\n")
            log.close()
        return result
    return wrapper


def outDebugReturn(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"\n~| Function {func.__name__} returned:\n{result}\n")
        return result
    return wrapper


def profile_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n~|\tEXECUTION PROFILER\n________\nMETHOD: {func.__name__} | TIME: {end_time - start_time:.3f}s\n")
        return result
    return wrapper


""" STAND-ALONES """
def naturalKey(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def cLoadAssets(path: str, tileSize: int) -> list:
    surface = loadAsset(path)
    tileNumX = int(surface.get_size()[0] / tileSize)
    tileNumY = int(surface.get_size()[1] / tileSize)

    cutAssets = []
    for row in range(tileNumY):
        for col in range(tileNumX):
            x = col * tileSize
            y = row * tileSize
            newSurf = PYSURFACE((tileSize, tileSize), flags=pygame.SRCALPHA).convert_alpha()
            newSurf.blit(surface, (0, 0), PYRECT(x, y, tileSize, tileSize))
            cutAssets.append(newSurf)

    return cutAssets


def genAnimationLib(animationKeys: list) -> dict:
    """
    Generate a new animation library.
    """
    return {key: None for key in animationKeys}


_text_library = {}
def drawText(surf, ttf_path:str, text:str, position:VECTOR2=VECTOR2, size:int=30, color:list|tuple=(255,255,255), bg_color=None, center=True):
    global _text_library
    text_surf = _text_library.get(f"{text}{color}{size}")
    if text_surf is None:
        font = pygame.font.Font(ttf_path, size)
        # font = pygame.font.Font('assets/ui/font/minotaur.ttf', size)
        text_surf = font.render(text, True, color, bg_color)
        _text_library[f"{text}{color}{size}"] = text_surf
    x, y = position
    if center:
        surf.blit(text_surf, (x - (text_surf.get_width() // 2), y - (text_surf.get_height() // 2)))
    else:
        surf.blit(text_surf, (x, y))


def distTo(originVector, targetVector) -> pygame.math.Vector2:
    """
    Calculate the distance between the origin and the target vector along both the x and y axes.
    """
    deltaX = targetVector.x - originVector.x
    deltaY = targetVector.y - originVector.y
    return pygame.math.Vector2((deltaX), (deltaY))


def clamp(num: int, minValue: int, maxValue: int) -> int:
    """ Returns the number you input as long as its between the max and min values. """
    return max(min(num, maxValue), minValue)


_imageLibrary = {}
def loadAsset(path: str) -> pygame.Surface:
    global _imageLibrary
    image = _imageLibrary.get(path)
    if image == None:
        canonicalizedPath = path.replace('/', sep).replace('\\', sep)
        image = pygame.image.load(canonicalizedPath).convert_alpha()
        _imageLibrary[path] = image
    return image


def genLightGradient(radius=1, color=[55,55,55], intensity=1, stepRadius=1, alpha=1) -> pygame.Surface:
    # make a surface the size of the largest circle's diameter (radius * 2)
    surface = PYSURFACE((int(radius) * 2, int(radius) * 2), pygame.SRCALPHA)
    surface.convert_alpha()

    currentRadius = radius
    circleCount = radius // stepRadius

    # for every circle in circleCount
    for layer in range(circleCount):

        # create a new surface for the new circle (same size as original)
        layerSurface = PYSURFACE((int(radius) * 2, int(radius) * 2), pygame.SRCALPHA)
        layerSurface.convert_alpha()
        layerSurface.set_alpha(alpha)

        # draw the new circle on the new surface using the currentRadius
        pygame.draw.circle(layerSurface, [intensity * value for value in color], (radius, radius), currentRadius, width=5)  # width determines how much each circle overlaps each other

        # blit the circle layer onto the main surface
        surface.blit(layerSurface, (0, 0))

        # update the currentRadius and alpha for the next circle layer
        currentRadius -= stepRadius
        alpha += 1

    # return the main surface that has all the circle layers drawn on it
    return surface


def loadAssetDir(path: str) -> list:
    surfaceList = []
    for _, __, imageFiles in walk(path):
        sortedFiles = sorted(imageFiles, key=naturalKey)
        for image in sortedFiles:
            fullPath = path + '/' + image
            imageSurface = loadAsset(fullPath)
            surfaceList.append(imageSurface)

    return surfaceList


def loadAssetDirNum(path: str) -> list:
    surfaceList = []
    fileList = []
    for _, __, imageFiles in walk(path):
        for index, image in enumerate(imageFiles):
            fileList.append(image)

        # sort images based on numerical values in the image names: run1.png will always come before run12.png as walk doesnt sort files returned.
        fileList.sort(key=lambda image: int(
            ''.join(filter(str.isdigit, image))))

        for index, image in enumerate(fileList):
            fullPath = path + '/' + image
            imageSurface = loadAsset(fullPath).convert_alpha()
            imageSurface.set_colorkey([0, 0, 0])
            surfaceList.append(imageSurface)

    return surfaceList


def scaleImages(images: list, size: tuple) -> list:
    """ returns scaled image assets """
    scaled_images = []
    for image in images:
        scaled_images.append(pygame.transform.scale(image, size))
    return scaled_images


def sineWaveValue() -> int:
    value = math.sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0


def loadCFG(path:str=__file__, name:str=__name__) -> list:
    _cfg_path = path
    _cfg_path = _cfg_path.removesuffix("\\"+name+".py")
    _cfg_path += "\\.ncfg"
    with open(_cfg_path, "r") as cfgFile:
        return json.load(cfgFile)
    cfgFile.close()


