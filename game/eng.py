import math
import time
from random import randint

import pygame

from .food import Food
from .life import Life

pygame.init()

class GameInformation:
    def __init__(self, score_1, dur, fps):
        self.score_1 = score_1
        self.dur = dur
        self.fps = fps

class Game:
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    INF_FONT = pygame.font.SysFont("comicsans", 25)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (75, 75, 75)
    RED = (255, 0, 0)
    BLUE = (50, 20, 255)
    GREEN = (20, 255, 150)
    CYAN = (0, 255, 255)
    start_time = time.time()
    clock = pygame.time.Clock()

    i = 1

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.life_1 = Life(
            self.CYAN, self.window_width - 10 - Life.WIDTH, self.window_height // 2 - Life.HEIGHT//2, Life.NRG, Life.FD_COUNT)
        
        self.food = Food(self.window_width // 2, self.window_height // 2)
        
        self.score_1 = 0
        self.dur = 0.0
        self.fps = 0.0
        self.raw_dur = 0.0
        self.rounds = 0
        self.window = window
        
    def _draw_score(self, **kwargs):
        left_score_text = self.SCORE_FONT.render(
            f"Blue Score: {round(self.score_1)}", True, self.CYAN)
        time_text = self.INF_FONT.render(
            f"Time: {self.dur}", True, self.YELLOW)
        tick_text = self.INF_FONT.render(
            f"Ticks: {self.raw_dur}", True, self.YELLOW)
        fps_text = self.INF_FONT.render(
            f"FPS: {self.fps}", True, self.YELLOW)

            
        self.window.blit(left_score_text, (self.window_width //2.5, 20))
        self.window.blit(time_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 15))
        self.window.blit(tick_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 50))
        self.window.blit(fps_text, (self.window_width * (1/18) -
                                            fps_text.get_width()//2, 85,))

    def _handle_collision(self):  
        for life in [self.life_1]:
            d = math.dist((life.x, life.y), (self.food.x, self.food.y))

            
            if d <= Life.WIDTH + (self.food.RADIUS * 1.3):
                life.FD_COUNT += 1
                self.score_1 += 1
                life.NRG += 2200
                self.food.reset()
            

    def draw(self, draw_score=True):
        self.window.fill(self.BLACK)
        if draw_score:
            self._draw_score()

        self.life_1.draw(self.window)
        self.food.draw(self.window)
        


    def move_life(self, left=True, up=True, right=True, down=True, cum=True):
        if cum:
            if up:
                if up and self.life_1.y - Life.HEIGHT <= Life.HEIGHT:
                    self.score_1 -= 1
                    return False
                self.life_1.move_up(up)

            if down:
                if down and self.life_1.y + Life.HEIGHT >= self.window_height:
                    self.score_1 -= 1
                    return False
                self.life_1.move_down(down)

            if left:
                if left and self.life_1.x - Life.WIDTH <= - Life.WIDTH:
                    self.score_1 -= 1
                    return False
                self.life_1.move_left(left)

            if right:
                if right and self.life_1.x + Life.WIDTH >= self.window_width:
                    self.score_1 -= 1
                    return False
                self.life_1.move_right(right)

            if not up and not down and not left and not right:
                self.score_1 -= 1
                self.life_1.stop(False, False, False, False)

            if self.life_1.NRG < 2:
                self.score_1 -= 1
                return False
            
        return True

    def loop(self):
        self.move_life()
        self._handle_collision()

        game_info = GameInformation(
            self.score_1, self.dur, self.fps)

        return game_info
        

    def reset(self):
        self.food.reset()
        self.life_1.reset()
        self.score_1 = 0
        self.score_2 = 0