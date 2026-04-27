import json
import random

import pygame
from numpy import average
from pygame.locals import QUIT, KEYDOWN
from environment import Environment
from robot import DifferentialDriveRobot, evolve, generateIndividuals

#for potential visualization
USE_VISUALIZATION = False

NUM_EPOCHS_LIST = [1, 5, 10, 20, 30, 40, 50]
NUM_ROBOTS_LIST = [1, 5, 10, 20, 30, 40, 50]
RANDOM_SEEDS = [42, 137, 1905, 1927, 314159]

NUM_EPOCHS = 5
NUM_ROBOTS = 1

# to pause the execution
PAUSE = False

# Initialize Pygame
pygame.init()

# Set up environment
width, height = 1200, 800 # cm
env = Environment(width, height)

# (simulated) time taken for one cycle of the robot executing its algorithm
robot_timestep = 0.1 # in seconds (simulated time)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot Kinematic Simulator")

SIM_TIME = 10

def main():
    global USE_VISUALIZATION, PAUSE

    # run_evolutionary_simulation(num_robots=NUM_ROBOTS, num_epochs=NUM_EPOCHS)
    
    with open("./data/results.jsonl", "a") as f:
        for num_epochs in NUM_EPOCHS_LIST:
            print(f"Running simulations for num_epochs={num_epochs}...")
            for num_robots in NUM_ROBOTS_LIST:
                res_list = []
                for seed in RANDOM_SEEDS: # run each configuration with different random seeds
                    random.seed(seed)
                    res = run_evolutionary_simulation(
                        num_robots=num_robots,
                        num_epochs=num_epochs
                    )
                    res_list.append(res)
                # calculate average results for this configuration
                avg_res = {
                    "num_epochs": num_epochs,
                    "num_robots": num_robots,
                    "average_fitness_per_epoch": [average([r["average_fitness_per_epoch"] for r in res_list])],
                    "min_fitness_per_epoch": [average([r["min_fitness_per_epoch"]for r in res_list])],
                    "max_fitness_per_epoch": [average([r["max_fitness_per_epoch"] for r in res_list])]
                }
                
                f.write(json.dumps(avg_res) + "\n")

    # Quit Pygame
    pygame.quit()

def run_evolutionary_simulation(num_robots=NUM_ROBOTS, num_epochs=NUM_EPOCHS):
    res = {
        "num_epochs": num_epochs,
        "num_robots": num_robots,
        "average_fitness_per_epoch": [],
        "min_fitness_per_epoch": [],
        "max_fitness_per_epoch": []
    }

    start_time = pygame.time.get_ticks()  
        

    pop = generateIndividuals(num_robots)
    steps = int(SIM_TIME / robot_timestep)
    # Evolve for 10 epochs
    for _ in range(num_epochs):
        robots = []
        # start_time = pygame.time.get_ticks()    
        for phenotype in pop:
            robots.append(DifferentialDriveRobot(env,width/2-100,height/2-100,0, weights=phenotype))
            
        # Run sim
        #while (pygame.time.get_ticks() - start_time) / 1000 < SIM_TIME:
        for _ in range(steps):
            if USE_VISUALIZATION:
                screen.fill((0, 0, 0))
                env.draw(screen)

                for robot in robots:
                    robot.draw(screen)

                pygame.display.flip()
            # screen.fill((0, 0, 0))
            # env.draw(screen)
            for robot in robots:
                robot.move(robot_timestep)
                # robot.draw(screen)
            # pygame.display.flip()
            # pygame.display.update()
            
        evaluated_phenotypes = []
        fitness_values = []
        for robot in robots:
            fitness_val = robot.fitness()   
            fitness_values.append(fitness_val)
            evaluated_phenotypes.append((robot.weights, fitness_val))
        
        pop = evolve(evaluated_phenotypes)
        res["average_fitness_per_epoch"].append(average(fitness_values))
        res["max_fitness_per_epoch"].append(max(fitness_values))
        res["min_fitness_per_epoch"].append(min(fitness_values))
    return res



def drawBoom():
    font = pygame.font.SysFont("comicsansms", 172)  # pygame.font.Font(self.font, size)
    text_surface = font.render('BOOM', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width/2, height/2))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    main()
  

