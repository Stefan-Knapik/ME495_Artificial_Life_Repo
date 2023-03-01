import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants as c

# for seed in range(1, c.trials+1):
for seed in range(0, c.num_to_save):
    
    x = input("Press Enter to continue...")

    f = open(f"save/BestSolution{seed}.obj", "rb")
    BestSolution = pickle.load(f)
    f.close()

    BestSolution.Start_Simulation("GUI")
    
    
    