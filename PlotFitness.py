import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants as c
import matplotlib.cm as cm
import matplotlib.animation as animation

font_size = 14
    
fitness_progress = np.zeros((c.trials, c.numberOfGenerations, c.populationSize, 2))
for seed in range(1, c.trials+1):
    fitness_progress[seed-1,:,:,:] = np.load(f"savePHC/FitnessProgress_RS{seed}.npy")
fitness_progress[:,:,:,0] = -fitness_progress[:,:,:,0]

plt.figure(1)
for seed in range(0, c.trials):
    plt.plot(fitness_progress[seed,:,:,0].max(axis=1))
plt.ylabel('Best Fitness', fontsize=font_size)
plt.xlabel('Generation', fontsize=font_size)
plt.title('Evolutionary Progression of Fitness', fontsize=font_size+2)
plt.legend(('Random Seed 1', 'Random Seed 2', 'Random Seed 3', 'Random Seed 4', 'Random Seed 5'))
plt.savefig('BestFitnessObserved.png', dpi=300)
plt.show()

plt.figure(2)
plt.plot(fitness_progress[0,:,:,0])
plt.ylabel('Fitness', fontsize=font_size)
plt.xlabel('Generation', fontsize=font_size)
plt.title('Trial 1', fontsize=font_size+2)
plt.show()

for i in range(fitness_progress.shape[1]):
    plt.figure(3)
    plt.plot(fitness_progress[0,i,:,1], fitness_progress[0,i,:,0], '.', markersize=10)
    plt.ylabel('Fitness', fontsize=font_size)
    plt.xlabel('Age', fontsize=font_size)
    plt.title(f'Generation {i+1:04d}', fontsize=font_size+2)
    plt.xlim(np.min(fitness_progress[0,:,:,1]), np.max(fitness_progress[0,:,:,1])+1)
    plt.ylim(np.min(fitness_progress[0,:,:,0]), np.max(fitness_progress[0,:,:,0])+1)
    plt.savefig(f'video/Generation{i+1:04d}.png', dpi=300)
    plt.clf() 
    
    


