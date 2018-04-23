from GameObject import GameObject
import pygame

class Point(GameObject):
    def init():
        #Loading and scaling player image
        Point.yellow = pygame.image.load('images/yellowcircle.png').convert_alpha()
        Point.green  = pygame.image.load('images/greencircle.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.hit = False
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((1/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Point.yellow, (self.playerWidth, self.playerWidth))
        super(Point, self).__init__(x, y, self.scaled, 0)
    def update(self, w, h):
        super(Point, self).update()