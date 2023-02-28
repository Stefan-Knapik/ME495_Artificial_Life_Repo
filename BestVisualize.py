import pickle
import numpy as np
import matplotlib.pyplot as plt

for seed in range(1,6):

    f = open(f"save/BestSolution{seed}.obj", "rb")
    BestSolution = pickle.load(f)
    f.close()

    BestSolution.Start_Simulation("GUI")