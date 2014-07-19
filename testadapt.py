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

STEPS_TAKEN = 0
MOVE_LIMIT = 100

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH-1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT-1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

groundTile = pygame.image.load('tiles/ground.png')
ugroundTile = pygame.image.load('tiles/uground.png')
dgroundTile = pygame.image.load('tiles/dground.png')
lgroundTile = pygame.image.load('tiles/lground.png')
rgroundTile = pygame.image.load('tiles/rground.png')
ulgroundTile = pygame.image.load('tiles/ulground.png')
urgroundTile = pygame.image.load('tiles/urground.png')
dlgroundTile = pygame.image.load('tiles/dlground.png')
drgroundTile = pygame.image.load('tiles/drground.png')
cwallTile = pygame.image.load('tiles/cwall.png')
udwallTile = pygame.image.load('tiles/udwall.png')
lrwallTile = pygame.image.load('tiles/lrwall.png')
ulwallTile = pygame.image.load('tiles/ulwall.png')
urwallTile = pygame.image.load('tiles/urwall.png')
dlwallTile = pygame.image.load('tiles/dlwall.png')
drwallTile = pygame.image.load('tiles/drwall.png')
utwallTile = pygame.image.load('tiles/utwall.png')
dtwallTile = pygame.image.load('tiles/dtwall.png')
ltwallTile = pygame.image.load('tiles/ltwall.png')
rtwallTile = pygame.image.load('tiles/rtwall.png')
uendTile = pygame.image.load('tiles/uend.png')
dendTile = pygame.image.load('tiles/dend.png')
lendTile = pygame.image.load('tiles/lend.png')
rendTile = pygame.image.load('tiles/rend.png')
uedgeTile = pygame.image.load('tiles/uedge.png')
dedgeTile = pygame.image.load('tiles/dedge.png')
ledgeTile = pygame.image.load('tiles/ledge.png')
redgeTile = pygame.image.load('tiles/redge.png')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Test')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    mainBoard = generateBoard()
    character = Character()


        drawBoard(mainBoard)
        character.drawChar()
        powerups = gen_power_up()
        for up in powerups:
            up.drawPowerup
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    character.move(LEFT, mainBoard)
                elif event.key in (K_RIGHT, K_d):
                    character.move(RIGHT, mainBoard)
                elif event.key in (K_UP, K_w):
                    character.move(UP, mainBoard)
                elif event.key in (K_DOWN, K_s):
                    character.move(DOWN, mainBoard)
        character.light(mainBoard)
        DISPLAYSURF.blit(label, (0,0))
        step_count = BASICFONT.render("Steps Left: "+str(MOVE_LIMIT - STEPS_TAKEN), 1, (255,0,0))
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
    for x in range(1,BOARDWIDTH-1):
        board[x][0] = Tile('uground')
        board[x][BOARDHEIGHT-1] = Tile('dground')
    for y in range(1,BOARDHEIGHT-1):
        board[0][y] = Tile('lground')
        board[BOARDWIDTH-1][y] = Tile('rground')
    board[0][0] = Tile('ulground')
    board[BOARDWIDTH-1][0] = Tile('urground')
    board[BOARDWIDTH-1][BOARDHEIGHT-1] = Tile('drground')
    board[0][BOARDHEIGHT-1] = Tile('dlground')
    board[2][2] = Tile('lend')
    board[2][8] = Tile('uend')
    board[2][9] = Tile('dlwall')
    board[3][2] = Tile('urwall')
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
    if STEPS_TAKEN > MOVE_LIMIT:
        return BASICFONT.render("You lost to the Powers of Darkness", 1, (255,0,0))
    elif light_sum == total_condition:
        return BASICFONT.render("You Win! You lit up the night.", 1, (0,255,0))
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
            if self.tiletype == 'ground':
                DISPLAYSURF.blit(groundTile,(left, top))
            elif self.tiletype == 'uground':
                DISPLAYSURF.blit(ugroundTile,(left, top))
            elif self.tiletype == 'dground':
                DISPLAYSURF.blit(dgroundTile,(left, top))
            elif self.tiletype == 'lground':
                DISPLAYSURF.blit(lgroundTile,(left, top))
            elif self.tiletype == 'rground':
                DISPLAYSURF.blit(rgroundTile,(left, top))
            elif self.tiletype == 'ulground':
                DISPLAYSURF.blit(ulgroundTile,(left, top))
            elif self.tiletype == 'urground':
                DISPLAYSURF.blit(urgroundTile,(left, top))
            elif self.tiletype == 'dlground':
                DISPLAYSURF.blit(dlgroundTile,(left, top))
            elif self.tiletype == 'drground':
                DISPLAYSURF.blit(drgroundTile,(left, top))
            elif self.tiletype == 'cwall':
                DISPLAYSURF.blit(cwallTile,(left, top))
            elif self.tiletype == 'udwall':
                DISPLAYSURF.blit(udwallTile,(left, top))
            elif self.tiletype == 'lrwall':
                DISPLAYSURF.blit(lrwallTile,(left, top))
            elif self.tiletype == 'ulwall':
                DISPLAYSURF.blit(ulwallTile,(left, top))
            elif self.tiletype == 'urwall':
                DISPLAYSURF.blit(urwallTile,(left, top))
            elif self.tiletype == 'dlwall':
                DISPLAYSURF.blit(dlwallTile,(left, top))
            elif self.tiletype == 'drwall':
                DISPLAYSURF.blit(drwallTile,(left, top))
            elif self.tiletype == 'utwall':
                DISPLAYSURF.blit(utwallTile,(left, top))
            elif self.tiletype == 'dtwall':
                DISPLAYSURF.blit(dtwallTile,(left, top))
            elif self.tiletype == 'ltwall':
                DISPLAYSURF.blit(ltwallTile,(left, top))
            elif self.tiletype == 'rtwall':
                DISPLAYSURF.blit(rtwallTile,(left, top))
            elif self.tiletype == 'uend':
                DISPLAYSURF.blit(uendTile,(left, top))
            elif self.tiletype == 'dend':
                DISPLAYSURF.blit(dendTile,(left, top))
            elif self.tiletype == 'lend':
                DISPLAYSURF.blit(lendTile,(left, top))
            elif self.tiletype == 'rend':
                DISPLAYSURF.blit(rendTile,(left, top))
            elif self.tiletype == 'uedge':
                DISPLAYSURF.blit(uedgeTile,(left, top))
            elif self.tiletype == 'dedge':
                DISPLAYSURF.blit(dedgeTile,(left, top))
            elif self.tiletype == 'ledge':
                DISPLAYSURF.blit(ledgeTile,(left, top))
            elif self.tiletype == 'redge':
                DISPLAYSURF.blit(redgeTile,(left, top))
        else:
            pygame.draw.rect(DISPLAYSURF, BLACK, (left, top, TILESIZE, TILESIZE))

class Character:
    def __init__(self, name = 'Name'):
        self.name = name
        self.x = BOARDWIDTH // 2
        self.y = BOARDHEIGHT // 2
        self.oil = 5

    def move(self, move, board):
        if move == UP:
            if self.y > 0 and 'ground' in board[self.x][self.y-1].tiletype:
                self.y -= 1
        elif move == DOWN:
            if self.y < BOARDHEIGHT - 1 and 'ground' in board[self.x][self.y+1].tiletype:
                self.y += 1
        elif move == LEFT:
            if self.x > 0 and 'ground' in board[self.x-1][self.y].tiletype:
                self.x -= 1
        elif move == RIGHT:
            if self.x < BOARDWIDTH - 1 and 'ground' in board[self.x+1][self.y].tiletype:
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