# f = open(f"./fitness{181}.txt", "r")

# print(float(f.read()))
        
# f.close()


import numpy as np

# rng = np.random.default_rng(0)
np.random.seed(1)

x = np.random.randint(5, 30)
y = np.random.randint(5, 30)

print(x, y)