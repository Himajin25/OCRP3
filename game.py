import pygame as pg
import random as rd
import sys
from os import path
from settings import *
from sprites import *
from maps import *


#GAME
#basic game config
class Game:
    def __init__(self):
        #initialize screen an settings
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 50)
        self.running = True
        self.load_data()
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = Map(path.join(map_folder, "map1.txt"))
        #treasures_files = path.join(img_folder, "seringue.png", "needle.png", "tube.png")
        #self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        #self.map_img = self.map.make_map()
        #self.map.rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        #self.treasure_img = pg.image.load(path.join(img_folder, SERINGUE_IMG, NEEDLE_IMG, TUBE_IMG)).convert_alpha()
        self.seringue_img = pg.image.load(path.join(img_folder, SERINGUE_IMG)).convert()
        self.seringue_img = pg.transform.scale(self.seringue_img, (TILESIZE, TILESIZE))
        self.seringue_img.set_colorkey(WHITE)
        self.needle_img = pg.image.load(path.join(img_folder, NEEDLE_IMG)).convert_alpha()
        self.needle_img = pg.transform.scale(self.needle_img, (TILESIZE, TILESIZE))
        #return self.needle_img
        self.tube_img = pg.image.load(path.join(img_folder, TUBE_IMG)).convert()
        self.tube_img = pg.transform.scale(self.tube_img, (TILESIZE, TILESIZE))
        self.tube_img.set_colorkey(WHITE)
        #self.treasures_img = [self.seringue_img, self.needle_img, self.tube_img]
        #self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
#game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
#new game/game reset 
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.treasures = pg.sprite.Group()
        self.free = []
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "#":
                    Wall(self, col, row)
                    #print(x,y)
                if tile == "P":
                    self.player = Player(self, col, row)
                    #print(x,y)
                if tile == "M":
                    self.mob = Mob(self, col, row)
                    #print(x,y)
                if tile == "_":
                    self.treasok = col, row
                    self.free.append(self.treasok)
        print(self.free)
        self.treascoo = rd.sample(self.free, 3)
        print(self.treascoo)
        self.treaslist = ["seringue", "needle", "tube"]

        self.treasloc = {k:v for k, v in zip(self.treaslist, self.treascoo)}
        print(self.treasloc)
        

        self.seringue = Treasure(self, self.seringue_img, self.treasloc["seringue"][0], self.treasloc["seringue"][1])
        self.needle = Treasure(self, self.needle_img, self.treasloc["needle"][0], self.treasloc["needle"][1])
        self.tube = Treasure(self, self.tube_img, self.treasloc["tube"][0], self.treasloc["tube"][1])
        

                
        self.run()
        
#game update
    def update(self):
        self.all_sprites.update()
        self.collect = pg.sprite.spritecollide(self.player, self.treasures, True)
        self.end = pg.sprite.spritecollide(self.player, self.mobs, False)
        
        if self.collect:
            for key, value in self.treasloc.items():
                if value == (self.player.x, self.player.y):
                    del self.treasloc[key]
                    print("treasure collected")
                    print(self.treasloc)
                    return self.treasloc
                print(self.treasloc) 
        if self.end:
            if len(self.treasloc) == 0:
                print("you win")
                pg.quit()
            else:
                if len(self.treasloc) > 0:
                    print("you shall not pass")
        
        

#game inputs        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if event.key == pg.K_UP: 
                    self.player.move(dy=-1)

#game 15*15 grid, 32px            
    def draw_grid(self):
        for x in range (0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
                

#game rendering
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        
#game end
    def quit(self):
        pg.quit()


# creation of game object
g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()
