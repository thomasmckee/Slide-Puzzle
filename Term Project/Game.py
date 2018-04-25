from pygamegame import PygameGame
from Image import Image
from Maze import Maze
import pygame
import time
pygame.font.init()

class Game(PygameGame):
    #Init for start, the menu
    def init(self):
        self.gameMode = 'Menu'
    
    def mousePressed(self, x, y):
        #Different mousepressed fcts depending where in interface
        if self.gameMode == 'Menu':
            self.mousePressedMenu(x, y)
        if self.gameMode == 'Image':
            Image.mousePressed(Image, x, y)
            self.gameMode = Image.gameMode
        if self.gameMode == 'Maze':
            Maze.mousePressed(Maze, x, y)
            self.gameMode = Maze.gameMode
    
    def mousePressedMenu(self, x, y):
        #Selecting different modes from menu
        if 150 < x < 350 and 100 < y < 200:
            Image.init(Image)
            self.gameMode = 'Image'
        if 150 < x < 350 and 300 < y < 400:
            Maze.init(Maze)
            self.gameMode = 'Maze'
    
    def keyPressed(self, keyCode, modifier):
        if self.gameMode == 'Maze':
            Maze.keyPressed(Maze, keyCode, modifier)

    def timerFired(self, dt):
        #Timer only needed in maze
        if self.gameMode == 'Maze':
            Maze.timerFired(Maze, dt)

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
            Image.redrawAll(Image, screen)
        if self.gameMode == 'Maze':
            Maze.redrawAll(Maze, screen)
#Running the game
Game(500, 600).run()