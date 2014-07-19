import pygame, sys, random
from pygame.locals import *

BOARDWIDTH = 15
BOARDHEIGHT = 10
TILESIZE = 40
WINDOWWIDTH = 750
WINDOWHEIGHT = 480
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
BGCOLOR = BLACK
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
STEPS_TAKEN = 0
MOVE_LIMIT = 100
groundTile = pygame.image.load('tiles/ground.png')

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
        label = check_for_win(mainBoard)
        drawBoard(mainBoard)
        character.drawChar()
        check_for_win(mainBoard)
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
        character.light(mainBoard)
        DISPLAYSURF.blit(label, (0,0))
        step_count = BASICFONT.render("Steps Left"+str(MOVE_LIMIT - STEPS_TAKEN), 1, (255,0,0))
        DISPLAYSURF.blit(step_count, (600,0))
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
    left = XMARGIN + (tilex * TILESIZE)
    top = YMARGIN + (tiley * TILESIZE)
    return left, top

def check_for_win(board):
    total_condition = BOARDHEIGHT * BOARDWIDTH
    light_sum = 0
    for column in board:
        for tile in column:
            if tile.light >0:
                light_sum += 1
    if STEPS_TAKEN >= MOVE_LIMIT:
        return BASICFONT.render("You Looooooose", 1, (255,0,0))
    elif light_sum == total_condition:
        return BASICFONT.render("You Win", 1, (255,255,0))
    elif MOVE_LIMIT - STEPS_TAKEN <15:
        return BASICFONT.render("DANGER DANGER", 1, (255,0,0))
    else:
        return BASICFONT.render("You Better get moving", 1, (255,255,0))

        

class Tile:
    def __init__(self, tiletype = 'ground'):
        self.tiletype = tiletype
        self.light = 0

    def brighten(self):
        self.light += 1

    def drawTile(self, tilex, tiley):
        left, top = getLeftTopOfTile(tilex, tiley)
        if self.light:
            DISPLAYSURF.blit(groundTile,(left, top))
        else:
            pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, TILESIZE, TILESIZE))

class Character:
    def __init__(self, name = 'Name'):
        self.name = name
        self.x = BOARDWIDTH // 2
        self.y = BOARDHEIGHT // 2

    def move(self, move):
        if move == UP:
            if self.y > 0:
                self.y -= 1
        elif move == DOWN:
            if self.y < BOARDHEIGHT - 1:
                self.y += 1
        elif move == LEFT:
            if self.x > 0:
                self.x -= 1
        elif move == RIGHT:
            if self.x < BOARDWIDTH - 1:
                self.x += 1
        global STEPS_TAKEN
        STEPS_TAKEN += 1

    def light(self, board):
        board[self.x][self.y].brighten()
        if self.x > 0:
            board[self.x-1][self.y].brighten()
        if self.x < BOARDWIDTH - 1:
            board[self.x+1][self.y].brighten()
        if self.y > 0:
            board[self.x][self.y-1].brighten()
        if self.y < BOARDHEIGHT - 1:
            board[self.x][self.y+1].brighten()

    def drawChar(self):
        left, top = getLeftTopOfTile(self.x, self.y)
        pygame.draw.circle(DISPLAYSURF, WHITE, (left + TILESIZE // 2, top + TILESIZE // 2), TILESIZE // 2)

if __name__ == '__main__':
    main()