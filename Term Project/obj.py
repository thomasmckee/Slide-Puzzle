from GameObject import GameObject
import pygame

class Hole(GameObject):
    def init():
        #Loading and scaling player image
        Hole.image = pygame.image.load('images/mousehole.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Hole.image, (self.playerWidth, self.playerWidth))
        super(Hole, self).__init__(x, y, self.scaled, self.playerWidth)
    def update(self, w, h):
        super(Hole, self).update()

class Trap(GameObject):
    def init():
        #Loading and scaling player image
        Trap.image = pygame.image.load('images/trap.png').convert_alpha()
    #Using the super (gameobject) init and update
    def __init__(self, x, y, rows):
        self.hit = False
        self.rows = rows
        self.width = 500
        self.blockWidth = int(self.width / rows)
        self.playerWidth = int((2/5)*self.blockWidth)
        self.scaled = pygame.transform.scale(Trap.image, (self.playerWidth, self.playerWidth))
        super(Trap, self).__init__(x, y, self.scaled, self.playerWidth)
    def update(self, w, h):
        super(Trap, self).update()