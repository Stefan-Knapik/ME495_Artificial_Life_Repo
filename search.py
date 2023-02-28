import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from solution import SOLUTION
import numpy as np

for i in range(1,2):
    
    rand_robot = SOLUTION(0, i)
    rand_robot.Create_World()
    rand_robot.Create_Body()
    rand_robot.Create_Brain()
    
    # os.system(f"python simulate.py GUI {i}")
    os.system(f"python simulate.py GUI {i} > nul 2> nul")
    exit()
    
    
    
    # Initialize parallel hill climber
    phc = PARALLEL_HILL_CLIMBER(random_seed=i)
    
    # Search for best robot
    phc.Evolve()
    
    # Show best robot
    phc.Show_Best()
