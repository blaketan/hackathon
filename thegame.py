import pygame
import random

#classes
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
class player(pygame.sprite.Sprite):
# this class refers to the player object
    def __init__(self,x=400,y=300):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,move):
        """ Update the player's position. """
        if move == "up":
       		self.rect.y += 40
       	elif move == "left":
       		self.rect.x -= 40
       	elif move == "right":
       		self.rect.x += 40
       	else:
       		self.rect.y -= 40

# --- Sprite lists
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()



# initialize pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
done = False

#main game loop
player1=player()
all_sprites_list.add(player1)

while not done:
	#check for win condition
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
        	done = True
        elif event.type == pygame.KEYDOWN
    # --- Draw a frame

	screen.fill(WHITE)
	all_sprites_list.draw(screen)
pygame.quit()

import pygame, sys, pygame.mixer
from pygame.locals import*

pygame.init()

size = width, height = 1256, 640
screen = pygame.display.set_mode(size)
player_x = 0
player_y = 0
movex = 0 
movey = 0

maintheme = pygame.mixer.Sound("music/mainthemes.ogg")
maintheme.play()

player_w = pygame.image.load("characters/player/character_w.png").convert_alpha()
player_a = pygame.image.load("characters/player/character_a.png").convert_alpha()
player_s = pygame.image.load("characters/player/character_s.png").convert_alpha()
player_d = pygame.image.load("characters/player/character_d.png").convert_alpha()

background1 = pygame.image.load("maps/background1.png").convert_alpha()

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if 