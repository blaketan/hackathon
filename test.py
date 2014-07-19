import pygame, sys, random
from pygame.locals import *

BOARDWIDTH = 5
BOARDHEIGHT = 5
TILESIZE = 40
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH-1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT-1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Test')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    mainBoard = generateBoard()
    character = Character()

    while True:
        drawBoard(mainBoard)
        character.drawChar()
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    character.move(LEFT)
                elif event.key in (K_RIGHT, K_d):
                    character.move(RIGHT)
                elif event.key in (K_UP, K_w):
                    character.move(UP)
                elif event.key in (K_DOWN, K_s):
                    character.move(DOWN)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def generateBoard():
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(Tile())
        board.append(column)
    return board

def drawBoard(board):
    DISPLAYSURF.fill(BGCOLOR)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            board[tilex][tiley].drawTile(tilex, tiley)

def getLeftTopOfTile(tilex, tiley):
    left = XMARGIN + (tilex * TILESIZE) + (tilex - 1)
    top = YMARGIN + (tiley * TILESIZE) + (tiley - 1)
    return left, top

class Tile:
    def __init__(self, tiletype = 'ground'):
        self.tiletype = tiletype
        self.light = 0

    def brighten(self):
        self.light += 1

    def drawTile(self, tilex, tiley):
        left, top = getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE, TILESIZE))

class Character:
    def __init__(self, name = 'Name'):
        self.name = name
        self.pos = [0,0]

    def move(self, move):
        if move == UP:
            self.pos[1] -= 1
        elif move == DOWN:
            self.pos[1] += 1
        elif move == LEFT:
            self.pos[0] -= 1
        elif move == RIGHT:
            self.pos[0] += 1

    def drawChar(self):
        left, top = getLeftTopOfTile(self.pos[0], self.pos[1])
        pygame.draw.circle(DISPLAYSURF, WHITE, (left + TILESIZE // 2, top + TILESIZE // 2), TILESIZE // 2)

if __name__ == '__main__':
    main()