import pickle
import numpy as np
import matplotlib.pyplot as plt

seed = 1

fitness_progress = np.load(f"FitnessProgress{seed}.npy")

print(fitness_progress)

plt.figure(1)
plt.plot(fitness_progress)
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.show()

plt.figure(2)
plt.plot(fitness_progress.min(axis=1))
plt.ylabel('Best Fitness')
plt.xlabel('Generation')
plt.show()



exit()

f = open(f"BestSolution{seed}.obj", "rb")
BestSolution = pickle.load(f)
f.close()

BestSolution.Start_Simulation("GUI")