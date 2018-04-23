from pygamegame import PygameGame
from Block import Block
from Blank import Blank
from MazeBlock import MazeBlock
from Player import Player
import pygame
import time
pygame.font.init()

#Fix 4x4 hardcoding, create new non 4x4 levels, maze level menu/interface
#1v1 mode

class Game(PygameGame):
    
#Information about valid board states taken from this website:
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    #However, all of this code is original
    def isValidBoard(self, board):
        if board == list(range(len(board))):
            return True
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
            if (board.index(self.boardL)//len(board)) % 2 == 0:
                if inversions % 2 == 1:
                    return True
            elif (board.index(self.boardL)//len(board)) % 2 == 1:
                if inversions % 2 == 0:
                    return True
        return False
    
    #Init for start, the menu
    def init(self):
        self.gameMode = 'Menu'
    
    #Init for image puzzle
    def initImage(self):
        self.hint = False
        self.gameWon = False
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
                x = j*(self.blockWidth)+(self.blockWidth/2)
                y = i*(self.blockWidth)+(self.blockWidth/2)
                self.blocks.add(Block(x, y))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.puzzleWidth * (7/8)
        self.blocks.add(Blank(blankInitial, blankInitial))
        #If the board that was created is not valid, make a new one until it is
        if not self.isValidBoard(Block.board):
            self.init()
            return
    
    #Init for maze puzzle
    def initMaze(self):
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
    
    def mousePressed(self, x, y):
        #Different mousepressed fcts depending where in interface
        if self.gameMode == 'Menu':
            self.mousePressedMenu(x, y)
        if self.gameMode == 'Image':
            self.mousePressedImage(x, y)
        if self.gameMode == 'Maze':
            self.mousePressedMaze(x, y)
    
    def mousePressedMenu(self, x, y):
        #Selecting different modes from menu
        if 150 < x < 350 and 100 < y < 200:
            self.initImage()
            self.gameMode = 'Image'
        if 150 < x < 350 and 300 < y < 400:
            self.initMaze()
            self.gameMode = 'Maze'
    
    def mousePressedMaze(self, x, y):
        #Out of bounds check
        if not 0 < x < self.width or not 0 < y < self.height:
            return
        #Option to return to menu if game is lost
        if self.gameWon or self.gameLost:
            if 175 < x < 325 and 312 < y < 388:
                self.gameMode = 'Menu'
            return
        #Can't move block with player on it
        if  abs(self.player.x - x) < self.blockWidth / 2 and \
            abs(self.player.y - y) < self.blockWidth / 2 :
            return
        #Menu button in game
        if 0 < x < 166 and 500 < y < 600:
            self.gameMode = 'Menu'
            return
        self.bI = MazeBlock.board.index(0)
        self.bX = self.bI % self.rows
        self.bY = self.bI // self.rows
        cX = x // self.blockWidth
        cY = y // self.blockWidth
        i  = int(cY * self.rows + cX)
        dx, dy = 0, 0
        if abs(self.bX-cX) + abs(self.bY-cY) < 2: #If valid move
            self.remainingMoves -= 1
            if self.remainingMoves == 0:
                self.gameLost = True
            #Updating the numeric board that checks legality
            MazeBlock.board[i], MazeBlock.board[self.bI] = \
            MazeBlock.board[self.bI], MazeBlock.board[i]
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
        
    def mousePressedImage(self, x, y):
        #Out of bounds check
        if not 0 < x < self.width or not 0 < y < self.height:
            return
        #Option to return to menu if game is lost
        if self.gameWon:
            if 175 < x < 325 and 312 < y < 388:
                self.gameMode = 'Menu'
            return
        #Menu button in game
        if 0 < x < 166 and 500 < y < 600:
            self.gameMode = 'Menu'
            return
        #Turning on/off hints:
        if 333 < x < 500 and 500 < y < 600:
            self.hint = not self.hint
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
        #Temporary win notification until better interface created
        if Block.board == list(range(self.boardL+1)):
            self.gameWon = True
    
    def keyPressed(self, keyCode, modifier):
        #Movement of Player:
        if keyCode == pygame.K_d:
            #Preventing out of bounds
            if self.playerIndex % self.rows == self.rows-1:
                return
            #Can't move to blank
            if MazeBlock.board[self.playerIndex+1] == 0:
                return
            #Testing for validity of movement, then moving
            if  MazeBlock.board[self.playerIndex][1] and \
                MazeBlock.board[self.playerIndex+1][3]:
                self.player.update( self.player.x + self.blockWidth, 
                                    self.player.y, 
                                    self.width, self.height)
                self.playerIndex += 1
        #Same but for other directions:
        if keyCode == pygame.K_w:
            if self.playerIndex // self.rows == 0:
                return
            if MazeBlock.board[self.playerIndex-self.rows] == 0:
                return
            if  MazeBlock.board[self.playerIndex][0] and \
                MazeBlock.board[self.playerIndex-self.rows][2]:
                self.player.update( self.player.x, 
                                    self.player.y - self.blockWidth, 
                                    self.width, self.height)
                self.playerIndex -= self.rows
        if keyCode == pygame.K_a:
            if self.playerIndex % self.rows == 0:
                return
            if MazeBlock.board[self.playerIndex-1] == 0:
                return
            if  MazeBlock.board[self.playerIndex][3] and \
                MazeBlock.board[self.playerIndex-1][1]:
                self.player.update( self.player.x - self.blockWidth, 
                                    self.player.y, 
                                    self.width, self.height)
                self.playerIndex -= 1
        if keyCode == pygame.K_s:
            if self.playerIndex // self.rows == self.rows - 1:
                return
            if MazeBlock.board[self.playerIndex+self.rows] == 0:
                return
            if  MazeBlock.board[self.playerIndex][2] and \
                MazeBlock.board[self.playerIndex+self.rows][0]:
                self.player.update( self.player.x, 
                                    self.player.y + self.blockWidth, 
                                    self.width, self.height)
                self.playerIndex += self.rows
        if self.playerIndex == self.rows**2 - 1:
            self.gameWon = True 

    def timerFired(self, dt):
        #Timer only needed in maze
        if self.gameMode != 'Maze':
            return
        #Decreasing time remaining every second
        self.timerCalled += 1
        if self.timerCalled % self.fps == 0:
            self.remainingTime -= 1
            if self.remainingTime == 0:
                self.gameLost = True

    def redrawAll(self, screen):
        #Setting up RGB values for later use
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        #Defining redraw for the menu
        if self.gameMode == 'Menu':
            #Defining and drawing rects for different buttons
            rect1 = (150, 100, 200, 100)
            rect2 = (150, 300, 200, 100)
            pygame.draw.rect(screen, black, rect1, 5)
            pygame.draw.rect(screen, black, rect2, 5)
            myfont = pygame.font.SysFont('Arial', 50)
            textsurface1 = myfont.render('Image', True, black)
            textsurface2 = myfont.render('Maze', True, black)
            screen.blit(textsurface1,(195,120))
            screen.blit(textsurface2,(200,320))
        #Redraw for image slide puzzle mode
        if self.gameMode == 'Image':
            myfont = pygame.font.SysFont('Arial', 35)
            if self.gameWon: # Displaying a message when game is won
                r = (0, 0, self.width, self.height)
                pygame.draw.rect(screen, white, r)
                winfont = pygame.font.SysFont('Arial', 60)
                wintext = winfont.render('You Won!', True, green)
                screen.blit(wintext, (150, 150))
                pygame.draw.rect(screen, black, (175, 312.5, 150, 75), 5)
                #Creating a button to return to menu once won
                menutext = myfont.render('Menu', True, black)
                screen.blit(menutext, (215, 330))
                return
            #Drawing option boxes at bottom of screen
            pygame.draw.rect(screen, blue, (0, 500, 500, 100))
            pygame.draw.line(screen, black, (166, 500), (166, 600), 5)
            pygame.draw.line(screen, black, (333, 500), (333, 600), 5)
            self.blocks.draw(screen)
            textsurface1 = myfont.render('Hint', True, black)
            textsurface2 = myfont.render('Menu', True, black)
            textsurface3 = myfont.render('Solve', True, black)
            screen.blit(textsurface1, (390, 530))
            screen.blit(textsurface2, (45, 530))
            screen.blit(textsurface3, (215, 530))
            #If hints are activated, numbers representing desired final
            #location will show up on the pieces
            if self.hint:
                for block in self.blocks:
                    #Skipping over the blank space for this
                    if isinstance(block, Blank):
                        continue
                    num = int(block.index)
                    hintfont = pygame.font.SysFont('Arial', 20, True)
                    numsurface = hintfont.render('%d'%num, True, white)
                    shadow = hintfont.render('%d'%num, True, black)
                    '''
                    Artificially creating an outline for the hint text, so it 
                    can be read on any color image. Basically, creating a black 
                    number in every direction around the original number, one 
                    pixel off, then drawing the number in white on top
                    '''
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 2, 
                                                block.y - self.blockWidth/2))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 4, 
                                                block.y - self.blockWidth/2))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 3, 
                                                block.y - self.blockWidth/2+1))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 3,
                                                block.y - self.blockWidth/2-1))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 2, 
                                                block.y - self.blockWidth/2-1))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 2, 
                                                block.y - self.blockWidth/2+1))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 4, 
                                                block.y - self.blockWidth/2-1))
                    screen.blit(shadow,     (   block.x - self.blockWidth/2 + 4, 
                                                block.y - self.blockWidth/2+1))
                    screen.blit(numsurface, (   block.x - self.blockWidth/2 + 3,
                                                block.y - self.blockWidth/2))
        if self.gameMode == 'Maze':
            myfont = pygame.font.SysFont('Arial', 35)
            #Drawing win and lose screens, with option to return to menu
            #Soon: Next level/try again buttons
            if self.gameLost:
                r = (0, 0, self.width, self.height)
                pygame.draw.rect(screen, white, r)
                lossfont = pygame.font.SysFont('Arial', 60)
                losstext = lossfont.render('You Lost!', True, red)
                screen.blit(losstext, (150, 150))
                pygame.draw.rect(screen, black, (175, 312.5, 150, 75), 5)
                menutext = myfont.render('Menu', True, black)
                screen.blit(menutext, (215, 330))
                return
            if self.gameWon:
                r = (0, 0, self.width, self.height)
                pygame.draw.rect(screen, white, r)
                winfont = pygame.font.SysFont('Arial', 60)
                wintext = winfont.render('You Won!', True, green)
                screen.blit(wintext, (150, 150))
                pygame.draw.rect(screen, black, (175, 312.5, 150, 75), 5)
                menutext = myfont.render('Menu', True, black)
                screen.blit(menutext, (215, 330))
                return
            #Drawing remaining moves/time, and menu button
            pygame.draw.rect(screen, blue, (0, 500, 500, 100))
            pygame.draw.line(screen, black, (166, 500), (166, 600), 5)
            pygame.draw.line(screen, black, (333, 500), (333, 600), 5)
            self.blocks.draw(screen)
            self.playerSprite.draw(screen)
            pygame.draw.rect(screen, green, ((7/8)*self.width - 25, 
            (7/8)*self.width - 25, 50, 50), 5)
            textsurface1 = myfont.render(  'Moves: %d' %self.remainingMoves, 
                                            True, black)
            textsurface2 = myfont.render('Menu', True, black)
            textsurface3 = myfont.render(   'Time: %d' %self.remainingTime,
                                            True, black)
            screen.blit(textsurface1, (355, 530))
            screen.blit(textsurface2, (45, 530))
            screen.blit(textsurface3, (195, 530))
#Running the game
Game(500, 600).run()