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
    if "png" in name:
        image = image.convert_alpha()
    else:
        image = image.convert() 
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

#player class
class Player():
    
    def __init__(self):
    	self.cursor=None
    	self.x = 0
    	self.y = 0
    	self.action = None
    	self.color = None
    
    def draw_cursor(self,surface):
        surface.blit(self.cursor,(self.x*50,self.y*50))
    	

#Game class
class Game():

    def __init__(self):
        self.pieces = [\
        [ 0, 0, 0, 0, 8, 9, 8, 2, 0, 0],\
        [ 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],\
        [ 0, 0, 0,14, 0, 0, 0, 0, 0, 0],\
        [ 1, 0,13, 0, 5, 6, 0, 2, 0,14],\
        [ 2, 0,14, 0,16,15, 0, 1, 0,13],\
        [ 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],\
        [ 0, 0, 0, 0, 0, 0, 0,11, 0, 0],\
        [ 0, 0,14,18,19,18, 0, 0, 0, 0]\
        ]\
        
        self.laser = load_image('laser.png')
        self.laser_hit = load_image('laser_hit.png')
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
    
    def rotate_piece(self, x, y):
        rotateable_pieces = [1,2,3,4,5,6,11,12,13,14,15,16]
        if self.pieces[y][x] in rotateable_pieces:
            piece = self.pieces[y][x]
            if piece == 4:
                piece = 1
            elif piece == 6:
                piece = 5
            elif piece == 14:
                piece = 11
            elif piece == 16:
                piece = 15
            else:
                piece = piece+1
            
            self.pieces[y][x] = piece
            
            return True
        else:
            return False

    def legal_select(self, color, x, y):
        legal_pieces = None
        if color == 'red':
            legal_pieces=[1,2,3,4,5,6,7,8,9]
        elif color == 'grey':
            legal_pieces=[11,12,13,14,15,16,17,18,19]
        piece = self.pieces[y][x]
        
        return piece in legal_pieces    
    
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
    
    def fire_laser(self,color,surface):
        startx = 0
        starty = 0
    	dir = '' 	
    	if color is 'red':
    	    startx = 0
    	    starty = 0
    	    dir = 'down'
    	elif color is 'grey':
    	    startx = 9
    	    starty = 7
    	    dir = 'up'
    	
    	laserx = startx
    	lasery = starty
    	
    	firing = True
    	
    	while firing:
    	    hit = 0
    	    pygame.display.flip()
    	    pygame.time.wait(100)
    	    if dir is 'down':
    	        if lasery+1 <= 8:
    	            if self.pieces[lasery][laserx] == 0:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        lasery = lasery+1
                    else:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        hit = 1
                else:
                    firing=False
                    
                if hit == 1:
                    right = [1,11,5,15]
                    left = [4,14,6,16]
                    destroy = [2,3,7,8,9,12,13,17,18,19]
                    piece = self.pieces[lasery][laserx]
                    if piece in right:
                        dir = 'right'
                        laserx=laserx+1
                    elif piece in left:
                        dir = 'left'
                        laserx=laserx-1
                    elif piece in destroy:
                        firing = False
                        if piece not in (8,18):
                            self.pieces[lasery][laserx]=0
                        else:
                            if piece == 8:
                                self.pieces[lasery][laserx]=7
                            if piece == 18:
                                self.pieces[lasery][laserx]=17
                        surface.blit(self.laser_hit,(laserx*50,lasery*50))
    	    elif dir is 'right':
    	        if laserx+1 <= 10:
    	            if self.pieces[lasery][laserx] == 0:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        laserx=laserx+1
                    else:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        hit = 1
                else:
                    firing=False
                    
                if hit == 1:
                    up = [4,6,14,16]
                    down = [3,5,13,15]
                    destroy = [1,2,7,8,9,11,12,17,18,19]
                    piece = self.pieces[lasery][laserx]
                    if piece in up:
                        dir = 'up'
                        lasery=lasery-1
                    elif piece in down:
                        dir = 'down'
                        lasery=lasery+1
                    elif piece in destroy:
                        firing = False
                        if piece not in (8,18):
                            self.pieces[lasery][laserx]=0
                        else:
                            if piece == 8:
                                self.pieces[lasery][laserx]=7
                            if piece == 18:
                                self.pieces[lasery][laserx]=17
                        surface.blit(self.laser_hit,(laserx*50,lasery*50))
    	    elif dir is 'left':
    	        if laserx-1 >= -1:
    	            if self.pieces[lasery][laserx] == 0:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        laserx=laserx-1
                    else:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        hit = 1
                else:
                    firing=False
                    
                if hit == 1:
                    up = [1,5,11,15]
                    down = [2,6,12,16]
                    destroy = [3,4,7,8,9,13,14,17,18,19]
                    piece = self.pieces[lasery][laserx]
                    if piece in up:
                        dir = 'up'
                        lasery=lasery-1
                    elif piece in down:
                        dir = 'down'
                        lasery=lasery+1
                    elif piece in destroy:
                        firing = False
                        if piece not in (8,18):
                            self.pieces[lasery][laserx]=0
                        else:
                            if piece == 8:
                                self.pieces[lasery][laserx]=7
                            if piece == 18:
                                self.pieces[lasery][laserx]=17
                        surface.blit(self.laser_hit,(laserx*50,lasery*50))
    	    if dir is 'up':
    	        if lasery-1 >= -1:
    	            if self.pieces[lasery][laserx] == 0:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        lasery = lasery-1
                    else:
                        surface.blit(self.laser,(laserx*50,lasery*50))
                        hit = 1
                else:
                    firing=False
                    
                if hit == 1:
                    right = [2,12,6,16]
                    left = [3,13,5,15]
                    destroy = [1,4,7,8,9,11,14,17,18,19]
                    piece = self.pieces[lasery][laserx]
                    if piece in right:
                        dir = 'right'
                        laserx=laserx+1
                    elif piece in left:
                        dir = 'left'
                        laserx=laserx-1
                    elif piece in destroy:
                        firing = False
                        if piece not in (8,18):
                            self.pieces[lasery][laserx]=0
                        else:
                            if piece == 8:
                                self.pieces[lasery][laserx]=7
                            if piece == 18:
                                self.pieces[lasery][laserx]=17
                        surface.blit(self.laser_hit,(laserx*50,lasery*50))

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
    
    #create players and game
    game = Game()
    red_player = Player()
    grey_player = Player()
    red_player.cursor = load_image('red_select.bmp',-1)
    red_player.y=0
    red_player.x=5
    red_player.action='select'
    red_player.color='red'
    grey_player.cursor = load_image('grey_select.bmp',-1)
    grey_player.y=7
    grey_player.x=4
    grey_player.action='select'
    grey_player.color='grey'
    turn='red_player'
	
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
    red_player.draw_cursor(screen)
    pygame.display.flip()
    
    going = True
    player = 'red'
    while going:
        clock.tick(60)
        redraw=0
        
        if turn == 'red_player':
            player = red_player
        elif turn == 'grey_player':
            player = grey_player
        
        if player.action == 'laser':
            game.fire_laser(player.color,screen)
            pygame.display.flip()
            pygame.time.wait(1000)
            player.action = 'select'
            player.cursor = load_image(player.color+'_select.bmp',-1)
            if turn == 'grey_player':
                turn = 'red_player'
                player = red_player
            else:
                turn='grey_player'
                player = grey_player
            redraw=1
            
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_UP:
        	    if player.action == 'select':
        	        if player.y-1 >= 0:
        	            player.y = player.y - 1
        	            redraw=1
        	    elif player.action == 'action':
        	        illegal_color=0
        	        obelisk=0
        	        obelisk2x=0
        	        if player.color == 'red':
        	            illegal_color=2
        	            oblisk=7
        	            oblisk2x=8
        	        else:
        	            illegal_color=1
        	            oblisk=17
        	            oblisk2x=18        	        
        	        if game.pieces[player.y-1][player.x] == oblisk and game.pieces[player.y-1][player.x] == oblisk:
        	            game.pieces[player.y-1][player.x]=oblisk2x
        	            game.pieces[player.y][player.x]=0
        	            player.action='laser'
        	            player.cursor=None
        	            redraw = 1
        	        elif game.pieces[player.y-1][player.x] == 0 and game.pieces[player.y-1][player.x] != illegal_color and player.y-1 >= 0:
        	            game.pieces[player.y-1][player.x]=game.pieces[player.y][player.x]
        	            if game.pieces[player.y][player.x] is not oblisk2x:
        	                game.pieces[player.y][player.x] = 0
        	            else:
        	                game.pieces[player.y][player.x]=oblisk
        	                game.pieces[player.y-1][player.x]=oblisk
                        player.action='laser'
                        player.cursor=None
                        redraw = 1
            elif event.type == KEYDOWN and event.key == K_DOWN:
        	    if player.action == 'select':
        	        if player.y+1 <= 7:
        	            player.y = player.y + 1
        	            redraw=1
        	    elif player.action == 'action':
        	        illegal_color=0
        	        obelisk=0
        	        obelisk2x=0
        	        if player.color == 'red':
        	            illegal_color=2
        	            oblisk=7
        	            oblisk2x=8
        	        else:
        	            illegal_color=1
        	            oblisk=17
        	            oblisk2x=18
        	        if game.pieces[player.y+1][player.x] == oblisk and game.pieces[player.y+1][player.x] == oblisk:
        	            game.pieces[player.y+1][player.x]=oblisk2x
        	            game.pieces[player.y][player.x]=0
        	            player.action='laser'
        	            player.cursor=None
        	            redraw = 1
        	        elif game.pieces[player.y+1][player.x] == 0 and game.pieces[player.y+1][player.x] != illegal_color and player.y+1 <= 7:
        	            game.pieces[player.y+1][player.x]=game.pieces[player.y][player.x]
        	            if game.pieces[player.y][player.x] is not oblisk2x:
        	                game.pieces[player.y][player.x] = 0
        	            else:
        	                game.pieces[player.y][player.x]=oblisk
        	                game.pieces[player.y+1][player.x]=oblisk
                        player.action='laser'
                        player.cursor=None
                        redraw = 1
            elif event.type == KEYDOWN and event.key == K_LEFT:
        	    if player.action == 'select':
        	        if player.x-1 >= 0:
        	            player.x = player.x - 1
        	            redraw=1
        	    elif player.action == 'action':
        	        illegal_color=0
        	        obelisk=0
        	        obelisk2x=0
        	        if player.color == 'red':
        	            illegal_color=2
        	            oblisk=7
        	            oblisk2x=8
        	        else:
        	            illegal_color=1
        	            oblisk=17
        	            oblisk2x=18
        	        if game.pieces[player.y][player.x-1] == oblisk and game.pieces[player.y][player.x-1] == oblisk:
        	            game.pieces[player.y][player.x-1]=oblisk2x
        	            game.pieces[player.y][player.x]=0
        	            player.action='laser'
        	            player.cursor=None
        	            redraw = 1
        	        elif game.pieces[player.y][player.x-1] == 0 and game.pieces[player.y][player.x-1] != illegal_color and player.x-1 >= 0:
        	            game.pieces[player.y][player.x-1]=game.pieces[player.y][player.x]
        	            if game.pieces[player.y][player.x] is not oblisk2x:
        	                game.pieces[player.y][player.x] = 0
        	            else:
        	                game.pieces[player.y][player.x]=oblisk
        	                game.pieces[player.y][player.x-1]=oblisk
                        player.action='laser'
                        player.cursor=None
                        redraw = 1
            elif event.type == KEYDOWN and event.key == K_RIGHT:
        	    if player.action == 'select':
        	        if player.x+1 <= 9:
        	            player.x = player.x + 1
        	            redraw=1
        	    elif player.action == 'action':
        	        illegal_color=0
        	        obelisk=0
        	        obelisk2x=0
        	        if player.color == 'red':
        	            illegal_color=2
        	            oblisk=7
        	            oblisk2x=8
        	        else:
        	            illegal_color=1
        	            oblisk=17
        	            oblisk2x=18
        	        if game.pieces[player.y][player.x+1] == oblisk and game.pieces[player.y][player.x+1] == oblisk:
        	            game.pieces[player.y][player.x+1]=oblisk2x
        	            game.pieces[player.y][player.x]=0
        	            player.action='laser'
        	            player.cursor=None
        	            redraw = 1
        	        elif game.pieces[player.y][player.x+1] == 0 and game.pieces[player.y][player.x+1] != illegal_color and player.x+1 <= 9:
        	            game.pieces[player.y][player.x+1]=game.pieces[player.y][player.x]
        	            if game.pieces[player.y][player.x] is not oblisk2x:
        	                game.pieces[player.y][player.x] = 0
        	            else:
        	                game.pieces[player.y][player.x]=oblisk
        	                game.pieces[player.y][player.x+1]=oblisk
                        player.action='laser'
                        player.cursor=None
                        redraw = 1
            elif event.type == KEYDOWN and event.key == K_r:
                if player.action == 'select' or player.action == 'rotate':
                    if game.rotate_piece(player.x,player.y) == True:
                        player.action = 'rotate'
                        redraw=1
                    else:
                        player.action = 'select'
            elif event.type == KEYDOWN and event.key == K_RETURN:
        	    if player.action == 'select':
        	        if game.legal_select(player.color,player.x,player.y):
        	            player.action = 'action'
        	            player.cursor = load_image(player.color+'_action.bmp',-1)
        	            redraw=1
        	    if player.action == 'rotate':
                        player.action='laser'
                        player.cursor=None
                        redraw = 1
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            
        if redraw == 1:
            screen.blit(background,(0,0))
            game.draw_pieces(screen)
            if player.cursor is not None:
                player.draw_cursor(screen)
            pygame.display.flip()


#call main loop
main()

