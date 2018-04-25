from GameObject import GameObject
import pygame

class Hole(GameObject):
    def init():
        #Loading and scaling player image
        Hole.image = pygame.image.load('images/mousehole.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Hole.image, (self.playerWidth, self.playerWidth))
        super(Hole, self).__init__(x, y, self.scaled, self.playerWidth)
    def update(self, w, h):
        super(Hole, self).update()

class Trap(GameObject):
    def init():
        #Loading and scaling player image
        Trap.image = pygame.image.load('images/trap.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.hit = False
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Trap.image, (self.playerWidth, self.playerWidth))
        super(Trap, self).__init__(x, y, self.scaled, self.playerWidth)
    def update(self, w, h):
        super(Trap, self).update()

class Enemy(GameObject):
    def init():
        Enemy.image = pygame.image.load('images/enemy.png').convert_alpha()
    def __init__(self, d1, d2, i, r):
        self.width = 500
        self.rows = r
        self.blockWidth = int(self.width / self.rows)
        self.d1 = d1
        self.d2 = d2
        self.i  = i
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        w = self.blockWidth / 2
        #Finding the initial x and y, as well as velocities, of the enemy
        #Based off of the inputs from spawnEnemy fct in Maze class
        if d1 == 'V':
            self.x = w+(w*i*2)
            if d2 == 'U':
                self.y = self.width + w
                self.vy = -5
            if d2 == 'D':
                self.y = -w
                self.vy = 5
        if d1 == 'H':
            self.y = w+(w*i*2)
            if d2 == 'L':
                self.x = self.width + w
                self.vx = -5
            if d2 == 'R':
                self.x = -w
                self.vx = 5
        self.scaled = pygame.transform.scale(Enemy.image, (self.blockWidth, self.blockWidth))
        super(Enemy, self).__init__(self.x, self.y, self.scaled, w)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Enemy, self).update()

class MazeBlock(GameObject):
    def init():
        #Loading a blank white image to be drawn onto
        MazeBlock.image = pygame.image.load('images/grass.png').convert()
        #Creating a board that will use boolean values to determine legal
        #player moves later
        MazeBlock.board = []
    def __init__(self, x, y, dirs, rows):
        #Scaling the image
        self.rows = rows
        self.width = 500
        self.blockWidth =int(self.width / self.rows)
        #Implemented following 3 lines to deal with scaling visual glitch
        w = self.blockWidth
        self.tile = pygame.transform.scale(MazeBlock.image, (w, w))
        self.n, self.e, self.s, self.w = dirs[0], dirs[1], dirs[2], dirs[3]
        MazeBlock.board.append([self.n, self.e, self.s, self.w])
        #Adding blank once all other pieces are there
        if len(MazeBlock.board) == self.rows**2-1:
            MazeBlock.board.append(0)
        super(MazeBlock, self).__init__(x, y, self.tile, 0)
        #Drawing on the piece based off of inputs
        self.drawPiece()
    def drawPiece(self):
        #Setting up RGB values
        black = (0, 0, 0)
        white = (255, 255, 255)
        brown = (139,69,19)
        #Creating an outline
        self.outline = (0, 0, self.blockWidth, self.blockWidth)
        pygame.draw.rect(self.tile, black, self.outline, 1)
        #Drawing path based off of inputted direction values from initiation
        L1 = (1/5)*self.blockWidth
        L2 = (2/5)*self.blockWidth
        L3 = (3/5)*self.blockWidth
        if self.n:
            r = (L2, 0, L1, L3)
            pygame.draw.rect(self.tile, brown, r)
        if self.e:
            r = (L2, L2, L3, L1)
            pygame.draw.rect(self.tile, brown, r)
        if self.s:
            r = (L2, L2, L1, L3)
            pygame.draw.rect(self.tile, brown, r)
        if self.w:
            r = (0, L2, L3, L1)
            pygame.draw.rect(self.tile, brown, r)
    #Standard update fct
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(MazeBlock, self).update()

class Blank(GameObject):
    def init():
        #Loading the blank image
        Blank.image = pygame.image.load('images/blank.png').convert()
    #Calling init and having update, same as Block class
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / self.rows)+1
        self.scaled = pygame.transform.scale(Blank.image, (self.blockWidth, self.blockWidth))
        super(Blank, self).__init__(x, y, self.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Blank, self).update()

class Player(GameObject):
    def init():
        #Loading and scaling player image
        Player.image = pygame.image.load('images/player.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Player.image, (self.playerWidth, self.playerWidth))
        super(Player, self).__init__(x, y, self.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Player, self).update()

class Point(GameObject):
    def init():
        #Loading and scaling player image
        Point.yellow = pygame.image.load('images/cheese.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.hit = False
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Point.yellow, (self.playerWidth, self.playerWidth))
        super(Point, self).__init__(x, y, self.scaled, self.playerWidth)
    def update(self, w, h):
        super(Point, self).update()