import math
import time
from random import randint

import pygame

from .food import Food
from .life import Life

pygame.init()

class GameInformation:
    def __init__(self, score_1, score_2, score_3, score_4, dur, fps):
        self.score_1 = score_1
        self.score_2 = score_2
        self.score_3 = score_3
        self.score_4 = score_4

        self.dur = dur
        self.fps = fps

class Game:
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    INF_FONT = pygame.font.SysFont("comicsans", 20)
    TT_FONT = pygame.font.SysFont("comicsans", 15)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (75, 75, 75)
    RED = (255, 0, 0)
    BLUE = (50, 20, 255)
    GREEN = (20, 255, 150)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)

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
        self.life_3 = Life(
            self.PURPLE, self.window_width - 10 - Life.WIDTH, self.window_height // 2 - Life.HEIGHT//2, Life.NRG)
        self.life_4 = Life(
            self.CYAN, self.window_width - 10 - Life.WIDTH, self.window_height // 2 - Life.HEIGHT//2, Life.NRG)
        
        self.food = []
        for i in range(5):
            self.food.append(Food())
        
        self.score_1 = 0
        self.score_2 = 0
        self.score_3 = 0
        self.score_4 = 0
        self.dur = 0.0
        self.fps = 0.0
        self.raw_dur = 0.0
        self.rounds = 0
        self.window = window
        
    def _draw_score(self, **kwargs):
        blue_score_text = self.SCORE_FONT.render(
            f"{round(self.score_1)}", True, self.BLUE)
        green_score_text = self.SCORE_FONT.render(
            f"{round(self.score_2)}", True, self.GREEN)
        purple_score_text = self.SCORE_FONT.render(
            f"{round(self.score_3)}", True, self.PURPLE)
        cyan_score_text = self.SCORE_FONT.render(
            f"{round(self.score_4)}", True, self.CYAN)
          
        
        fps_text = self.INF_FONT.render(
            f"FPS: {self.fps}", True, self.YELLOW)
        
        head = self.INF_FONT.render(
            f"Time", True, self.YELLOW)
        time_text = self.TT_FONT.render(
            f"Current: {self.dur}", True, self.YELLOW)
        tick_text = self.TT_FONT.render(
            f"Total: {self.raw_dur}", True, self.YELLOW)   

        self.window.blit(blue_score_text, (self.window_width //
                                           2.3 - blue_score_text.get_width()//2, 10))
        self.window.blit(green_score_text, (self.window_width * (4/5) -
                                            green_score_text.get_width()//1.5, 10))
        self.window.blit(purple_score_text, (self.window_width //
                                             4 - purple_score_text.get_width()//2, 10))
        self.window.blit(cyan_score_text, (self.window_width * (3/5) -
                                             cyan_score_text.get_width()//2, 10))
        
        self.window.blit(head, (self.window_width * (1/100), 10))
        self.window.blit(time_text, (self.window_width * (1/100), 45))
        self.window.blit(tick_text, (self.window_width * (1/100), 30))
        self.window.blit(fps_text, (self.window_width * (905/1000), 10))

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

        for life in [self.life_3]:
            for food in self.food:
                d = math.dist((life.x, life.y), (food.x, food.y))

            
                if d <= Life.WIDTH + food.RADIUS:
                    self.score_3 += 1
                    life.NRG += 2200
                    food.reset()

        
        for life in [self.life_4]:
            for food in self.food:
                d = math.dist((life.x, life.y), (food.x, food.y))

            
                if d <= Life.WIDTH + food.RADIUS:
                    self.score_4 += 1
                    life.NRG += 2200
                    food.reset()
            

    def draw(self, draw_score, draw1, draw2, draw3, draw4):
        self.window.fill(self.BLACK)
        if draw_score:
            self._draw_score()

        if draw1:
            self.life_1.draw(self.window)
        if draw2:
            self.life_2.draw(self.window)
        if draw3:
            self.life_3.draw(self.window)
        if draw4:
            self.life_4.draw(self.window)

        for food in self.food:
            food.draw(self.window)
        


    def move_life(self, left=True, up=True, right=True, down=True, cum=True, balls=True):
        # dist_life = math.dist((self.life_1.x, self.life_1.y), (self.life_2.x, self.life_2.y))
        if cum and balls:
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

        elif cum and not balls:
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

        elif not cum and balls:
            if up:
                if up and self.life_3.y - Life.HEIGHT <= Life.HEIGHT:
                    self.score_3 -= 1
                    return False
                self.life_3.move_up(up)

            if down:
                if down and self.life_3.y + Life.HEIGHT >= self.window_height:
                    self.score_3 -= 1
                    return False
                self.life_3.move_down(down)

            if left:
                if left and self.life_3.x - Life.WIDTH <= - Life.WIDTH:
                    self.score_3 -= 1
                    return False
                self.life_3.move_left(left)

            if right:
                if right and self.life_3.x + Life.WIDTH >= self.window_width:
                    self.score_3 -= 1
                    return False
                self.life_3.move_right(right)

            if not up and not down and not left and not right:
                self.score_3 -= 1
                self.life_3.stop(False, False, False, False)

            if self.life_3.NRG < 2:
                self.score_3 -= 1
                return False

        elif not cum and not balls:
            if up:
                if up and self.life_4.y - Life.HEIGHT <= Life.HEIGHT:
                    self.score_4 -= 1
                    return False
                self.life_4.move_up(up)

            if down:
                if down and self.life_4.y + Life.HEIGHT >= self.window_height:
                    self.score_4 -= 1
                    return False
                self.life_4.move_down(down)

            if left:
                if left and self.life_4.x - Life.WIDTH <= - Life.WIDTH:
                    self.score_4 -= 1
                    return False
                self.life_4.move_left(left)

            if right:
                if right and self.life_4.x + Life.WIDTH >= self.window_width:
                    self.score_4 -= 1
                    return False
                self.life_4.move_right(right)

            if not up and not down and not left and not right:
                self.score_4 -= 1
                self.life_4.stop(False, False, False, False)

            if self.life_4.NRG < 2:
                self.score_4 -= 1
                return False

        return True


    def loop(self):
        self.move_life()
        self._handle_collision()

        game_info = GameInformation(
            self.score_1, self.score_2, self.score_3, self.score_4, self.dur, self.fps)

        return game_info
        

    def reset(self):
        for food in self.food:
            food.reset()

        self.life_1.reset()
        self.life_2.reset()
        self.life_3.reset()
        self.life_4.reset()
        self.score_1 = 0
        self.score_2 = 0
        self.score_3 = 0
        self.score_4 = 0