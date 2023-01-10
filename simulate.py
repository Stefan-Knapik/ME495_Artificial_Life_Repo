import pybullet as p
import time

num_steps = 1000
time_step_size = 1/200

physicsClient = p.connect(p.GUI)

p.loadSDF("box.sdf")

for i in range(num_steps):
    p.stepSimulation()

    print(i)
    time.sleep(time_step_size)

p.disconnect()