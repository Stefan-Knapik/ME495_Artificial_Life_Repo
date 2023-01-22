from solution import SOLUTION
import constants as c
import copy
import time
from tqdm import tqdm

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        
        self.parents = {}
        for hc in range(c.populationSize):
            self.parents[hc] = SOLUTION()
        
        # self.parent = SOLUTION()
        
    def Evolve(self):
        
        for hc in self.parents:
            self.parents[hc].Evaluate("GUI")
    
        # self.parent.Evaluate("GUI")
        
        # pbar_evo = tqdm(total = c.numberOfGenerations, colour = 'green', 
        #                 desc = 'Evolution Progress', unit = 'generations',
        #                 disable = not c.progress_bar)
        
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()
            
        #     pbar_evo.update(1)
        # pbar_evo.close()
            
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()
        
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
    
    def Mutate(self):
        self.child.Mutate()
    
    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
            
    def Print(self):
        print('\n------------', self.parent.fitness, self.child.fitness, '------------', sep = '    ')
        
    def Show_Best(self):
        pass
    
        # self.parent.Evaluate("GUI")
        
        