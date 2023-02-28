import pickle
import numpy as np
import matplotlib.pyplot as plt

fitness_progress = np.load(f"save/FitnessProgress1.npy")
fitness_progress = np.expand_dims(fitness_progress, axis=0)

for seed in range(1,2):
    temp = np.load(f"save/FitnessProgress{seed}.npy")
    fitness_progress = np.append(fitness_progress, np.expand_dims(temp, axis=0), axis=0)

plt.figure(1)
for seed in range(1,2):
    plt.plot(fitness_progress[seed,:,:].min(axis=1))
plt.ylabel('Best Fitness')
plt.xlabel('Generation')
plt.show()

plt.figure(2)
plt.plot(list[0])
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.show()





exit()

f = open(f"BestSolution{seed}.obj", "rb")
BestSolution = pickle.load(f)
f.close()

BestSolution.Start_Simulation("GUI")