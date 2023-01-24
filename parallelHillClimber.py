import os
from solution import SOLUTION
import constants as c
import copy
import time
from tqdm import tqdm

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        
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
            
            pbar_evo.update(1)
        pbar_evo.close()
            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        
    def Spawn(self):
        self.children = {}
        
        for hc in self.parents:
            self.children[hc] = copy.deepcopy(self.parents[hc])
            self.children[hc].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for hc in self.parents:
            self.children[hc].Mutate()
            
    def Evaluate(self, solutions):
        for hc in solutions:
            solutions[hc].Start_Simulation("DIRECT")
            
        for hc in solutions:
            solutions[hc].Wait_For_Simulation_To_End()
    
    def Select(self):
        for hc in self.parents:
            if self.parents[hc].fitness > self.children[hc].fitness:
                self.parents[hc] = self.children[hc]
            
    def Print(self):
        if c.printFitness == True:
            print()
            for hc in self.parents:
                print(self.parents[hc].fitness, self.children[hc].fitness, sep = '    ')
            print()
        
    def Show_Best(self):
        # find the most fit parent
        self.bestParent = self.parents[0]
        for hc in self.parents:
            if self.parents[hc].fitness < self.bestParent.fitness:
                self.bestParent = self.parents[hc]
        
        # simulate the most fit parent with graphics and print/save its fitness
        f = open("BestFitness.txt", "w")
        f.write(str(self.bestParent.fitness))
        f.close()
        # print(f"\n {self.bestParent.fitness} \n")
        
        self.bestParent.Start_Simulation("GUI")
        

        
        