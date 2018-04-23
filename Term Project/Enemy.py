import pygame
from GameObject import GameObject

class Enemy(GameObject):
    def init():
        Enemy.image = pygame.image.load('images/browncircle.png').convert_alpha()
    def __init__(self, d1, d2, i, r):
        self.width = 500
        self.rows = r
        self.blockWidth = int(self.width / self.rows)
        self.d1 = d1
        self.d2 = d2
        self.i  = i
        w = self.blockWidth / 2
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        if d1 == 'V':
            self.x = w+(w*i*2)
            if d2 == 'U':
                self.y = self.width + w
                self.vy = -5
            if d2 == 'D':
                self.y = -w
                self.vy = 5
        if d1 == 'H':
            self.y = w+(w*i*2)
            if d2 == 'L':
                self.x = self.width + w
                self.vx = -5
            if d2 == 'R':
                self.x = -w
                self.vx = 5
        self.scaled = pygame.transform.scale(Enemy.image, (self.blockWidth, self.blockWidth))
        super(Enemy, self).__init__(self.x, self.y, self.scaled, w)
    def update(self, x, y, w, h):
        self.x = x
        self.y = y
        super(Enemy, self).update()