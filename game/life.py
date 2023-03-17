import pygame
import math
from random import randint


class Life:
    VEL = 6
    WIDTH = 30
    HEIGHT = 30
    NRG = 2500

    def __init__(self, color, x, y, NRG):
        self.x = randint(40, 1240)
        self.y = randint(40, 660)
        self.color = color
        self.NRG = NRG

    #to draw a square if called
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        
    #movement functions
    def move_up(self, up=True):
        if up:
            self.y_vel = self.VEL
            self.y -= self.y_vel
        else:
            self.y_vel *= 0
    def move_down(self, down=True):
        if down:
            self.y_vel = self.VEL
            self.y += self.y_vel
        else: 
            self.y_vel *= 0
        
    def move_left(self, left=True):    
        if left:
            self.x_vel = self.VEL
            self.x -= self.x_vel
        else: 
            self.x_vel *= 0

    def move_right(self, right=True):
        if right:
            self.x_vel = self.VEL
            self.x += self.x_vel
        else:
            self.x_vel *= 0
    
    def stop(self, up=False, down=False, left=False, right=False):
        if not up and down and left and right:
            self.y_vel *= 0
            self.x_vel *= 0
        else:
            pass



    def reset(self):
        self.x = randint(25, 1255)
        self.y = randint(75, 645)