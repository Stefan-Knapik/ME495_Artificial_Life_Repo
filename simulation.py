import pybullet as p
import time

num_steps = 1000
time_step_size = 1/60

physicsClient = p.connect(p.GUI)

for i in range(num_steps):
    p.stepSimulation()

    print(i)
    time.sleep(time_step_size)

p.disconnect()