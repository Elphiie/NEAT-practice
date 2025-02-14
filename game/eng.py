import math
import time
import random
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
        
        self.food = Food(self.window_width // 2, self.window_height // 2)
        
        self.rng_timer = random.uniform(0.2, 3.0)
        self.score_1 = 0
        self.score_2 = 0
        self.dur = 0.0
        self.fps = 0.0
        self.raw_dur = 0.0
        self.rounds = 0
        self.window = window
        
    def _draw_score(self, draw1, draw2, **kwargs):
        if draw1:
            left_score_text = self.SCORE_FONT.render(
                f"Blue Score: {round(self.score_1)}", True, self.BLUE)
            self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        if draw2:
            right_score_text = self.SCORE_FONT.render(
                f"Green Score: {round(self.score_2)}", True, self.GREEN)
            self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))
            
        time_text = self.INF_FONT.render(
            f"Time: {self.dur}", True, self.YELLOW)
        tick_text = self.INF_FONT.render(
            f"Ticks: {self.raw_dur}", True, self.YELLOW)
        fps_text = self.INF_FONT.render(
            f"FPS: {self.fps}", True, self.YELLOW)

            
        
        
        self.window.blit(time_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 15))
        self.window.blit(tick_text, (self.window_width * (1/18) -
                                            time_text.get_width()//2, 50))
        self.window.blit(fps_text, (self.window_width * (1/18) -
                                            fps_text.get_width()//2, 85,))

    def _handle_collision(self):  
        for life in [self.life_1]:
            d = math.dist((life.x, life.y), (self.food.x, self.food.y))

            
            if d <= (Life.WIDTH * 2) + self.food.RADIUS:
                self.score_1 += 5
                life.NRG += 2200
                self.food.reset()



        for life in [self.life_2]:
            d = math.dist((life.x, life.y), (self.food.x, self.food.y))

            
            if d <= (Life.WIDTH * 2) + self.food.RADIUS:
                self.score_2 += 5
                life.NRG += 2200
                self.food.reset()
            

    def draw(self, draw_score=True, draw1=False, draw2=False):
        self.window.fill(self.BLACK)
        if draw_score:
            if draw1:
                self.life_1.draw(self.window)
                self._draw_score(draw1, draw2)
            if draw2:
                self.life_2.draw(self.window)
                self._draw_score(draw1, draw2)
        self.food.draw(self.window)
                
        # spawn_food = self.rng_timer - self.dur
        # for t in spawn_food:
        #     if t <= 0.1:
        #         food.append(self.food.draw(self.window))
            

        


    def move_life(self, left=True, up=True, right=True, down=True, upLeft=True, upRight=True, downLeft=True, downRight=True, cum=True):
        # dist_life = math.dist((self.life_1.x, self.life_1.y), (self.life_2.x, self.life_2.y))
        if cum and self.life_1.NRG > 3:
            if up:
                if up and self.life_1.y - (Life.HEIGHT * 2) <= Life.HEIGHT:
                    self.score_1 -= 0.1
                    return False
                else:
                    self.life_1.move_up(up)

            if down:
                if down and self.life_1.y + (Life.HEIGHT * 2) >= self.window_height:
                    self.score_1 -= 0.1
                    return False
                else:
                    self.life_1.move_down(down)

            if left:
                if left and self.life_1.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_1 -= 0.1
                    return False
                else:
                    self.life_1.move_left(left)

            if right:
                if right and self.life_1.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_1 -= 0.1
                    return False
                else:
                    self.life_1.move_right(right)
            
            if upLeft:
                if upLeft and self.life_1.y - (Life.HEIGHT * 2) <= Life.HEIGHT and self.life_1.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_1 -= 0.2
                    return False
                else:
                    self.life_1.move_upLeft(upLeft)

            if upRight:
                if upRight and self.life_1.y - (Life.HEIGHT * 2) <= Life.HEIGHT and self.life_1.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_1 -= 0.2
                    return False
                else:
                    self.life_1.move_upRight(upRight)

            if downLeft:
                if downLeft and self.life_1.y + (Life.HEIGHT * 2) >= Life.HEIGHT and self.life_1.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_1 -= 0.2
                    return False
                else:
                    self.life_1.move_downLeft(downLeft)

            if downRight:
                if downRight and self.life_1.y + (Life.HEIGHT * 2) >= Life.HEIGHT and self.life_1.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_1 -= 0.2
                    return False
                else:
                    self.life_1.move_downRight(downRight)                 

            if not up and not down and not left and not right and not upLeft and not upRight and not downLeft and not downRight:
                self.score_1 -= 0.1
                self.life_1.stop(False, False, False, False, False, False, False, False)

        if self.life_1.NRG <= 3:
            self.score_1 -= 0.1
            return False

        elif not cum and self.life_2.NRG > 3:
            if up:
                if up and self.life_2.y - (Life.HEIGHT * 2) <= Life.HEIGHT:
                    self.score_2 -= 1
                    return False
                else:
                    self.life_2.move_up(up)

            if down:
                if down and self.life_2.y + (Life.HEIGHT * 2) >= self.window_height:
                    self.score_2 -= 0.1
                    return False
                else:
                    self.life_2.move_down(down)

            if left:
                if left and self.life_2.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_2 -= 0.1
                    return False
                else:
                    self.life_2.move_left(left)

            if right:
                if right and self.life_2.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_2 -= 0.1
                    return False
                else:
                    self.life_2.move_right(right)

            if upLeft:
                if upLeft and self.life_2.y - (Life.HEIGHT * 2) <= Life.HEIGHT and self.life_2.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_2 -= 0.2
                    return False
                else:
                    self.life_2.move_upLeft(upLeft)

            if upRight:
                if upRight and self.life_2.y - (Life.HEIGHT * 2) <= Life.HEIGHT and self.life_2.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_2 -= 0.2
                    return False
                else:
                    self.life_2.move_upRight(upRight)

            if downLeft:
                if downLeft and self.life_2.y + (Life.HEIGHT * 2) >= Life.HEIGHT and self.life_2.x - (Life.WIDTH * 2) <= - Life.WIDTH:
                    self.score_2 -= 0.2
                    return False
                else:
                    self.life_2.move_downLeft(downLeft)

            if downRight:
                if downRight and self.life_2.y + (Life.HEIGHT * 2) >= Life.HEIGHT and self.life_2.x + (Life.WIDTH * 2) >= self.window_width:
                    self.score_2 -= 0.2
                    return False
                else:
                    self.life_2.move_downRight(downRight)                 

            if not up and not down and not left and not right and not upLeft and not upRight and not downLeft and not downRight:
                self.score_1 -= 0.1
                self.life_2.stop(False, False, False, False, False, False, False, False)

        if self.life_2.NRG <= 3:
            self.score_2 -= 0.1
            return False    

        # else:
        #     return False


        return True

    def loop(self):
        self.move_life()
        self._handle_collision()

        game_info = GameInformation(
            self.score_1, self.score_2, self.dur, self.fps)

        return game_info
        

    def reset(self):
        self.food.reset()
        self.life_1.reset()
        self.life_2.reset()
        self.score_1 = 0
        self.score_2 = 0
        self.rng_timer = 0