import pygame
import random
from GameObject import GameObject

class Block(GameObject):
    @staticmethod
    def init():
        #Loading the image
        image = pygame.image.load('images/gameimage.jpg').convert()
        width, height = image.get_size()
        #Cropping the image so it is the largest possible square, \
        #starting from the top left corner
        L = min(width, height)
        cropSq = (0, 0, L, L)
        cropped = image.subsurface(cropSq)
        puzzleWidth, puzzleHeight = 500, 500
        #Scaling to window size
        Block.scaled = pygame.transform.scale(  cropped, 
                                                (puzzleWidth, puzzleHeight))
        rows, cols = 4, 4
        cellWidth = puzzleWidth / rows
        Block.images = []
        #Cutting up the image into 4x4 
        for i in range(rows):
            for j in range(cols):
                subImage = Block.scaled.subsurface(i*cellWidth, j*cellWidth,
                                            cellWidth, cellWidth)
                Block.images.append(subImage)
        Block.images.pop()
        Block.seen = set()
        Block.board = []

    def __init__(self, x, y):
        self.boardLen = 15
        #Messy way to randomly assort blocks, but not sure if it can be improved
        while True:
            r = random.randint(0,self.boardLen - 1)
            #Finding an index not already found
            if r not in Block.seen:
                image = Block.images[r]
                Block.seen.add(r)
                #Creating a numeric board for easier legality checking
                Block.board.append(r)
                if len(Block.seen) == self.boardLen:
                    Block.board.append(self.boardLen)
                break
        super(Block, self).__init__(x, y, image, 0)
    
    #Simple function for updating new coordinates of blocks
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Block, self).update()