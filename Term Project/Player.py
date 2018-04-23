import pygame
from GameObject import GameObject

class Player(GameObject):
    def init():
        #Loading and scaling player image
        image = pygame.image.load('images/player.png').convert_alpha()
        Player.scaled = pygame.transform.scale(image, (25, 25))
    #Using the super (gameobject) init and update
    def __init__(self, x, y):
        super(Player, self).__init__(x, y, Player.scaled, 0)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Player, self).update()
        