
import pygame as pg
import sys
from os import path
from game import *
from sprites import *
from settings import *
""" This is the main loop to run the game """

# create instance of game object
g = Game()

while g.running:
    g.new()  # start a new game

pg.quit()
