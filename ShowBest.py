import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants as c

for N in range(0, c.num_to_save):
    for seed in range(1, c.trials+1):
        for algo in ['PHC', 'AFPO']:
            
            print(f"save/BestSolution_{algo}_RS{seed}_N{N}.obj")
            x = input("Press Enter to continue...")
            
            f = open(f"save/BestSolution_{algo}_RS{seed}_N{N}.obj", "rb")
            BestSolution = pickle.load(f)
            f.close()
            BestSolution.Start_Simulation("GUI")
            
        
    
    