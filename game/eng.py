import math
import time
from random import randint

import pygame

from .food import Food
from .life import Life

pygame.init()

class GameInformation:
    def __init__(self, score_1, score_2, dur, fps):
        self.score_1 = score_1
        self.score_2 = score_2
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

    start_time = time.time()
    clock = pygame.time.Clock()

    i = 1

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.life_1 = Life(
            self.BLUE, self.window_width - 10 - Life.WIDTH, self.window_height // 2 - Life.HEIGHT//2, Life.NRG)
        self.life_2 = Life(
            self.GREEN, self.window_width - 10 - Life.WIDTH, self.window_height // 2 - Life.HEIGHT//2, Life.NRG)
        
        self.food = []
        for i in range(5):
            self.food.append(Food())
        
        self.score_1 = 0
        self.score_2 = 0
        self.dur = 0.0
        self.fps = 0.0
        self.raw_dur = 0.0
        self.rounds = 0
        self.window = window
        
    def _draw_score(self, **kwargs):
        left_score_text = self.SCORE_FONT.render(
            f"Blue Score: {round(self.score_1)}", True, self.BLUE)
        right_score_text = self.SCORE_FONT.render(
            f"Green Score: {round(self.score_2)}", True, self.GREEN)
        time_text = self.INF_FONT.render(
            f"Time: {self.dur}", True, self.YELLOW)
        tick_text = self.INF_FONT.render(
            f"Ticks: {self.raw_dur}", True, self.YELLOW)
        fps_text = self.INF_FONT.render(
            f"FPS: {self.fps}", True, self.YELLOW)

            
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))
        self.window.blit(time_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 15))
        self.window.blit(tick_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 50))
        self.window.blit(fps_text, (self.window_width * (1/18) -
                                            fps_text.get_width()//2, 85,))

    def _handle_collision(self):
          
        for life in [self.life_1]:
            for food in self.food:
                d = math.dist((life.x, life.y), (food.x, food.y))

            
                if d <= Life.WIDTH + food.RADIUS:
                    self.score_1 += 1
                    life.NRG += 2200
                    food.reset()



        for life in [self.life_2]:
            for food in self.food:
                d = math.dist((life.x, life.y), (food.x, food.y))

            
                if d <= Life.WIDTH + food.RADIUS:
                    self.score_2 += 1
                    life.NRG += 2200
                    food.reset()
            

    def draw(self, draw_score, draw1, draw2):
        self.window.fill(self.BLACK)
        if draw_score:
            self._draw_score()

        if draw1:
            self.life_1.draw(self.window)
        if draw2:
            self.life_2.draw(self.window)

        for food in self.food:
            food.draw(self.window)
        


    def move_life(self, left=True, up=True, right=True, down=True, cum=True):
        # dist_life = math.dist((self.life_1.x, self.life_1.y), (self.life_2.x, self.life_2.y))
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

        else:
            if up:
                if up and self.life_2.y - Life.HEIGHT <= Life.HEIGHT:
                    self.score_2 -= 1
                    return False
                self.life_2.move_up(up)

            if down:
                if down and self.life_2.y + Life.HEIGHT >= self.window_height:
                    self.score_2 -= 1
                    return False
                self.life_2.move_down(down)

            if left:
                if left and self.life_2.x - Life.WIDTH <= - Life.WIDTH:
                    self.score_2 -= 1
                    return False
                self.life_2.move_left(left)

            if right:
                if right and self.life_2.x + Life.WIDTH >= self.window_width:
                    self.score_2 -= 1
                    return False
                self.life_2.move_right(right)

            if not up and not down and not left and not right:
                self.score_2 -= 1
                self.life_2.stop(False, False, False, False)

            if self.life_2.NRG < 2:
                self.score_2 -= 1
                return False    

        


        return True

    def loop(self):
        self.move_life()
        self._handle_collision()

        game_info = GameInformation(
            self.score_1, self.score_2, self.dur, self.fps)

        return game_info
        

    def reset(self):
        for food in self.food:
            food.reset()

        self.life_1.reset()
        self.life_2.reset()
        self.score_1 = 0
        self.score_2 = 0