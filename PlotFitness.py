import pickle
import numpy as np
import matplotlib.pyplot as plt
import constants as c
import matplotlib.cm as cm
import matplotlib.animation as animation

font_size = 14

algo = 'PHC' # 'PHC' or 'AFPO'
fitness_progressA = np.zeros((c.trials, c.numberOfGenerations, c.populationSize, 2))
for seed in range(1, c.trials+1):
    fitness_progressA[seed-1,:,:,:] = np.load(f"save/FitnessProgress_{algo}_RS{seed}.npy")
fitness_progressA[:,:,:,0] = -fitness_progressA[:,:,:,0]

algo = 'AFPO' # 'PHC' or 'AFPO'
fitness_progressB = np.zeros((c.trials, c.numberOfGenerations, c.populationSize, 2))
for seed in range(1, c.trials+1):
    fitness_progressB[seed-1,:,:,:] = np.load(f"save/FitnessProgress_{algo}_RS{seed}.npy")
fitness_progressB[:,:,:,0] = -fitness_progressB[:,:,:,0]

# Fitness progression across trials
plt.figure(1)
for seed in range(0, c.trials):
    plt.plot(fitness_progressA[seed,:,:,0].max(axis=1), 'r', label='PHC' if seed==0 else None)
for seed in range(0, c.trials):
    plt.plot(fitness_progressB[seed,:,:,0].max(axis=1), 'b', label='AFPO' if seed==0 else None)
plt.ylabel('Best Fitness', fontsize=font_size)
plt.xlabel('Generation', fontsize=font_size)
plt.title('Evolutionary Progression of Fitness', fontsize=font_size+2)
plt.legend(loc="upper left")
plt.savefig('BestFitnessObserved.png', dpi=300)
plt.show()

# Fitness progression across a population
seed = 0
plt.figure(2)
plt.plot(fitness_progressA[seed,:,:,0])
plt.ylabel('Fitness', fontsize=font_size)
plt.xlabel('Generation', fontsize=font_size)
plt.title('Trial 1', fontsize=font_size+2)
plt.show()


# Fitness progression across a population, animated points
seed = 0
xmax = max(np.max(fitness_progressA[seed,:,:,1]), np.max(fitness_progressB[seed,:,:,1]))
xmin = min(np.min(fitness_progressA[seed,:,:,1]), np.min(fitness_progressA[seed,:,:,1]))
ymax = max(np.max(fitness_progressA[seed,:,:,0]), np.max(fitness_progressB[seed,:,:,0]))
ymin = min(np.min(fitness_progressA[seed,:,:,0]), np.min(fitness_progressA[seed,:,:,0]))
for i in range(fitness_progressA.shape[1]):
    plt.figure(3)
    plt.plot(fitness_progressA[seed,i,:,1], fitness_progressA[seed,i,:,0], '.r', markersize=10, label='PHC')
    plt.plot(fitness_progressB[seed,i,:,1], fitness_progressB[seed,i,:,0], '.b', markersize=10, label='AFPO')
    plt.ylabel('Fitness', fontsize=font_size)
    plt.xlabel('Age', fontsize=font_size)
    plt.title(f'Generation {i+1:04d}', fontsize=font_size+2)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax+1)
    plt.legend(loc="upper left")
    plt.savefig(f'video/Generation{i+1:04d}.png', dpi=300)
    # plt.show()
    plt.clf() 
    
    
    


