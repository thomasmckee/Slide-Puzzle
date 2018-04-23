import pygame
from GameObject import GameObject

class Player(GameObject):
    def init():
        #Loading and scaling player image
        Player.image = pygame.image.load('images/player.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((1/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Player.image, (self.playerWidth, self.playerWidth))
        super(Player, self).__init__(x, y, self.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Player, self).update()
        