from turtle import window_width
import pygame
from random import randint
class Food:
    RADIUS = 30

    def __init__(self, x, y):
        self.x = randint(200, 1190)
        self.y = randint(200, 680)

    def draw(self, win):
        pygame.draw.circle(
            win, (255, 50, 50), (self.x, self.y), self.RADIUS)

    def reset(self):
        self.x = randint(100, 1220)
        self.y = randint(150, 680)