import pygame as pg
import sys
from os import path


#SETTINGS
#some basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)


#game settings
WIDTH = 480
HEIGHT = 480
FPS = 30

TITLE = "P3 MacGuyver"
BGCOLOR = LIGHTGREY
TILESIZE = 32
TILEWIDTH = WIDTH / TILESIZE
TILEHEIGHT = HEIGHT / TILESIZE

#player settings
PLAYER_IMG = "MacGyver.png"

#mob settings
MOB_IMG = "Gardien.png"

#tresure settings
SERINGUE_IMG = "seringue.png"
NEEDLE_IMG = "needle.png"
TUBE_IMG = "tube.png"

SPRITESHEET = "floor-tiles-20x20.png"