
import pygame as pg
import sys
from os import path
from game import *
from sprites import *
from settings import *


g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()