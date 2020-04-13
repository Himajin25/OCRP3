import pygame as pg
import sys
from os import path

""" Game options are stored in this file in constants which allows for easy tweaks without touching the code """

# basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)


# screen settings
WIDTH = 480
HEIGHT = 480
TITLE = "P3 MacGuyver"
BGCOLOR = LIGHTGREY
TILESIZE = 32
TILEWIDTH = WIDTH / TILESIZE
TILEHEIGHT = HEIGHT / TILESIZE

# game framerate
FPS = 30

# assets images
PLAYER_IMG = "MacGyver.png"   # player image
MOB_IMG = "Gardien.png"     # guardian image
SERINGUE_IMG = "seringue.png"   # item image
NEEDLE_IMG = "needle.png"   # item image
TUBE_IMG = "tube.png"  # item image
SPRITESHEET = "floor-tiles-20x20.png"   # floor and wall images
