from GameObject import GameObject
import pygame

class Star(GameObject):
    def init():
        #Loading and scaling player image
        Star.image = pygame.image.load('images/star.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Star.image, (self.playerWidth, self.playerWidth))
        super(Star, self).__init__(x, y, self.scaled, 0)
    def update(self, w, h):
        super(Star, self).update()