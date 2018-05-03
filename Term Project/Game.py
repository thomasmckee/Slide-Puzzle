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
        blue2 = (43, 108, 119)
        blue3 = (156, 199, 211)
        grey = (61, 61, 61)
        #Defining redraw for the menu
        if self.gameMode == 'Menu':
            backrect = (0, 0, 500, 600)
            pygame.draw.rect(screen, blue3, backrect)
            #Defining and drawing rects for different buttons
            rect1 = (25, 325, 200, 100)
            rect2 = (25, 475, 200, 100)
            rect3 = (275, 325, 200, 100)
            rect4 = (275, 475, 200, 100)
            pygame.draw.rect(screen, blue2, rect1)
            pygame.draw.rect(screen, blue2, rect2)
            pygame.draw.rect(screen, blue2, rect3)
            pygame.draw.rect(screen, blue2, rect4)
            pygame.draw.rect(screen, grey, rect1, 5)
            pygame.draw.rect(screen, grey, rect2, 5)
            pygame.draw.rect(screen, grey, rect3, 5)
            pygame.draw.rect(screen, grey, rect4, 5)
            myfont = pygame.font.SysFont('Arial', 50)
            myfont2 = pygame.font.SysFont('Arial', 60, True)
            textsurface1 = myfont.render('Practice', True, black)
            textsurface2 = myfont.render('Race', True, black)
            textsurface3 = myfont.render('Maze', True, black)
            textsurface4 = myfont.render('Upload', True, black)
            ts1rect = textsurface1.get_rect(center=(125, 375))
            ts2rect = textsurface3.get_rect(center=(375, 375))
            ts3rect = textsurface2.get_rect(center=(125, 525))
            ts4rect = textsurface4.get_rect(center=(375, 525))
            screen.blit(textsurface1,ts1rect)
            screen.blit(textsurface2,ts2rect)
            screen.blit(textsurface3,ts3rect)
            screen.blit(textsurface4,ts4rect)
            titletext = myfont2.render('Slide Puzzle Game', True, black)
            titletextrect = titletext.get_rect(center=(self.width/2, 100))
            screen.blit(titletext, titletextrect)
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