import math
import os
import pickle
import time

import neat
import pygame
import visualize
from game import Game


class GoL:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.life_1 = self.game.life_1
        self.life_2 = self.game.life_2
        self.score_1 = self.game.score_1
        self.score_2 = self.game.score_2
        self.food = self.game.food



    def best_net(self, net, draw=False):
        clock = pygame.time.Clock()
        start_time = time.time()
        run = True

        life = self.life_1
    
        food = self.food
        window_height = self.game.window_height
        window_width = self.game.window_height

        while run:
            pygame.display.update()
            clock.tick(6000)
            duration = time.time() - start_time
            self.game.dur = round(duration, 2)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            if draw:
                self.game.draw(draw_score=True)         

            
            near_wall = False

            # checks if our squares is close to the window border            
            if window_height + life.y <= window_height + 10:
                near_wall = True
                
            elif life.y + life.HEIGHT + 10 >= window_height:
                near_wall = True

            elif window_width + life.x <= window_width + 10:
                near_wall = True 

            elif life.x + life.WIDTH + 10 >= window_width:
                near_wall = True

            else:
                near_wall = False


            output = net.activate(
                (
                life.x,
                life.x - food.x,
                near_wall,
                life.y - food.y, 
                life.y,              
                )
            )

            decision = output.index(max(output))

            valid = True
            if decision == 0:  # Don't move
                valid = self.game.move_life(False, False, False, False, cum=True)
                life.NRG -= 2
                # we want to discourage this
            elif decision == 1:  # Move up
                valid = self.game.move_life(down=False, up=True, right=False, left=False, cum=True)
                life.NRG -= 3
            elif decision == 2:  # Move down
                valid = self.game.move_life(up=False, right=False, left=False, down=True, cum=True)
                life.NRG -= 3
            elif decision == 3:  # Move left
                valid = self.game.move_life(left=True, up=False, down=False, right=False, cum=True)
                life.NRG -= 3
            elif decision == 4:  # Move right
                valid = self.game.move_life(up=False, down=False, right=True, left=False, cum=True)
                life.NRG -= 3
            if not valid:
                self.game.move_life(False, False, False, False, cum=True) 

            self.game.loop()

        return False


    def train_ai(self, genome1, genome2, config, duration, draw=False):
        run = True
        start_time = time.time()
        clock = pygame.time.Clock()

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        while run:
            pygame.display.update()
            clock.tick(6000)
            raw_time = pygame.time.get_ticks()
            fps = clock.get_fps()
            duration = time.time() - start_time
            self.game.fps = round(fps, 2)
            self.game.raw_dur = round(raw_time/1000, 2)
            self.game.dur = round(duration, 2)

            game_info = self.game.loop()

            self.move_ai(net1, net2)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True       

            if draw:
                self.game.draw(draw_score=True)


            if game_info.score_1 >= 100 or game_info.score_2 >= 100 or game_info.score_1 <= -10 or game_info.score_2 <= -10: 

                self.calculate_fitness(duration)
                break
                          
        return False

    def move_ai(self, net1, net2):
        players = [(self.genome1, net1, self.life_1, True), (self.genome2, net2, self.life_2, False)]
        window_height = self.game.window_height
        window_width = self.game.window_width
        food = self.food

        for (genome, net, life, cum) in players:
            dist_food = math.dist((life.x, life.y), (self.food.x, self.food.y))
            near_wall_up = False
            near_wall_down = False
            near_wall_left = False
            near_wall_rigth = False

            # checks if our squares is close to the window border            
            if window_height + life.y <= window_height + 10:
                near_wall_up = True
                
            elif life.y + life.HEIGHT + 10 >= window_height:
                near_wall_down = True

            elif window_width + life.x <= window_width + 10:
                near_wall_left = True 

            elif life.x + life.WIDTH + 10 >= window_width:
                near_wall_rigth = True

            else:
                near_wall_up = False
                near_wall_down = False
                near_wall_left = False
                near_wall_rigth = False


            output = net.activate(
                (
                near_wall_left,
                life.x,
                near_wall_rigth,
                life.x - food.x,
                near_wall_up,
                life.y - food.y,
                near_wall_down, 
                life.y,              
                )
            )

            decision = output.index(max(output))

            valid = True
            if decision == 0:  # Don't move
                valid = self.game.move_life(False, False, False, False, cum=cum)
                genome.fitness -= 0.1
                life.NRG -= 2
                  # we want to discourage this
            elif decision == 1:  # Move up
                valid = self.game.move_life(down=False, up=True, right=False, left=False, cum=cum)
                life.NRG -= 3
            elif decision == 2:  # Move down
                valid = self.game.move_life(up=False, right=False, left=False, down=True, cum=cum)
                life.NRG -= 3
            elif decision == 3:  # Move left
                valid = self.game.move_life(left=True, up=False, down=False, right=False, cum=cum)
                life.NRG -= 3
            elif decision == 4:  # Move right
                valid = self.game.move_life(up=False, down=False, right=True, left=False, cum=cum)
                life.NRG -= 3
            if not valid:  # If the movement makes the square go off the screen punish the AI
                genome.fitness -= 1


            if life.NRG <= 0: # If the square moves too much punish the
                genome.fitness -= 1

            if dist_food <= life.WIDTH + (self.food.RADIUS * 2.25):
                genome.fitness += 0.01

            if dist_food <= life.WIDTH + (self.food.RADIUS * 2):
                genome.fitness += 0.1

            if dist_food <= life.WIDTH + (self.food.RADIUS * 1.3):
                genome.fitness += 3



    def calculate_fitness(self, duration):
        self.genome1.fitness += duration
        self.genome2.fitness += duration




def eval_genomes(genomes, config):
    start_time = time.time()
    width, height = 1280, 720
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ai-test")

    node_names = {
                -8:'near wall left',                
                -7: 'life pos x',
                -6: 'near wall right',
                -5: 'food dist x',
                -4: 'near wall up',                               
                -3: 'food dist y',
                -2: 'near wall down',
                -1: 'life pos y',
                0: 'stop',
                1: 'up',
                2: 'down',
                3: 'left',
                4: 'right'
                }

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            gol = GoL(win, width, height)

            force_quit = gol.train_ai(genome1, genome2, config, duration=time.time()-start_time, draw=True)
            if force_quit:
                #saves an svg file vizualising the network for current genomes playing at the time of closing
                visualize.draw_net(config, genome1, True, '1', node_names=node_names)

                visualize.draw_net(config, genome2, True, '2', node_names=node_names)
               
                quit()



def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-6')
    # p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 25)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
    
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)


    node_names = {
                -8:'near wall left',                
                -7: 'life pos x',
                -6: 'near wall right',
                -5: 'food dist x',
                -4: 'near wall up',                               
                -3: 'food dist y',
                -2: 'near wall down',
                -1: 'life pos y',
                0: 'stop',
                1: 'up',
                2: 'down',
                3: 'left',
                4: 'right'
                }
    
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.plot_stats(stats, ylog=False, view=True)

    visualize.plot_species(stats, view=True)


def test_winner(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 1280, 720
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Let there be Life")
    gol = GoL(win, width, height)
    gol.best_net(winner_net, draw=True)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)



    run_neat(config)
    # test_winner(config)