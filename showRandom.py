import os
from solution import SOLUTION

number_of_robots = 8

for i in range(number_of_robots):
    
    # Reset temp folder
    os.system("rmdir temp /s /q")
    os.system("mkdir temp")
        
    # Create new robot and show a simulation
    rand_robot = SOLUTION(i)
    
    rand_robot.Create_World()
    rand_robot.Create_Body()
    rand_robot.Create_Brain()
    
    # os.system(f"python simulate.py GUI {i}")
    os.system(f"python simulate.py GUI {i} > nul 2> nul")
    