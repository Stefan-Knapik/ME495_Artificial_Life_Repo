import os
from solution2 import SOLUTION
import numpy as np

number_of_robots = 3

for i in range(number_of_robots):
    
    # Reset temp folder
    os.system("rmdir temp /s /q")
    os.system("mkdir temp")
        
    # Create new robot and show a simulation
    number_of_links = np.random.randint(5, 20)
    max_children_per_parent = np.random.randint(1, 4)
    
    rand_robot = SOLUTION(i, number_of_links, max_children_per_parent)
    
    rand_robot.Create_World()
    rand_robot.Create_Body()
    rand_robot.Create_Brain()
    
    # os.system(f"python simulate.py GUI {i}")
    os.system(f"python simulate.py GUI {i} > nul 2> nul")
    