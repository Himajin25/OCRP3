import pygame as pg
import sys
from os import path
from settings import *
from game import *


#SPRITES
#spritesheet
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image (self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (TILESIZE, TILESIZE))
        return image

#macguyver 
class Player(pg.sprite.Sprite):
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

#macguyver movement
    def move(self, dx=0, dy=0): 
        if not self.collideWithWalls(dx, dy):
            self.x += dx
            self.y += dy
#macguyver collisions
    def collideWithWalls(self, dx, dy):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False



#walls of maze    
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x , y):
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

#removal af treasure post capture
    def gotTreasure(self):
        #calculate distance between player and treasure
        self.collect = pg.sprite.spritecollide(self.player, self.treasures, False)
        for treasure in self.treasloc:
            if self.collect:
                self.treasloc.pop("treasure")
                print(self.treasloc)
    