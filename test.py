# f = open(f"./fitness{181}.txt", "r")

# print(float(f.read()))
        
# f.close()

import numpy as np
from solution import SOLUTION

np.random.seed(9)

x = SOLUTION(0)
x.Start_Simulation('GUI')