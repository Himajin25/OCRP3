import pygame as pg
import random as rd
import sys
from os import path
from settings import *
from sprites import *
from maps import *

""" In this file, basic game configuration is coded through Game Class creation
    making use of Pygame's 3 steps process:
    Step 1= Process Input where user can input commands
    Step 2= Game update where inputs are registered by pygame
    Step 3= Rendering where pygame makes changes visible through blitting/ drawing
    (step 4= Timekeeping where length of each iteration through the game loop is configured)
    Steps are initiated through methods of the Game class
    """


# basic game config
class Game:
    def __init__(self):
        """ Initialize screen and general game settings """
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 50)
        self.running = True
        self.load_data()

    def load_data(self):
        """ Configuration of all assets to make them usable in game """
        # set up assets folders
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = Map(path.join(map_folder, "map1.txt"))
        # load assets images and assign to different sprites
        # convert them to game specific requirements
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.player_img = pg.image.load(
            path.join(img_folder, PLAYER_IMG)).convert_alpha()  # "".convert" makes img easy to manipulate by pygame(speed and bugs)
        self.player_img = pg.transform.scale(
            self.player_img, (TILESIZE, TILESIZE))
        self.mob_img = pg.image.load(
            path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.seringue_img = pg.image.load(
            path.join(img_folder, SERINGUE_IMG)).convert()
        self.seringue_img = pg.transform.scale(
            self.seringue_img, (TILESIZE, TILESIZE))
        self.seringue_img.set_colorkey(WHITE)
        self.needle_img = pg.image.load(
            path.join(img_folder, NEEDLE_IMG)).convert_alpha()
        self.needle_img = pg.transform.scale(
            self.needle_img, (TILESIZE, TILESIZE))
        self.tube_img = pg.image.load(
            path.join(img_folder, TUBE_IMG)).convert()
        self.tube_img = pg.transform.scale(self.tube_img, (TILESIZE, TILESIZE))
        # "colorkey" tells pygame which part of img to make transparent
        self.tube_img.set_colorkey(WHITE)

# new game/game reset
    def new(self):
        """ Method starting new game and configuring all game elements generated every game initialization 
        these include:
        - sprites and their groups
        - the maze, it's elements and their position
        - the run method
        """
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.treasures = pg.sprite.Group()
        self.free_tiles = []    # empty list to store tiles coordinates from map.txt file
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # extract index and items from list
                if tile == "#":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "M":
                    self.mob = Mob(self, col, row)
                if tile == "_":
                    self.empty_tile = col, row
                    self.free_tiles.append(self.empty_tile)

        # list of coordinates from randomly selected free tiles
        self.random_free_tiles = rd.sample(self.free_tiles, 3)
        self.items = ["seringue", "needle", "tube"]   # collectable items
        self.item_loc = {k: v for k, v in zip(
            self.items, self.random_free_tiles)}   # dict coupling items with coordinates
        self.seringue = Treasure(
            self, self.seringue_img, self.item_loc["seringue"][0], self.item_loc["seringue"][1])
        self.needle = Treasure(
            self, self.needle_img, self.item_loc["needle"][0], self.item_loc["needle"][1])
        self.tube = Treasure(
            self, self.tube_img, self.item_loc["tube"][0], self.item_loc["tube"][1])

        self.run()

    def events(self):
        """ Method allowing for user to interact with game
        game loop "event" section
        allows for moving Player around maze;
        allows for quitting game through closure of game window
        """
        # game loop update section
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

    def update(self):
        """ Method updating game after inputs ;
        - updates all sprites
        - accounts for items collection
        - accounts for face-off with guardian
        """
        self.all_sprites.update()

        self.items_collection = pg.sprite.spritecollide(
            self.player, self.treasures, True)    # items colletcion
        if self.items_collection:
            # remove item from dict when collected by player
            for key, value in self.item_loc.items():
                if value == (self.player.x, self.player.y):
                    del self.item_loc[key]
                    print("treasure collected")
                    print(self.item_loc)
                    return self.item_loc

        self.face_guardian = pg.sprite.spritecollide(
            self.player, self.mobs, False)   # face-off with guardian
        if self.face_guardian:
            # check if dict is empty when player faces guardian. if empty, player clears game
            if len(self.item_loc) == 0:
                print("you win")
                self.quit()
            else:
                if len(self.item_loc) > 0:
                    print("you shall not pass")

    def draw_grid(self):
        """ Method for drawing a grid on the screen """
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        """ Method for drawing/blitting updated game on to screen and flipping it, game loop draw section """
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # after drawing everything, flip display
        pg.display.flip()

    def run(self):
        """ Method for running the actual game loop with all 3 steps """
        self.playing = True  # create variable to define whether we are playing or not
        while self.playing:
            # keep track of time
            self.clock.tick(FPS)
            # keep track of process inputs
            self.events()
            # keep track of what each sprite needs to do
            self.update()
            # draw game elements onto screen
            self.draw()

    def quit(self):
        """ Method for exiting the game """
        sys.exit()
        pg.quit()
