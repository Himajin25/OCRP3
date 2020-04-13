import pygame as pg
from settings import *

""" In this file we configure the game maze;
- layout is imported from external text file
- text file is converted into a list of its elements and their indexes
- maze dimension is determined by the list size: make sure to fit the screen configuration accordingly
 """


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
