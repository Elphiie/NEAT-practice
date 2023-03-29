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

        # energy bars width limits
        div1 = int((self.NRG-6000)/100)
        div2 = int((self.NRG-12000)/200)
        div3 = int((self.NRG-24000)/400)
        div4 = int((self.NRG-48000)/800)
        div5 = int((self.NRG-96000)/1600)
        div6 = int((self.NRG-192000)/3200)

        bar1 = int(self.NRG / 100)
        bar2 = div1
        bar3 = div2
        bar4 = div3
        bar5 = div4
        bar6 = div5
        bar7 = div6
        x = self.x
       
        
        if self.NRG > 1500:
            color = (0, 255, 0)
        elif self.NRG <= 1250 and self.NRG > 750:
            color = (255, 255, 0)
        elif self.NRG <= 750:
            color = (255, 50, 50)

        # to stop energy bar from going over the limit
        if self.NRG >= 6000:
            bar1 = 60
        if self.NRG >= 12000:
            bar2 = 60
        if self.NRG >= 24000:
            bar3 = 60
        if self.NRG >= 48000:
            bar4 = 60
        if self.NRG >= 96000:
            bar5 = 60
        if self.NRG >= 192000:
            bar6 = 60
        if self.NRG >= 384000:
            bar7 = 60 

        pygame.draw.rect(
                    win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        
        # draws new energy bar on top if previous bar is full
        pygame.draw.rect(
            win, color, (x, self.y - 6, bar1, 4))

        if self.NRG >= 6000:
            pygame.draw.rect(
            win, (0, 50, 255), (x, self.y - 6, bar2, 4))
        
        if self.NRG >= 12000:
            pygame.draw.rect(
            win, (255, 100, 255), (x, self.y - 6, bar3, 4))
        
        if self.NRG >= 24000:
            pygame.draw.rect(
            win, (255, 150, 50), (x, self.y - 6, bar4, 4))
            
        if self.NRG >= 48000:
            pygame.draw.rect(
            win, (255, 255, 0), (x, self.y - 6, bar5, 4))

        if self.NRG >= 96000:
            pygame.draw.rect(
            win, (10, 255, 255), (x, self.y - 6, bar6, 4))

        if self.NRG >= 192000:
            pygame.draw.rect(
            win, (255, 255, 255), (x, self.y - 6, bar7, 4))

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