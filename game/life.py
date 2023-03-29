import pygame
import math
from random import randint


class Life:
    VEL = 6
    WIDTH = 30
    HEIGHT = 30
    NRG = 3000

    def __init__(self, color, x, y, NRG):
        self.x = randint(40, 1240)
        self.y = randint(40, 660)
        self.color = color
        self.NRG = NRG

    #to draw a square if called
    def draw(self, win):        
        color = (0, 0, 0)

        # energy bars
        div1 = int((self.NRG-6000)/100)
        div2 = int((self.NRG-12000)/100)
        div3 = int((self.NRG-18000)/100)

        bar1 = int(self.NRG / 100)
        bar2 = div1
        bar3 = div2
        bar4 = div3
        x = self.x
       
        
        if self.NRG > 1500:
            color = (0, 255, 0)
        elif self.NRG <= 1250 and self.NRG > 750:
            color = (255, 255, 0)
        elif self.NRG <= 750:
            color = (255, 50, 50)

        if self.NRG >= 6000:
            bar1 = 60
        if self.NRG >= 12000:
            bar2 = 60
        if self.NRG >= 18000:
            bar3 = 60

        pygame.draw.rect(
                    win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        
        pygame.draw.rect(
            win, color, (x, self.y - 6, bar1, 4))

        if self.NRG >= 6000:
            pygame.draw.rect(
            win, (0, 50, 255), (x, self.y - 6, bar2, 4))
        
        if self.NRG >= 12000:
            pygame.draw.rect(
            win, (255, 100, 255), (x, self.y - 6, bar3, 4))
        
        if self.NRG >= 18000:
            pygame.draw.rect(
            win, (255, 150, 50), (x, self.y - 6, bar4, 4))
            
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