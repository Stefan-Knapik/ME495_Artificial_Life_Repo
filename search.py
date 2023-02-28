import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import numpy as np

for i in range(1,2):
    
    # Set seed for robot generation
    rng = np.random.default_rng(i)
    
    # Initialize parallel hill climber
    phc = PARALLEL_HILL_CLIMBER()
    
    # Search for best robot
    phc.Evolve()
    
    # Show best robot
    phc.Show_Best()
