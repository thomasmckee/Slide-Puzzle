import pygame
from GameObject import GameObject

class Blank(GameObject):
    def init():
        #Loading the blank image
        Blank.image = pygame.image.load('images/blank.png').convert()
        
    #Calling init and having update, same as Block class
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / self.rows)
        self.scaled = pygame.transform.scale(Blank.image, (self.blockWidth, self.blockWidth))
        super(Blank, self).__init__(x, y, self.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Blank, self).update()