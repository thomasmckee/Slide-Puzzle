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
    def __init__(self, x, y, dirs):
        #Scaling the image
        self.tile = pygame.transform.scale(MazeBlock.image, (125, 125))
        self.n, self.e, self.s, self.w = dirs[0], dirs[1], dirs[2], dirs[3]
        MazeBlock.board.append([self.n, self.e, self.s, self.w])
        #Temporary hardcoding for 4x4, adds a representation of the blank space
        #to the physical (not graphical) board
        if len(MazeBlock.board) == 15:
            MazeBlock.board.append(0)
        super(MazeBlock, self).__init__(x, y, self.tile, 0)
        #Drawing on the piece based off of inputs
        self.drawPiece()
    def drawPiece(self):
        #Setting up RGB values
        black = (0, 0, 0)
        white = (255, 255, 255)
        #Creating an outline
        self.r1 = (0, 0, 125, 125)
        pygame.draw.rect(self.tile, black, self.r1, 5)
        #Drawing path based off of inputted direction values from initiation
        if self.n:
            r = (50, 0, 25, 75)
            pygame.draw.rect(self.tile, black, r)
        if self.e:
            r = (50, 50, 75, 25)
            pygame.draw.rect(self.tile, black, r)
        if self.s:
            r = (50, 50, 25, 75)
            pygame.draw.rect(self.tile, black, r)
        if self.w:
            r = (0, 50, 75, 25)
            pygame.draw.rect(self.tile, black, r)
    #Standard update fct
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(MazeBlock, self).update()
        