import pygame
import random

#classes

class Player(x = 400,y = 300):
# this class refers to the player object
	def __init__(self,x,y):









# initialize pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
done = False

#main game loop
player()

while not done:
	#check for win condition
	for event in pygame.event.get()
	    if event.type == pygame.QUIT:
            done = True
        elif event = pygame.event.KEYUP








pygame.quit()