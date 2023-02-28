import pickle
import numpy as np
import matplotlib.pyplot as plt

for seed in range(1,6):
    list[seed-1] = np.load(f"FitnessProgress{seed}.npy")

plt.figure(1)
plt.hold(True)
for fitness_progress in list:
    plt.plot(fitness_progress.min(axis=1))
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