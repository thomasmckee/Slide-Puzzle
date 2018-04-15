import pygame
from GameObject import GameObject

class Blank(GameObject):
    def init():
        #Loading the blank image
        image = pygame.image.load('images/blank.png').convert()
        Blank.scaled = pygame.transform.scale(image, (125, 125))
    #Calling init and having update, same as Block class
    def __init__(self, x, y):
        super(Blank, self).__init__(x, y, Blank.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Blank, self).update()