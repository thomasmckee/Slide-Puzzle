import pygame
import random
from GameObject import GameObject

class MazeBlock(GameObject):
    def init():
        #Loading a blank white image to be drawn onto
        MazeBlock.image = pygame.image.load('images/whiteblank.png').convert()
        #Creating a board that will use boolean values to determine legal
        #player moves later
        MazeBlock.board = []
    def __init__(self, x, y, dirs, rows):
        #Scaling the image
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / self.rows)
        self.tile = pygame.transform.scale(MazeBlock.image, (self.blockWidth, self.blockWidth))
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
        #Creating an outline
        self.outline = (0, 0, self.blockWidth, self.blockWidth)
        pygame.draw.rect(self.tile, black, self.outline, 5)
        #Drawing path based off of inputted direction values from initiation
        L1 = (1/5)*self.blockWidth
        L2 = (2/5)*self.blockWidth
        L3 = (3/5)*self.blockWidth
        if self.n:
            r = (L2, 0, L1, L3)
            pygame.draw.rect(self.tile, black, r)
        if self.e:
            r = (L2, L2, L3, L1)
            pygame.draw.rect(self.tile, black, r)
        if self.s:
            r = (L2, L2, L1, L3)
            pygame.draw.rect(self.tile, black, r)
        if self.w:
            r = (0, L2, L3, L1)
            pygame.draw.rect(self.tile, black, r)
    #Standard update fct
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(MazeBlock, self).update()
        