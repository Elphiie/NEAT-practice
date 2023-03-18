from turtle import window_width
import pygame
from random import randint
class Food:
    RADIUS = 60

    def __init__(self, color, x, y):
        self.color = color
        self.x = randint(100, 1180)
        self.y = randint(100, 620)

    def draw(self, win):
        pygame.draw.circle(
            win, self.color, (self.x, self.y), self.RADIUS)

    def reset(self):
        self.x = randint(25, 1255)
        self.y = randint(75, 645)