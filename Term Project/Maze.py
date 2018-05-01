from Block import Block
from MazeObj import Trap, Hole, Enemy, Point, Blank, MazeBlock, Player
import pygame
import random

'''
Note: to be able to see all levels without completing them, change
self.maxLevel to 5
'''

class Maze(object):
    def init(self):
        self.maxLevel = 5
        self.level = 0
        self.mouseClicks = 0
        self.width = 500
        self.height = 600
        self.c = 10
        self.fps = 50
        self.move = None
        self.moveCount = 0
        self.gameMode = 'Maze'
        self.gameWon = False
        self.gameLost = False
        self.blocks = pygame.sprite.Group()
        self.rows = 4
        self.blockWidth = self.width / self.rows
        MazeBlock.init()
        self.timerCalled = 0
        self.maze = []
        self.getLevelBlocks(self, self.level)
        Point.init()
        self.points = pygame.sprite.Group()
        Trap.init()
        self.traps = pygame.sprite.Group()
        Enemy.init()
        self.enemies = pygame.sprite.Group()
        Hole.init()
        self.hole = pygame.sprite.Group()
    
    def getLevelBlocks(self, level):
        #Level = 0 means menu, so no blocks needed
        if level == 0:
            return
        #Creating the maze pieces
        cross = (True, True, True, True)
        upt = (True, True, False, True)
        downt = (False, True, True, True)
        rightt = (True, True, True, False)
        leftt = (True, False, True, True)
        tlc = (True, False, False, True)
        trc = (True, True, False, False)
        blc = (False, False, True, True)
        brc = (False, True, True, False)
        blank = (False, False, False, False)
        vert = (True, False, True, False)
        horz = (False, True, False, True)
        #Emptying sprites and resetting timer every time a level is loaded
        self.blocks.empty()
        self.points.empty()
        self.enemies.empty()
        self.traps.empty()
        self.hole.empty()
        self.timerCalled = 0
        self.move = None
        self.moveCount = 0
        #Creating the levels
        if level == 1:
            self.rows = 4
            self.blockWidth = self.width / self.rows
            #Each level is constricted by different time/ num moves
            self.remainingMoves = 30
            self.remainingTime = 30
            self.maze = [   horz, vert, cross, downt, 
                            blank, tlc, trc, blc, 
                            brc, blank, horz, blank, 
                            horz, upt, blank]    
        if level == 2:
            self.rows = 4
            self.blockWidth = self.width / self.rows
            self.remainingMoves = 50
            self.remainingTime = 50
            self.maze = [   brc, blank, cross, upt, 
                            downt, trc, blank, vert, 
                            horz, blank, trc, blank, 
                            vert, cross, blank]
            w = self.blockWidth / 2
            #Adding the cheese
            self.points.add(Point(w, w*7, 4))
            self.points.add(Point(w*3, w*3, 4))
            self.points.add(Point(w*7, w*5, 4))
        if level == 3:
            self.rows = 5
            self.blockWidth = self.width / self.rows
            self.remainingMoves = 60
            self.remainingTime = 60
            self.maze = [   brc, tlc, rightt, blank, horz,
                            downt, blank, cross, blc, blank,
                            upt, vert, blank, trc, blank,
                            blank, blc, vert, blank, horz, 
                            cross, leftt, blank, vert] 
            w = self.blockWidth / 2
            #Adding mousetraps
            self.traps.add(Trap(w*7, w*3, 5))
            self.traps.add(Trap(w*7, w*7, 5))
            self.traps.add(Trap(w*5, w*7, 5))
            self.traps.add(Trap(w*3, w*3, 5))
        if level == 4:
            self.rows = 5
            self.blockWidth = self.width / self.rows
            self.remainingMoves = 75
            self.remainingTime = 75
            self.maze = [   brc, vert, blank, upt, tlc, 
                            blank, blc, blank, blank, cross, 
                            cross, trc, tlc, vert, horz, 
                            blank, blc, blank, brc, upt, 
                            blank, downt, cross, blank]
        if level == 5:
            self.rows = 6
            self.blockWidth = self.width / self.rows
            self.remainingMoves = 200
            self.remainingTime = 200
            self.maze = [   brc, vert, upt, rightt, blank, tlc,
                            blc, blank, leftt, blank, cross, horz,
                            trc, downt, blank, vert, brc, blank,
                            blank, horz, blc, blank, upt, downt,
                            tlc, blank, horz, cross, blank, brc,
                            trc, leftt, rightt, blank, vert]
            w = self.blockWidth / 2
            self.traps.add(Trap(w*7, w*5, 6))
            self.traps.add(Trap(w*9, w*9, 6))
            self.traps.add(Trap(w, w*7, 6))
            self.points.add(Point(w*11, w, 6))
            self.points.add(Point(w*7, w*7, 6))
            self.points.add(Point(w, w*11, 6))
        if level == 'RAND':
            self.createRandom(self)
        self.coords = []
        MazeBlock.board = []
        self.playerIndex = 0
        #Creating the coordinates of the maze blocks
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
        #Making blocks and adding to sprite group
        for i in range(self.rows**2-1):
            self.blocks.add(MazeBlock(self.coords[i][0], self.coords[i][1],
            self.maze[i], self.rows))
        #Loading up the blank and adding it to sprite group
        Blank.init()
        blankInitial = self.width * ((self.rows * 2 - 1) / (self.rows * 2))
        self.blocks.add(Blank(blankInitial, blankInitial, self.rows))
        #Initiating the player
        Player.init()
        self.player = Player(self.blockWidth/2, self.blockWidth/2, self.rows, 'S')
        self.playerSprite = pygame.sprite.Group()
        self.playerSprite.add(self.player)
        #Creating end goal (hole)
        w = ((self.rows**2-(self.rows/2))/(self.rows**2))*self.width
        hole = Hole(w, w, self.rows)
        self.hole.add(hole)
    
    def createRandom(self):
        #Creating the maze pieces
        cross = (True, True, True, True)
        upt = (True, True, False, True)
        downt = (False, True, True, True)
        rightt = (True, True, True, False)
        leftt = (True, False, True, True)
        tlc = (True, False, False, True)
        trc = (True, True, False, False)
        blc = (False, False, True, True)
        brc = (False, True, True, False)
        blank = (False, False, False, False)
        vert = (True, False, True, False)
        horz = (False, True, False, True)
        blockList = [cross, upt, downt, rightt, leftt, tlc, trc, blc, brc,
        vert, horz]
        #Emptying sprites and resetting timer every time a level is loaded
        self.blocks.empty()
        self.points.empty()
        self.enemies.empty()
        self.traps.empty()
        self.hole.empty()
        self.timerCalled = 0
        self.move = None
        self.moveCount = 0
        self.maze = []
        self.rows = 6
        self.blockWidth = self.width / self.rows
        self.remainingMoves = 200
        self.remainingTime = 200
        seen = set()
        for i in range(10):
            self.maze.append(blank)
        for j in range(25):
            self.maze.append(random.choice(blockList))
        random.shuffle(self.maze)
        self.maze[0] = brc
        for k in range(3):
            w = self.blockWidth / 2
            r1 = random.choice(range(3, 10, 2))
            r2 = random.choice(range(3, 10, 2))
            while (r1, r2) in seen:
                r1 = random.choice(range(3, 10, 2))
                r2 = random.choice(range(3, 10, 2))
            seen.add((r1, r2))
            self.traps.add(Trap(w*r1, w*r2, 6))
            r3 = random.choice(range(3, 10, 2))
            r4 = random.choice(range(3, 10, 2))
            while (r3, r4) in seen:
                r3 = random.choice(range(3, 10, 2))
                r4 = random.choice(range(3, 10, 2))
            seen.add((r3, r4))
            self.points.add(Point(w*r3, w*r4, 6))
        
    def mousePressedMenu(self, x, y):
        #Ignore the first click because it transfers from menu screen
        self.mouseClicks += 1
        if self.mouseClicks == 1:
            return
        #Level buttons
        if 225 < y < 275:
            if 25 < x < 75:
                #maxLevel is highest level player is allowed to enter
                if self.maxLevel >= 1:
                    self.level = 1
            if 125 < x < 175:
                if self.maxLevel >= 2:
                    self.level = 2
            if 225 < x < 275:
                if self.maxLevel >= 3:
                    self.level = 3
            if 325 < x < 375:
                if self.maxLevel >= 4:
                    self.level = 4
            if 425 < x < 475:
                if self.maxLevel >= 5:
                    self.level = 5
        if 175 < x < 325 and 500 < y < 575:
            self.gameMode = 'Menu'
        if 175 < x < 325 and 350 < y < 425:
            self.level = 'RAND'
        #Getting the blocks for chosen level
        self.getLevelBlocks(self, self.level)

    def mousePressed(self, x, y):
        if self.level == 0: #menu condition
            self.mousePressedMenu(self, x, y)
            return 
        #Out of bounds check
        if not 0 < x < self.width or not 0 < y < self.height:
            return
        #Option to return to level select if game is won or lost
        if self.gameWon or self.gameLost:
            if 175 < x < 325 and 312 < y < 388:
                self.level = 0
                self.gameWon = False
                self.gameLost = False
            return
        #Can't move blocks while mouse is moving:
        if self.move != None:
            return
        #Can't move block with player on it
        if  abs(self.player.x - x) < self.blockWidth / 2 and \
            abs(self.player.y - y) < self.blockWidth / 2 :
            return
        #Level select button in game
        if 500 < y < 600:
            if 0 < x < 166:
                self.level = 0
            return
        #Calculating indexes of blank and click to compare for valid move test
        self.bI = MazeBlock.board.index(0)
        self.bX = self.bI % self.rows
        self.bY = self.bI // self.rows
        cX = x // self.blockWidth
        cY = y // self.blockWidth
        i  = int(cY * self.rows + cX)
        dx, dy = 0, 0
        if abs(self.bX-cX) + abs(self.bY-cY) == 1: #If valid move
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
    
    def movePlayer(self, dir):
        x, y = self.player.x, self.player.y
        if dir == 'N':
            d = self.blockWidth / self.c
            self.player.update(x, y-d, self.width, self.height)
        if dir == 'E':
            d = self.blockWidth / self.c
            self.player.update(x+d, y, self.width, self.height)
        if dir == 'S':
            d = self.blockWidth / self.c
            self.player.update(x, y+d, self.width, self.height)
        if dir == 'W':
            d = self.blockWidth / self.c
            self.player.update(x-d, y, self.width, self.height)

    def keyPressed(self, keyCode, modifier):
        if self.level == 0:
            return
        if self.move != None:
            return
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
                x, y = self.player.x, self.player.y
                self.playerSprite.empty()
                self.player = Player(x, y, self.rows, 'E')
                self.playerSprite.add(self.player)
                self.move = 'E'
                self.playerIndex += 1
        #Same but for other directions:
        if keyCode == pygame.K_w:
            if self.playerIndex // self.rows == 0:
                return
            if MazeBlock.board[self.playerIndex-self.rows] == 0:
                return
            if  MazeBlock.board[self.playerIndex][0] and \
                MazeBlock.board[self.playerIndex-self.rows][2]:
                x, y = self.player.x, self.player.y
                self.playerSprite.empty()
                self.player = Player(x, y, self.rows, 'N')
                self.playerSprite.add(self.player)
                self.move = 'N'
                self.playerIndex -= self.rows
        if keyCode == pygame.K_a:
            if self.playerIndex % self.rows == 0:
                return
            if MazeBlock.board[self.playerIndex-1] == 0:
                return
            if  MazeBlock.board[self.playerIndex][3] and \
                MazeBlock.board[self.playerIndex-1][1]:
                x, y = self.player.x, self.player.y 
                self.playerSprite.empty()
                self.player = Player(x, y, self.rows, 'W')
                self.playerSprite.add(self.player)
                self.move = 'W'
                self.playerIndex -= 1
        if keyCode == pygame.K_s:
            if self.playerIndex // self.rows == self.rows - 1:
                return
            if MazeBlock.board[self.playerIndex+self.rows] == 0:
                return
            if  MazeBlock.board[self.playerIndex][2] and \
                MazeBlock.board[self.playerIndex+self.rows][0]:
                x, y = self.player.x, self.player.y
                self.playerSprite.empty()
                self.player = Player(x, y, self.rows, 'S')
                self.playerSprite.add(self.player)
                self.move = 'S'
                self.playerIndex += self.rows
    
    #Creates an enemy coming from a random direction
    def spawnEnemy(self):
        dir1 = random.choice(['V', 'H']) #Determining vertical or horizontal
        i = random.randint(0, self.rows - 1) #Determining index (row/col num)
        if dir1 == 'V':
            dir2 = random.choice(['U', 'D']) #If vertical, choosing up or down
        if dir1 == 'H':
            dir2 = random.choice(['L', 'R']) #If horiz, choosing left or right
        self.enemies.add(Enemy(dir1, dir2, i, self.rows))
    
    #Moves the enemy based off of its defined velocity from its direction
    def moveEnemy(self):
        for enem in self.enemies:
            newX = enem.x + enem.vx
            newY = enem.y + enem.vy
            enem.update(newX, newY, self.width, self.height)

    def timerFired(self, dt):
        #Timerfired not needed for menu
        if self.level == 0:
            return
        if self.gameLost or self.gameWon:
            return
        self.timerCalled += 1
        #Decreasing remaining time every second
        if self.timerCalled % self.fps == 0:
            self.remainingTime -= 1
            #Player loses if time runs out
            if self.remainingTime == 0:
                self.gameLost = True
        #Spawning enemies
        if self.level in [4, 5, 'RAND']:
            if self.timerCalled % 120 == 0:
                if self.timerCalled > 300:
                    self.spawnEnemy(self)
            self.moveEnemy(self)
        if self.move != None:
            self.movePlayer(self, self.move)
            self.moveCount += 1
            if self.moveCount == self.c:
                self.move = None
                self.moveCount = 0
        for pt in pygame.sprite.groupcollide(self.points, self.playerSprite,
        True, False, pygame.sprite.collide_circle):
            #If mouse and cheese collide, delete cheese
            pt.update(self.width, self.height)
        if pygame.sprite.groupcollide(self.traps, self.playerSprite, False, False,
        pygame.sprite.collide_circle):
            #If mouse and mousetrap collide, lose level
            self.gameLost = True
        for enem in self.enemies:
            if  enem.x > 600 or enem.x < -100 or \
                enem.y > 600 or enem.y < -100:
                #Deletes enemies once out of bounds
                self.enemies.remove(enem)
        if pygame.sprite.groupcollide(self.playerSprite, self.enemies,
        False, False, pygame.sprite.collide_circle):
            self.gameLost = True
            #If mouse collides with cat, game over
        if pygame.sprite.groupcollide(self.playerSprite, self.hole,
        False, False, pygame.sprite.collide_circle):
            if self.level == 2 or self.level == 5:
                if len(self.points) == 0:
                    if self.level == self.maxLevel:
                        self.maxLevel += 1
                    self.gameWon = True
            else:
                if self.level == self.maxLevel:
                    self.maxLevel += 1
                self.gameWon = True
    
    def redrawAll(self, screen):
        #Setting up RGB values
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        yellow = (255, 255, 0)
        #Creating a font
        myfont = pygame.font.SysFont('Arial', 35)
        if self.level == 0:
            #Drawing level selection screen
            r = (0, 0, self.width, self.height)
            pygame.draw.rect(screen, white, r)
            titletext = myfont.render('Select Level:', True, black)
            screen.blit(titletext, (170, 100))
            rls = [ (25, 225, 50, 50),
                    (125, 225, 50, 50),
                    (225, 225, 50, 50),
                    (325, 225, 50, 50),
                    (425, 225, 50, 50)]
            #Completed levels show up green, incomplete red, and current yellow
            for i in range(len(rls)):
                color = red
                if i + 1 < self.maxLevel:
                    color = green
                if i + 1 == self.maxLevel:
                    color = yellow
                pygame.draw.rect(screen, color, rls[i])
                pygame.draw.rect(screen, black, rls[i], 5)
                leveltext = myfont.render('%d'%(i+1), True, black)
                screen.blit(leveltext, (42+(i*100), 228))
            #Drawing menu and random button
            menurect = (175, 500, 150, 75)
            pygame.draw.rect(screen, black, menurect, 5)
            menutext = myfont.render('Menu', True, black)
            screen.blit(menutext, (215, 517))
            randomrect = (175, 350, 150, 75)
            pygame.draw.rect(screen, black, randomrect, 5)
            randomtext = myfont.render('Random', True, black)
            screen.blit(randomtext, (195, 365))
            return 
        #Drawing win and lose screens, with option to return to level selection
        if self.gameLost:
            r = (0, 0, self.width, self.height)
            pygame.draw.rect(screen, white, r)
            lossfont = pygame.font.SysFont('Arial', 60)
            losstext = lossfont.render('You Lost!', True, red)
            screen.blit(losstext, (150, 150))
            pygame.draw.rect(screen, black, (175, 312.5, 150, 75), 5)
            menutext = myfont.render('Levels', True, black)
            screen.blit(menutext, (210, 330))
            return
        if self.gameWon:
            r = (0, 0, self.width, self.height)
            pygame.draw.rect(screen, white, r)
            winfont = pygame.font.SysFont('Arial', 60)
            wintext = winfont.render('You Won!', True, green)
            screen.blit(wintext, (150, 150))
            pygame.draw.rect(screen, black, (175, 312.5, 150, 75), 5)
            menutext = myfont.render('Levels', True, black)
            screen.blit(menutext, (210, 330))
            return
        #Drawing blocks
        self.blocks.draw(screen)
        #Fixing one weird graphical issue with scaling
        if self.level == 5 or self.level == 'RAND':
            pygame.draw.line(screen, black, (249, 0), (249, 500), 1)
            pygame.draw.line(screen, black, (0, 249), (500, 249), 1)
        #Drawing hole
        self.hole.draw(screen)
        #Drawing enemies
        self.enemies.draw(screen)
        #Drawing remaining moves/time, and menu button
        pygame.draw.rect(screen, blue, (0, 500, 500, 100))
        pygame.draw.line(screen, black, (166, 500), (166, 600), 5)
        pygame.draw.line(screen, black, (333, 500), (333, 600), 5)
        pygame.draw.line(screen, black, (0, 500), (500, 500), 5)
        L1 = (1/5)*self.blockWidth
        L2 = (2/5)*self.blockWidth
        L3 = ((self.rows*2-1) / (self.rows*2))*self.width
        textsurface1 = myfont.render(  'Moves: %d' %self.remainingMoves, 
                                        True, black)
        textsurface2 = myfont.render('Levels', True, black)
        textsurface3 = myfont.render(   'Time: %d' %self.remainingTime,
                                        True, black)
        screen.blit(textsurface1, (355, 530))
        screen.blit(textsurface2, (40, 530))
        screen.blit(textsurface3, (195, 530))
        #Drawing special level conditions
        self.points.draw(screen)
        self.traps.draw(screen)
        #drawing player
        self.playerSprite.draw(screen)