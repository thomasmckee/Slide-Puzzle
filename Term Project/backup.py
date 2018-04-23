from Player import Player
from Block import Block
from MazeBlock import MazeBlock
from Blank import Blank
import pygame

class Maze(object):
    def init(self):
        self.gameMode = 'Maze'
        self.gameWon = False
        self.gameLost = False
        Block.init()
        self.blocks = pygame.sprite.Group()
        self.rows = 4
        self.puzzleWidth = 500
        self.blockWidth = self.puzzleWidth / self.rows
        self.boardL = 15
        self.coords = []
        MazeBlock.init()
        for i in range(self.rows):
            for j in range(self.rows):
                index = i * self.rows + j
                #Not taking the last block, as it is supposed to be blank
                if index == self.rows**2-1:
                    continue
                #Calculating location of blocks and adding them to sprite group
                x = j*(self.blockWidth)+(self.blockWidth/2)
                y = i*(self.blockWidth)+(self.blockWidth/2)
                self.coords.append((x, y))
        #Creating the maze pieces
        cross = (True, True, True, True)
        upt = (True, True, False, True)
        downt = (False, True, True, True)
        tlc = (True, False, False, True)
        trc = (True, True, False, False)
        blc = (False, False, True, True)
        brc = (False, True, True, False)
        blank = (False, False, False, False)
        vert = (True, False, True, False)
        horz = (False, True, False, True)
        #Creating the maze
        maze1 = [horz, horz, cross, downt, upt, tlc, trc, blc, brc, blank, 
        horz, blank, horz, blank, blank]
        for i in range(self.rows**2-1):
            self.blocks.add(MazeBlock(self.coords[i][0], self.coords[i][1],
            maze1[i]))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.puzzleWidth * (7/8)
        self.blocks.add(Blank(blankInitial, blankInitial))
        #Initiating the player
        Player.init()
        self.player = Player(62.5, 62.5)
        self.playerSprite = pygame.sprite.Group()
        self.playerSprite.add(self.player)
        self.playerIndex = 0
        self.remainingMoves = 30
        self.remainingTime = 30
        self.timerCalled = 0