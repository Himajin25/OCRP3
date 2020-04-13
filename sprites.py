import pygame as pg
import sys
from os import path
from settings import *
from game import *

""" In this file all game sprites are created and configured, these include:
- walls in Wall Class: static sprites that cannot be crossed
- items in Treasure Class: static sprites that can be collected
- guardian in Mob Class: static sprite 
- player in Player Class: dynamic sprite that can be moved by user and interact with other sprites
"""

# SPRITES
# spritesheet


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (TILESIZE, TILESIZE))
        return image


class Player(pg.sprite.Sprite):
    # this is the player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def move(self, dx=0, dy=0):
        # method allowing for player movement
        if not self.collision_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collision_walls(self, dx, dy):
        # method configuring behavior when colliding with wall sprites
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


class Wall(pg.sprite.Sprite):
    # this is the class configuring the walls
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image(80, 220, 20, 20)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mob(pg.sprite.Sprite):
    # this is the class configuring the guardian
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Treasure(pg.sprite.Sprite):
    # this is the class configuring items
    def __init__(self, game, image, x, y):
        self.groups = game.all_sprites, game.treasures
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
