import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants as c

fitness_progress = np.load(f"save/FitnessProgress1.npy")
fitness_progress = np.expand_dims(fitness_progress, axis=0)

for seed in range(1, c.trials+1):
    temp = np.load(f"save/FitnessProgress{seed}.npy")
    fitness_progress = np.append(fitness_progress, np.expand_dims(-temp, axis=0), axis=0)

plt.figure(1)
for seed in range(1, c.trials+1):
    plt.plot(fitness_progress[seed,:,:].max(axis=1))
plt.ylabel('Best Fitness')
plt.xlabel('Generation')
plt.legend(('Seed 1', 'Seed 2', 'Seed 3', 'Seed 4', 'Seed 5'))
plt.show()

plt.figure(2)
plt.plot(fitness_progress[1,:,:])
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.show()
