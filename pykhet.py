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

    for y in range(8):
        for x in range(10):
            if board[y][x] == 0:
                background.blit(black_tile,(x*50,y*50))
            elif board[y][x] == 1:
                background.blit(grey_tile,(x*50,y*50))
            elif board[y][x] == 2:
                background.blit(red_tile,(x*50,y*50))            
    screen.blit(background,(0,0))
    pygame.display.flip()
    
    going = True
    while going:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False

#call main loop
main()

