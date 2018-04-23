from Blank import Blank
from Block import Block
import pygame

class Image(object):
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
        
    def init(self):
        self.gameMode = 'Image'
        self.width = 500
        self.height = 600
        self.hint = False
        self.gameWon = False
        Block.init()
        self.blocks = pygame.sprite.Group()
        self.rows = 4
        self.puzzleWidth = 500
        self.blockWidth = self.puzzleWidth / self.rows
        self.boardL = self.rows**2-1
        for i in range(self.rows):
            for j in range(self.rows):
                #Not taking the last block, as it is supposed to be blank
                if i+j == (self.rows-1)*2:
                    continue
                #Calculating location of blocks and adding them to sprite group
                x = j*(self.blockWidth)+(self.blockWidth/2)
                y = i*(self.blockWidth)+(self.blockWidth/2)
                self.blocks.add(Block(x, y))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.puzzleWidth * (7/8)
        self.blocks.add(Blank(blankInitial, blankInitial, self.rows))
        #If the board that was created is not valid, make a new one until it is
        if not self.isValidBoard(self, Block.board):
            self.init(self)
            return
    def mousePressed(self, x, y):
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
    
    def redrawAll(self, screen):
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
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
    