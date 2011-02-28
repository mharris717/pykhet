#!/usr/bin/env python

import pygame, sys, os
from pygame.locals import *

#loads an image
def load_image(name, colorkey=None):
    fullname = os.path.join('images',name)
    try:
            image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert() 
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

#Game class
class Game():

    def __init__(self):
        self.pieces = [\
        [ 0, 0, 0, 0, 8, 9, 8, 2, 0, 0],\
        [ 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],\
        [ 0, 0, 0,14, 0, 0, 0, 0, 0, 0],\
        [ 1, 0,13, 0, 5, 6, 0, 2, 0,14],\
        [ 2, 0,14, 0,15,16, 0, 1, 0,13],\
        [ 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],\
        [ 0, 0, 0, 0, 0, 0, 0,11, 0, 0],\
        [ 0, 0,14,18,19,18, 0, 0, 0, 0]\
        ]\
        
        self.red_pyramid = load_image('red_pyramid.bmp')
        self.red_djed = load_image('red_djed.bmp')
        self.red_obelisk = load_image('red_obelisk.bmp')
        self.red_obelisk2x = load_image('red_obelisk2x.bmp')
        self.red_pharaoh = load_image('red_pharaoh.bmp',-1)
        self.grey_pyramid = load_image('grey_pyramid.bmp')
        self.grey_djed = load_image('grey_djed.bmp')
        self.grey_obelisk = load_image('grey_obelisk.bmp')
        self.grey_obelisk2x = load_image('grey_obelisk2x.bmp')
        self.grey_pharaoh = load_image('grey_pharaoh.bmp',-1)

        screen = pygame.display.get_surface()

        
    def draw_pieces(self,surface):
        for y in range(8):
            for x in range(10):
                if self.pieces[y][x] == 1:
                    surface.blit(self.red_pyramid,(x*50,y*50))
                elif self.pieces[y][x] == 2:
                    surface.blit(pygame.transform.flip(self.red_pyramid,0,1),(x*50,y*50))
                elif self.pieces[y][x] == 3:
                    surface.blit(pygame.transform.flip(self.red_pyramid,1,1),(x*50,y*50))
                elif self.pieces[y][x] == 4:
                    surface.blit(pygame.transform.flip(self.red_pyramid,1,0),(x*50,y*50))
                elif self.pieces[y][x] == 5:
                    surface.blit(self.red_djed,(x*50,y*50))
                elif self.pieces[y][x] == 6:
                    surface.blit(pygame.transform.flip(self.red_djed,0,1),(x*50,y*50))
                elif self.pieces[y][x] == 7:
                    surface.blit(self.red_obelisk,(x*50,y*50))
                elif self.pieces[y][x] == 8:
                    surface.blit(self.red_obelisk2x,(x*50,y*50))
                elif self.pieces[y][x] == 9:
                    surface.blit(self.red_pharaoh,(x*50,y*50))
                elif self.pieces[y][x] == 11:
                    surface.blit(self.grey_pyramid,(x*50,y*50))
                elif self.pieces[y][x] == 12:
                    surface.blit(pygame.transform.flip(self.grey_pyramid,0,1),(x*50,y*50))
                elif self.pieces[y][x] == 13:
                    surface.blit(pygame.transform.flip(self.grey_pyramid,1,1),(x*50,y*50))
                elif self.pieces[y][x] == 14:
                    surface.blit(pygame.transform.flip(self.grey_pyramid,1,0),(x*50,y*50))
                elif self.pieces[y][x] == 15:
                    surface.blit(self.grey_djed,(x*50,y*50))
                elif self.pieces[y][x] == 16:
                    surface.blit(pygame.transform.flip(self.grey_djed,0,1),(x*50,y*50))
                elif self.pieces[y][x] == 17:
                    surface.blit(self.grey_obelisk,(x*50,y*50))
                elif self.pieces[y][x] == 18:
                    surface.blit(self.grey_obelisk2x,(x*50,y*50))
                elif self.pieces[y][x] == 19:
                    surface.blit(self.grey_pharaoh,(x*50,y*50))


#main function
def main():
    #setup
    pygame.init()
    screen = pygame.display.set_mode((500,400))
    pygame.display.set_caption('pyKhet')
    clock = pygame.time.Clock()
    
    #setup board
    board = [\
    [01,02,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,00,02],\
    [01,00,00,00,00,00,00,00,01,02]\
    ]\

    #setup and draw board
    black_tile = load_image('black_tile.bmp')
    grey_tile = load_image('grey_tile.bmp')
    red_tile = load_image('red_tile.bmp')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    game = Game()
	
    for y in range(8):
        for x in range(10):
            if board[y][x] == 0:
                background.blit(black_tile,(x*50,y*50))
            elif board[y][x] == 1:
                background.blit(red_tile,(x*50,y*50))
            elif board[y][x] == 2:
                background.blit(grey_tile,(x*50,y*50))            
    screen.blit(background,(0,0))
    game.draw_pieces(screen)
    pygame.display.flip()
    
    going = True
    while going:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

#call main loop
main()

