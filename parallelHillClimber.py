from solution import SOLUTION
import constants as c
import os
import copy
import time
import pickle
from tqdm import tqdm
import numpy as np
import random

class PARALLEL_HILL_CLIMBER:

    def __init__(self, random_seed=0, algo='PHC'):
        
        self.nextAvailableID = 0
        self.algo = algo
        self.not_pareto_front = []
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        # os.system("del brain*.nndf > nul 2> nul")
        # os.system("del fitness*.txt > nul 2> nul")
        # os.system("del tmp*.txt > nul 2> nul")
        os.system("rmdir temp /s /q")
        os.system("mkdir temp")
        
        self.fitness_progress = np.zeros((c.numberOfGenerations, c.populationSize, 2))
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
            self.Evolve_For_One_Generation(currentGeneration)
            self.Save_Best(currentGeneration)
            
            pbar_evo.update(1)
        pbar_evo.close()
            
    def Evolve_For_One_Generation(self, currentGeneration):
        if self.algo == 'PHC':
            self.Spawn()
            self.Mutate()
            self.Evaluate(self.children)
            self.Print()
            self.Select()
        elif self.algo == 'AFPO':
            self.Spawn_AFPO()
            self.Mutate_AFPO()
            self.Evaluate(self.children)
            self.Print()
            self.Select_AFPO()
        else:
            print("Invalid algorithm, choose 'PHC' or 'AFPO'")
            exit()
        
    def Spawn(self):
        self.children = {}
        
        for hc in self.parents:
            self.children[hc] = copy.deepcopy(self.parents[hc])
            self.children[hc].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            
    def Spawn_AFPO(self):
        self.children = {}
        for hc in self.parents:
            self.children[hc] = copy.deepcopy(self.parents[hc])
            self.children[hc].Set_ID(self.nextAvailableID)
            if hc in self.not_pareto_front:
                self.children[hc] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for hc in self.parents:
            self.children[hc].Mutate()
            self.children[hc].age += 1
            self.parents[hc].age += 1
            
    def Mutate_AFPO(self):
        for hc in self.parents:
            if hc not in self.not_pareto_front:
                self.children[hc].Mutate()
                self.children[hc].age += 1
                self.parents[hc].age += 1
            
    def Evaluate(self, solutions):
        for hc in solutions:
            solutions[hc].Start_Simulation("DIRECT")
            
        for hc in solutions:
            solutions[hc].Wait_For_Simulation_To_End()
    
    def Select(self):
        for hc in self.parents:
            if self.parents[hc].fitness > self.children[hc].fitness:
                self.parents[hc] = self.children[hc]
                
    def Select_AFPO(self): 
        for hc in self.parents:
            if self.parents[hc].fitness > self.children[hc].fitness:
                self.parents[hc] = self.children[hc]
            if hc in self.not_pareto_front:
                self.parents[hc] = self.children[hc]
                
        criteria = np.zeros((c.populationSize, 2))
        for hc in self.parents:
            criteria[hc, 0] = self.parents[hc].fitness
            criteria[hc, 1] = self.parents[hc].age
        
        # get the pareto front
        safe_until_age = c.safe_until_age
        keep_best_percentile = c.keep_best_percentile
        
        self.not_pareto_front = []
        fitness_cutoff = np.percentile(criteria[:,0], keep_best_percentile)
        for hc in self.parents:
            better_fitness = criteria[hc,0] < np.delete(criteria[:,0], hc, axis=0)
            better_age = criteria[hc,1] < np.delete(criteria[:,1], hc, axis=0)
            if np.any(better_fitness + better_age == 0) \
                and self.parents[hc].age > safe_until_age \
                and self.parents[hc].fitness > fitness_cutoff:
                    
                self.not_pareto_front.append(hc)
        # print(criteria)
        # print(self.not_pareto_front)
        # input()
        
    def Print(self):
        if c.printFitness == True:
            print()
            for hc in self.parents:
                print(f'Parent & Child Fitness: {self.parents[hc].fitness:11.6f} {self.children[hc].fitness:11.6f}')
            print()
        
    def Save_Best(self, currentGeneration):
        # find the most fit parent
        self.bestParent = self.parents[0]
        for hc in self.parents:
            self.fitness_progress[currentGeneration, hc, 0] = self.parents[hc].fitness
            self.fitness_progress[currentGeneration, hc, 1] = self.parents[hc].age
            if self.parents[hc].fitness < self.bestParent.fitness:
                self.bestParent = self.parents[hc]
        
        # # save the most fit parent
        # if c.trials > 1:
        #     f = open(f"savePHC/BestFitness{self.random_seed}.txt", "w")
        #     f.write(str(self.bestParent.fitness))
        #     f.close()

        #     f = open(f"savePHC/BestSolution{self.random_seed}.obj", "wb")
        #     pickle.dump(self.bestParent, f) 
        #     f.close()
        
        # save the N best parents
        num = c.num_to_save
        hcs = np.argpartition(self.fitness_progress[currentGeneration,:, 0], num)[:num]
        idx_sort = np.argsort(self.fitness_progress[currentGeneration,hcs, 0])
        hcs = hcs[idx_sort]
        for i in range(num):
            hc = hcs[i]
            
            f = open(f"save/BestFitness_{self.algo}_RS{self.random_seed}_N{i}.txt", "w")
            f.write(str(self.parents[hc].fitness))
            f.close()

            f = open(f"save/BestSolution_{self.algo}_RS{self.random_seed}_N{i}.obj", "wb")
            pickle.dump(self.parents[hc], f) 
            f.close()
        
        # save the fitness progress
        np.save(f"save/FitnessProgress_{self.algo}_RS{self.random_seed}.npy", self.fitness_progress)
        
    def Show_Best(self):
        # simulate the most fit parent
        self.bestParent.Show_Simulation()
        