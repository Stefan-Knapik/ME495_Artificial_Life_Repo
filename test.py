# f = open(f"./fitness{181}.txt", "r")

# print(float(f.read()))
        
# f.close()

import numpy as np
from solution import SOLUTION
import random

seed = 0
random.seed(seed)
np.random.seed(seed)

x = SOLUTION(seed)
x.Start_Simulation('GUI')

for i in range(10):
    x.Mutate()

print(1)
input()
x.Start_Simulation('GUI')
