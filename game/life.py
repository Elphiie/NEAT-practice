import pygame
import math
from random import randint


class Life:
    VEL = 6
    WIDTH = 30
    HEIGHT = 30
    NRG = 3100

    def __init__(self, color, x, y, NRG):
        self.x = randint(40, 1240)
        self.y = randint(40, 660)
        self.color = color
        self.NRG = NRG

    #to draw a square if called
    def draw(self, win):        
        color = (0, 0, 0)
        last_bar_width = int(self.NRG / 100)
        second_bar_width = int((self.NRG / 2)/100)
        x = self.x
       
        
        if self.NRG > 1250:
            color = (0, 255, 0)
        elif self.NRG <= 1250 and self.NRG > 625:
            color = (255, 255, 0)
        elif self.NRG <= 625:
            color = (255, 50, 50)

        if self.NRG >= 3000:
            last_bar_width = 30

        pygame.draw.rect(
                    win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        
        pygame.draw.rect(
            win, color, (x, self.y - 6, last_bar_width, 4))

        if self.NRG >= 3000:
            pygame.draw.rect(
            win, (0, 50, 255), (x, self.y - 6, second_bar_width, 4))
                
            
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