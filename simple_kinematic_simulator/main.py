import pygame
from pygame.locals import QUIT, KEYDOWN
from environment import Environment
from robot import DifferentialDriveRobot, evolve, generateIndividuals

#for potential visualization
USE_VISUALIZATION = True

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

SIM_TIME = 5

def main():
    global USE_VISUALIZATION, PAUSE
    # init first gen
    pop = generateIndividuals(10)
    # Evolve for 10 epochs
    for x in range(10):
        robots = []
        start_time = pygame.time.get_ticks()    
        print(x)
        for phenotype in pop:
            print("current phenotype:", phenotype)
            # robots.append(DifferentialDriveRobot(env,35, 468,-1, weights=phenotype))
            robots.append(DifferentialDriveRobot(env,width/2-100,height/2-100,0, weights=phenotype))
            #robot = DifferentialDriveRobot(env,35, 468,-1, phenotype)
            
            # Run sim
        while (pygame.time.get_ticks() - start_time) / 1000 < SIM_TIME:
            screen.fill((0, 0, 0))
            env.draw(screen)
            for robot in robots:
                robot.move(robot_timestep)
                robot.draw(screen)
            pygame.display.flip()
            pygame.display.update()
            
        evaluated_phenotypes = []
        for robot in robots:
            evaluated_phenotypes.append((robot.weights, robot.fitness()))
                
        pop = evolve(evaluated_phenotypes)
        print("new population:", pop)
        
    print("total execution time:", (pygame.time.get_ticks() - start_time) / 1000, "seconds")  # runtime in seconds

    # Quit Pygame
    pygame.quit()
    # Run each phenotype for 5 seconds
    
    # Evaluate fitness at end of the the 5 seconds
    
    # Evolve 
    
    # Game loop
    # running = True
    # while running:
    #     #print(pygame.mouse.get_pos())
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #         if event.type == KEYDOWN:
    #             if event.key == pygame.K_h: # use space key to toggle between visualization and headless
    #                 USE_VISUALIZATION = not USE_VISUALIZATION
    #                 print("Visualization is", "on" if USE_VISUALIZATION else "off")
    #             if event.key == pygame.K_SPACE:
    #                 PAUSE = not PAUSE

    #     if not PAUSE:
    #         # simulate one execution cycle of the robot
    #         robot_pose = robot.move(robot_timestep)


    #     if USE_VISUALIZATION:
    #         screen.fill((0, 0, 0))
    #         # draw environment
    #         env.draw(screen)
    #         # draw robot
    #         robot.draw(screen)

    #         # warn the user if collision happened
    #         if robot.collided:
    #             print("Collision!")
    #             # Draw the animation
    #             drawBoom()

    #         pygame.display.flip()
    #         pygame.display.update()



def drawBoom():
    font = pygame.font.SysFont("comicsansms", 172)  # pygame.font.Font(self.font, size)
    text_surface = font.render('BOOM', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width/2, height/2))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    main()
  

