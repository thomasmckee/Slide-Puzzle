from pygamegame import PygameGame
from Image import Image
from Maze import Maze
from Race import Race
from Uploader import Uploader
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
        if self.gameMode == 'Uploader':
            Uploader.mousePressed(Uploader, x, y)
            self.gameMode = Uploader.gameMode
    
    def mousePressedMenu(self, x, y):
        #Selecting different modes from menu
        if 25 < x < 225 and 325 < y < 425:
            Image.init(Image)
            self.gameMode = 'Image'
        if 275 < x < 475 and 325 < y < 425:
            Race.init(Race)
            self.gameMode = 'Race'
        if 25 < x < 225 and 475 < y < 575:
            Maze.init(Maze)
            self.gameMode = 'Maze'
        if 275 < x < 475 and 475 < y < 575:
            Uploader.init(Uploader)
            self.gameMode = 'Uploader'
    
    def keyPressed(self, keyCode, modifier):
        if self.gameMode == 'Maze':
            Maze.keyPressed(Maze, keyCode, modifier)
        if self.gameMode == 'Uploader':
            Uploader.keyPressed(Uploader, keyCode, modifier)

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
            rect1 = (25, 325, 200, 100)
            rect2 = (25, 475, 200, 100)
            rect3 = (275, 325, 200, 100)
            rect4 = (275, 475, 200, 100)
            pygame.draw.rect(screen, black, rect1, 5)
            pygame.draw.rect(screen, black, rect2, 5)
            pygame.draw.rect(screen, black, rect3, 5)
            pygame.draw.rect(screen, black, rect4, 5)
            myfont = pygame.font.SysFont('Arial', 50)
            textsurface1 = myfont.render('Practice', True, black)
            textsurface2 = myfont.render('Race', True, black)
            textsurface3 = myfont.render('Maze', True, black)
            textsurface4 = myfont.render('Upload', True, black)
            screen.blit(textsurface1,(50, 342))
            screen.blit(textsurface2,(325, 342))
            screen.blit(textsurface3,(75, 492))
            screen.blit(textsurface4,(308, 492))
            titletext = myfont.render('Slide Puzzle Game', True, black)
            screen.blit(titletext, (75, 75))
        #Redraw for image, race, and maze modes
        if self.gameMode == 'Image':
            Image.redrawAll(Image, screen)
        if self.gameMode == 'Race':
            Race.redrawAll(Race, screen)
        if self.gameMode == 'Maze':
            Maze.redrawAll(Maze, screen)
        if self.gameMode == 'Uploader':
            Uploader.redrawAll(Uploader, screen)
#Running the game
Game(500, 600).run()