from pygamegame import PygameGame
from Image import Image
from Maze import Maze
from Race import Race
import pygame
import time
pygame.font.init()

#upgrade ui, solver, image uploader

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
        if self.gameMode == 'Race':
            Race.mousePressed(Race, x, y)
            self.gameMode = Race.gameMode
        if self.gameMode == 'Maze':
            Maze.mousePressed(Maze, x, y)
            self.gameMode = Maze.gameMode
    
    def mousePressedMenu(self, x, y):
        #Selecting different modes from menu
        if 150 < x < 350 and 100 < y < 200:
            Image.init(Image)
            self.gameMode = 'Image'
        if 150 < x < 350 and 250 < y < 350:
            Race.init(Race)
            self.gameMode = 'Race'
        if 150 < x < 350 and 400 < y < 500:
            Maze.init(Maze)
            self.gameMode = 'Maze'
    
    def keyPressed(self, keyCode, modifier):
        if self.gameMode == 'Maze':
            Maze.keyPressed(Maze, keyCode, modifier)

    def timerFired(self, dt):
        #Timer only needed in maze and race
        if self.gameMode == 'Maze':
            Maze.timerFired(Maze, dt)
        if self.gameMode == 'Race':
            Race.timerFired(Race, dt)

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
            rect2 = (150, 250, 200, 100)
            rect3 = (150, 400, 200, 100)
            pygame.draw.rect(screen, black, rect1, 5)
            pygame.draw.rect(screen, black, rect2, 5)
            pygame.draw.rect(screen, black, rect3, 5)
            myfont = pygame.font.SysFont('Arial', 50)
            textsurface1 = myfont.render('Practice', True, black)
            textsurface2 = myfont.render('Race', True, black)
            textsurface3 = myfont.render('Maze', True, black)
            screen.blit(textsurface1,(175, 120))
            screen.blit(textsurface2,(200, 270))
            screen.blit(textsurface3,(200, 420))
        #Redraw for image, race, and maze modes
        if self.gameMode == 'Image':
            Image.redrawAll(Image, screen)
        if self.gameMode == 'Race':
            Race.redrawAll(Race, screen)
        if self.gameMode == 'Maze':
            Maze.redrawAll(Maze, screen)
#Running the game
Game(500, 600).run()