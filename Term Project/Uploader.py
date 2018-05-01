import pygame
import os
import sys
pygame.font.init()

class Uploader(object):
    def init(self):
        self.tempName = ''
        self.fileName = ''
        self.path = 'images/'
        self.done = False
        self.invalidName = False
        self.validName = False
        self.invalidFile = False
        self.gameMode = 'Uploader'
        
    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_RETURN:
            #Once user presses enter, check if path works
            if os.path.exists(self.path + self.tempName):
                #Checking to see if valid file type
                if (self.tempName)[-3:] not in ['jpg', 'png']:
                    self.invalidFile = True
                    self.tempName = ''
                    return 
                self.invalidFile = False
                self.invalidName = False
                self.validName = True
                self.fileName = self.path + self.tempName
                self.done = True
                self.tempName = ''
            else:
                self.validName = False
                self.invalidName = True
                self.tempName = ''
        elif keyCode == pygame.K_BACKSPACE:
            #Providing a backspace function for user
            self.tempName = self.tempName[:-1]
        else:
            #Adding to tempname, shown on screen
            self.tempName += chr(keyCode)
            self.invalidName = False
            self.invalidFile = False
            self.validName = False
            
    def mousePressed(self, x, y):
        if 150 < x < 350 and 400 < y < 500:
            self.gameMode = 'Menu'
    
    def redrawAll(self, screen):
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        yellow = (255, 255, 0)
        
        screenrect = (0, 0, 500, 600)
        pygame.draw.rect(screen, white, screenrect)
        
        inputrect = (100, 200, 300, 50)
        pygame.draw.rect(screen, black, inputrect, 3)
        
        myfont = pygame.font.SysFont('Arial', 35)
        filetext = myfont.render(self.tempName, True, black)
        screen.blit(filetext, (110, 200))
        
        menurect = (150, 400, 200, 100)
        pygame.draw.rect(screen, black, menurect, 3)
        
        menutext = myfont.render('Menu', True, black)
        screen.blit(menutext, (210, 430))
        
        dirtext = myfont.render('Enter file name:', True, black)
        screen.blit(dirtext, (150, 150))
        
        if self.invalidName:
            msgtext = myfont.render('Invalid File Name', True, red)
        elif self.invalidFile:
            msgtext = myfont.render('Invalid File Type', True, red)
        elif self.validName:
            msgtext = myfont.render('Upload successful', True, green)
        
        if self.invalidFile or self.invalidName or self.validName:
            screen.blit(msgtext, (130, 250))