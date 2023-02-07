from solution import SOLUTION
import constants as c
import os
import copy
import time
import pickle
from tqdm import tqdm
import numpy as np

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        
        # os.system("del brain*.nndf > nul 2> nul")
        # os.system("del fitness*.txt > nul 2> nul")
        # os.system("del tmp*.txt > nul 2> nul")
        os.system("rmdir temp /s /q")
        os.system("mkdir temp")
        
        self.nextAvailableID = 0
        
        self.parents = {}
        for hc in range(c.populationSize):
            self.parents[hc] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        
    def Evolve(self):
        
        self.Evaluate(self.parents)
    
        pbar_evo = tqdm(total = c.numberOfGenerations, colour = 'green', 
                        desc = 'Evolution Progress', unit = 'generations',
                        disable = not c.progress_bar)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.Save_Best()
            
            pbar_evo.update(1)
        pbar_evo.close()
            
    def Evolve_For_One_Generation(self):
        # self.Spawn()
        self.Spawn_by_Copy_Crossover_or_Random()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        # self.Select_From_All()
        
    def Spawn(self):
        self.children = {}
        
        for hc in self.parents:
            self.children[hc+c.populationSize] = copy.deepcopy(self.parents[hc])
            self.children[hc+c.populationSize].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            
    def Spawn_by_Copy_Crossover_or_Random(self):
        
        # Sort parent by fitness
        ID_list = [x[0] for x in self.parents.items()]
        fitness_list = [x[1].fitness for x in self.parents.items()]
        parents = np.array([ID_list, fitness_list])
        parents = parents[:, parents[1,:].argsort()]
        
        # Select parents for crossover
        num_random = int(c.populationSize * c.randomPercentage)
        num_bred = int(c.populationSize * c.bredPercentage)
        num_copy = c.populationSize - num_random - num_bred
        breeding_parents = parents[0, 0:num_bred]
        copy_parents = parents[0, 0:num_copy]
        
        # Spawn
        self.children = {}
        N = c.populationSize     
        for hc in self.parents:
            if hc in breeding_parents:
                # Crossover
                parent1 = self.parents[hc]
                parent2 = self.parents[np.random.choice(breeding_parents)]
                self.children[hc+N] = copy.deepcopy(self.parents[hc])
                self.children[hc+N].weights = self.Crossover(parent1.weights, parent2.weights)
            elif hc in copy_parents:
                # Copy
                self.children[hc+N] = copy.deepcopy(self.parents[hc])
            else:
                # Random
                self.children[hc+N] = copy.deepcopy(self.parents[hc])
                self.children[hc+N].weights = 2 * np.random.rand(c.numSensorNeurons,c.numMotorNeurons) - 1
                
            self.children[hc+N].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            
    def Crossover(self, A_weights, B_weights):
        choice = np.random.randint(2, size = A_weights.size).reshape(A_weights.shape).astype(bool)
        return np.where(choice, A_weights, B_weights)
    
    def Mutate(self):
        for hc in self.parents:
            self.children[hc+c.populationSize].Mutate()
            
    def Evaluate(self, solutions):
        for hc in solutions:
            solutions[hc].Start_Simulation("DIRECT") # "DIRECT" or "GUI"
            
        for hc in solutions:
            solutions[hc].Wait_For_Simulation_To_End()
    
    def Select(self):
        for hc in self.parents:
            if self.parents[hc].fitness > self.children[hc+c.populationSize].fitness:
                self.parents[hc] = self.children[hc+c.populationSize]
                
    def Select_From_All(self):
        # Combine population into parents
        self.parents.update(self.children)
        
        # Sort population by fitness
        ID_list = [x[0] for x in self.parents.items()]
        fitness_list = [x[1].fitness for x in self.parents.items()]
        parents = np.array([ID_list, fitness_list])
        parents = parents[:, parents[1,:].argsort()]
        
        # Randomly kill low performers until population size is correct
        kill_list = []
        while parents.shape[1] > c.populationSize:
            kill_list = [kill_list, np.delete(parents, np.random.randint(-3,-1),1)]
        for unlucky_chap in kill_list:
            del self.parents[unlucky_chap]
            
    def Print(self):
        if c.printFitness == True:
            print()
            for hc in self.parents:
                print(f'Parent & Child Fitness: {self.parents[hc].fitness:11.6f} {self.children[hc+c.populationSize].fitness:11.6f}   \
                      {self.parents[hc].myID} {self.children[hc+c.populationSize].myID}')
            print()
        
    def Save_Best(self):
        # find the most fit parent
        self.bestParent = self.parents[0]
        for hc in self.parents:
            if self.parents[hc].fitness < self.bestParent.fitness:
                self.bestParent = self.parents[hc]
        
        # save the most fit parent
        f = open("BestFitness.txt", "w")
        f.write(str(self.bestParent.fitness))
        f.close()
        
        f = open("BestSolution.obj", "wb")
        pickle.dump(self.bestParent, f) 
        f.close()
        
    def Show_Best(self):
        self.Save_Best()
        # simulate the most fit parent
        self.bestParent.Show_Simulation()
        