from Block import Block, Blank
import pygame
import copy
import math

class Race(object):
#Information about valid board states taken from this website:
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
    #However, all of this code is original
    def isValidBoard(self, board):
        if board == list(range(len(board))):
            return True
        inversions = 0
        for i in range(len(board)):
            if i == 15:
                pass
            check = board[i:]
            for j in check:
                if board[i] > j:
                    inversions += 1
        if len(board) % 2 == 1:
            if inversions % 2 == 0:
                return True
        elif len(board) % 2 == 0:
            if board.index(self.boardL)//self.rows % 2 == 0:
                if inversions % 2 == 1:
                    return True
            elif board.index(self.boardL)//self.rows % 2 == 1:
                if inversions % 2 == 0:
                    return True
        return False
        
    def init(self):
        self.gameMode = 'Race'
        self.timerCalled = 0
        self.player = 0
        self.width = 500
        self.height = 600
        self.hint = False
        self.p1Finished = False
        self.p2Finished = False
        self.p1Time = 0
        self.p2Time = 0
        self.clicks = 0
        Block.init()
        self.blocks = pygame.sprite.Group()
        self.rows = 4
        self.puzzleWidth = 500
        self.blockWidth = self.puzzleWidth / self.rows
        self.boardL = self.rows**2-1
        self.coords = []
        for i in range(self.rows):
            for j in range(self.rows):
                #Not taking the last block, as it is supposed to be blank
                if i+j == (self.rows-1)*2:
                    continue
                #Calculating location of blocks and adding them to sprite group
                x = j*(self.blockWidth)+(self.blockWidth/2)
                y = i*(self.blockWidth)+(self.blockWidth/2)
                self.coords.append((x, y))
                self.blocks.add(Block(x, y))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.puzzleWidth * (7/8)
        self.blocks.add(Blank(blankInitial, blankInitial, self.rows))
        #If the board that was created is not valid, make a new one until it is
        if not self.isValidBoard(self, Block.board):
            self.init(self)
            return
        self.board = copy.deepcopy(Block.board)
    
    def mousePressed(self, x, y):
        #Ignoring first click because of some weird bug:
        self.clicks += 1
        if self.clicks == 1:
            return
        #Out of bounds check
        if not 0 < x < self.width or not 0 < y < self.height:
            return
        if self.player == 0:
            if 200 < x < 300 and 300 < y < 375:
                self.player = 1
            return
        if self.player == 1 and self.p1Finished:
            if 200 < x < 300 and 300 < y < 375:
                self.player = 2
            return
        if self.player == 2 and self.p2Finished:
            if 200 < x < 300 and 300 < y < 375:
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
        #Win condition
        if Block.board == list(range(self.boardL+1)):
            if self.player == 1:
                self.blocks.empty()
                Block.board = []
                for i in range(15):
                    x, y = self.coords[i][0], self.coords[i][1]
                    index = self.board[i]
                    self.blocks.add(Block(x, y, index))
                    blankInitial = self.puzzleWidth * (7/8)
                    self.blocks.add(Blank(blankInitial, blankInitial, self.rows))
                self.p1Finished = True
            if self.player == 2:
                self.p2Finished = True
    
    def timerFired(self, dt):
        if self.player == 0:
            return
        if self.player == 1 and not self.p1Finished:
            self.p1Time += 1
        if self.player == 2 and not self.p2Finished:
            self.p2Time += 1
    
    def drawBoard(self, screen):
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        myfont = pygame.font.SysFont('Arial', 35)
        self.blocks.draw(screen)
        pygame.draw.rect(screen, blue, (0, 500, 500, 100))
        pygame.draw.line(screen, black, (166, 500), (166, 600), 5)
        pygame.draw.line(screen, black, (333, 500), (333, 600), 5)
        textsurface1 = myfont.render('Hint', True, black)
        textsurface2 = myfont.render('Menu', True, black)
        if self.player == 1:
            textsurface3 = myfont.render('Time: %d'%(self.p1Time//50), True, 
            black)
        else:
            textsurface3 = myfont.render('Time: %d'%(self.p2Time//50), True, 
            black)
        screen.blit(textsurface1, (390, 530))
        screen.blit(textsurface2, (45, 530))
        screen.blit(textsurface3, (180, 530))
        #If hints are activated, numbers representing desired final
        #location will show up on the pieces
        if self.hint:
            for block in self.blocks:
                #Skipping over the blank space for this
                if isinstance(block, Blank):
                    continue
                num = int(block.index) + 1
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
    
    def redrawAll(self, screen):
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        myfont = pygame.font.SysFont('Arial', 35)
        if self.player == 0:
            startrect = (200, 300, 100, 75)
            pygame.draw.rect(screen, black, startrect, 5)
            starttext = myfont.render('Start', True, black)
            screen.blit(starttext, (218, 315))
            playertext = myfont.render("Player 1's turn", True, black)
            screen.blit(playertext, (160, 100))
        if self.player == 1:
            if self.p1Finished:
                startrect = (200, 300, 100, 75)
                pygame.draw.rect(screen, black, startrect, 5)
                starttext = myfont.render('Start', True, black)
                screen.blit(starttext, (218, 315))
                playertext = myfont.render("Player 2's turn", True, black)
                screen.blit(playertext, (160, 200))
                timetext = myfont.render("Player 1's Time: %0.1f"%(self.p1Time / 50),
                True, black)
                screen.blit(timetext, (115, 100))
            else:
                self.drawBoard(self, screen)
        if self.player == 2:
            if self.p2Finished:
                menurect = (200, 300, 100, 75)
                pygame.draw.rect(screen, black, menurect, 5)
                menutext = myfont.render('Menu', True, black)
                screen.blit(menutext, (216, 315))
                if self.p1Time < self.p2Time:
                    wintext = myfont.render("Player 1 Wins!", True, black)
                else:
                    wintext = myfont.render("Player 2 Wins!", True, black)
                screen.blit(wintext, (160, 200))
                timetext = myfont.render("Player 2's Time: %0.1f"%(self.p2Time / 50),
                True, black)
                screen.blit(timetext, (115, 100))
            else:
                self.drawBoard(self, screen)
    