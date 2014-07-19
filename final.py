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

STEPS_TAKEN = 0
MOVE_LIMIT = 150
LOST_YET = False
TREASURE_FOUND = False

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

dmovel = pygame.image.load('sprites/dmovel.png')
dmover = pygame.image.load('sprites/dmover.png')
dstill = pygame.image.load('sprites/dstill.png')
lmove = pygame.image.load('sprites/lmove.png')
lstill = pygame.image.load('sprites/lstill.png')
rmove = pygame.image.load('sprites/rmove.png')
rstill = pygame.image.load('sprites/rstill.png')
umovel = pygame.image.load('sprites/umovel.png')
umover = pygame.image.load('sprites/umover.png')
ustill = pygame.image.load('sprites/ustill.png')
treasureSprite = pygame.image.load('sprites/treasure.png')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Test')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    mainBoard = generateBoard()
    character = Character()
    treasure = Treasure()

    while True:
        drawBoard(mainBoard)
        treasure.drawTreasure(mainBoard)
        character.drawChar()
        checkForQuit()
        if [character.x,character.y] == [treasure.x,treasure.y]:
            global TREASURE_FOUND
            TREASURE_FOUND = True
        label = check_for_win(mainBoard)
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
    board[1][1] = Tile('lend')
    board[1][7] = Tile('uend')
    board[1][8] = Tile('dlwall')
    board[2][1] = Tile('urwall')
    board[2][2] = Tile('rtwall')
    board[2][3] = Tile('udwall')
    board[2][4] = Tile('udwall')
    board[2][5] = Tile('dend')
    board[2][8] = Tile('lrwall')
    board[3][2] = Tile('lrwall')
    board[3][8] = Tile('lrwall')
    board[4][1] = Tile('ulwall')
    board[4][2] = Tile('ltwall')
    board[4][3] = Tile('dend')
    board[4][6] = Tile('uend')
    board[4][7] = Tile('rtwall')
    board[4][8] = Tile('ltwall')
    board[4][9] = Tile('dedge')
    board[5][0] = Tile('uedge')
    board[5][1] = Tile('utwall')
    board[5][7] = Tile('rend')
    board[6][1] = Tile('lrwall')
    board[7][1] = Tile('urwall')
    board[7][2] = Tile('udwall')
    board[7][3] = Tile('dlwall')
    board[7][6] = Tile('lend')
    board[7][8] = Tile('lend')
    board[8][3] = Tile('lrwall')
    board[8][6] = Tile('dtwall')
    board[8][7] = Tile('udwall')
    board[8][8] = Tile('utwall')
    board[9][1] = Tile('lend')
    board[9][3] = Tile('rend')
    board[9][5] = Tile('uend')
    board[9][6] = Tile('drwall')
    board[9][8] = Tile('lrwall')
    board[10][1] = Tile('lrwall')
    board[10][8] = Tile('lrwall')
    board[11][1] = Tile('lrwall')
    board[11][3] = Tile('ulwall')
    board[11][4] = Tile('udwall')
    board[11][5] = Tile('udwall')
    board[11][6] = Tile('rtwall')
    board[11][7] = Tile('udwall')
    board[11][8] = Tile('drwall')
    board[12][1] = Tile('urwall')
    board[12][2] = Tile('udwall')
    board[12][3] = Tile('utwall')
    board[12][6] = Tile('lrwall')
    board[13][3] = Tile('urwall')
    board[13][4] = Tile('dend')
    board[13][6] = Tile('urwall')
    board[13][7] = Tile('udwall')
    board[13][8] = Tile('dlwall')
    board[14][8] = Tile('redge')
    return board


def check_for_win(board):
    total_condition = BOARDHEIGHT * BOARDWIDTH
    light_sum = 0
    for column in board:
        for tile in column:
            if tile.light >0:
                light_sum += 1
    if STEPS_TAKEN > MOVE_LIMIT:
        global LOST_YET
        LOST_YET = True
        return BASICFONT.render("You lost your heart to the darkness", 1, (255,0,0))
    elif TREASURE_FOUND:
        return BASICFONT.render("You win! You found the light.", 1, (0,255,0))
    elif light_sum == total_condition:
        return BASICFONT.render("You win! You lit up the night.", 1, (0,255,0))
    elif MOVE_LIMIT - STEPS_TAKEN <15:
        return BASICFONT.render("DANGER DANGER", 1, (255,0,0))
    else:
        return BASICFONT.render("You better get moving!", 1, (255,255,0))

def drawBoard(board):
    DISPLAYSURF.fill(BGCOLOR)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            board[tilex][tiley].drawTile(tilex, tiley)

def getLeftTopOfTile(tilex, tiley):
    left = XMARGIN + (tilex * TILESIZE)
    top = YMARGIN + (tiley * TILESIZE)
    return left, top

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
    def __init__(self, name = 'Timmy'):
        self.name = name
        self.x = BOARDWIDTH // 2
        self.y = BOARDHEIGHT // 2
        self.lastx = self.x
        self.lasty = self.y
        self.lastmove = DOWN
        self.oil = 5

    def move(self, move, board):
        if LOST_YET == False:
            if move == UP:
                self.lastmove = UP
                self.lasty = self.y
                if self.y > 0 and 'ground' in board[self.x][self.y-1].tiletype:
                    self.y -= 1
            elif move == DOWN:
                self.lastmove = DOWN
                self.lasty = self.y
                if self.y < BOARDHEIGHT - 1 and 'ground' in board[self.x][self.y+1].tiletype:
                    self.y += 1
            elif move == LEFT:
                self.lastmove = LEFT
                self.lastx = self.x
                if self.x > 0 and 'ground' in board[self.x-1][self.y].tiletype:
                    self.x -= 1
            elif move == RIGHT:
                self.lastmove = RIGHT
                self.lastx = self.x
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
        if self.x == self.lastx and self.y == self.lasty:
            if self.lastmove == UP:
                DISPLAYSURF.blit(ustill,(left, top))
            elif self.lastmove == DOWN:
                DISPLAYSURF.blit(dstill,(left, top))
            elif self.lastmove == LEFT:
                DISPLAYSURF.blit(lstill,(left, top))
            elif self.lastmove == RIGHT:
                DISPLAYSURF.blit(rstill,(left, top))
        else:
            if self.lastmove == UP:
                DISPLAYSURF.blit(umover,(left, top))
            elif self.lastmove == DOWN:
                DISPLAYSURF.blit(dmover,(left, top))
            elif self.lastmove == LEFT:
                DISPLAYSURF.blit(lmove,(left, top))
            elif self.lastmove == RIGHT:
                DISPLAYSURF.blit(rmove,(left, top))

class Treasure:
    def __init__(self):
        coordList = [[3,9],[3,1],[12,7],[12,4],[14,7],[6,0]]
        coord = random.choice(coordList)
        self.x = coord[0]
        self.y = coord[1]

    def drawTreasure(self, board):
        if board[self.x][self.y].light:
            left, top = getLeftTopOfTile(self.x, self.y)
            DISPLAYSURF.blit(treasureSprite,(left, top))

if __name__ == '__main__':
    main()