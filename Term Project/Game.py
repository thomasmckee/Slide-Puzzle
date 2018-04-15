from pygamegame import PygameGame
from Block import Block
from Blank import Blank
import pygame

class Game(PygameGame):
    
#Information about valid board states taken from this website:
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
#However, all of this code is original
    def isValidBoard(self, board):
        inversions = 0
        for i in range(len(board)):
            check = board[i:]
            for j in check:
                if board[i] > j and j != 0:
                    inversions += 1
        if len(board) % 2 == 1:
            if inversions % 2 == 0:
                return True
        elif len(board) % 2 == 0:
            if (board.index(0)//len(board)) % 2 == 0:
                if inversions % 2 == 1:
                    return True
            elif (board.index(0)//len(board)) % 2 == 1:
                if inversions % 2 == 0:
                    return True
        return False
    
    def init(self):
        Block.init()
        self.blocks = pygame.sprite.Group()
        self.rows = 4
        self.puzzleWidth = 500
        self.blockWidth = self.puzzleWidth / self.rows
        self.boardL = 15
        for i in range(self.rows):
            for j in range(self.rows):
                #Not taking the last block, as it is supposed to be blank
                if i+j == 6:
                    continue
                #Calculating location of blocks and adding them to sprite group
                x = i*(self.blockWidth)+(self.blockWidth/2)
                y = j*(self.blockWidth)+(self.blockWidth/2)
                self.blocks.add(Block(x, y))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.puzzleWidth * (7/8)
        self.blocks.add(Blank(blankInitial, blankInitial))
        #If the board that was created is not valid, make a new one until it is
        if not self.isValidBoard(Block.board):
            self.init()
            return

    def mousePressed(self, x, y):
        #Out of bounds check
        if x < 0 or x > self.puzzleWidth or y < 0 or y > self.puzzleWidth:
            return
        #Calculating the index of the blank 
        self.bI = Block.board.index(self.boardL)
        self.bX = self.bI %  self.rows
        self.bY = self.bI // self.rows
        #Calculating index of the click
        cX = x // self.blockWidth
        cY = y // self.blockWidth
        i  = int(cY * self.rows + cX)
        dx, dy = 0, 0
        if abs(self.bX-cX) + abs(self.bY-cY) < 2: #If valid move
            #Updating the numeric board that checks legality
            Block.board[i], Block.board[self.bI] = \
            Block.board[self.bI], Block.board[i]
            for block in self.blocks:
                #Finds which block was clicked
                if  abs(x-block.x) < (self.blockWidth / 2) and \
                    abs(y-block.y) < (self.blockWidth / 2):
                    #Determining the direction the block will move
                    if self.bX > cX:
                        dx = 1
                    elif self.bX < cX:
                        dx = -1
                    elif self.bY > cY:
                        dy = 1
                    elif self.bY < cY:
                        dy = -1
                    #Updating the block 
                    block.update(   block.x + (self.blockWidth * dx), 
                                    block.y + (self.blockWidth * dy),
                                    self.width, self.height)
        for block in self.blocks:
            if isinstance(block, Blank):
                #Updating the blank in opposite direction of the block
                dx, dy = -dx, -dy
                block.update(   block.x + (self.blockWidth * dx), 
                                block.y + (self.blockWidth * dy),
                                self.width, self.height)
    
    #Drawing the blocks
    def redrawAll(self, screen):
        self.blocks.draw(screen)

Game(500, 500).run()
    