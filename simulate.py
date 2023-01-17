import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

num_steps = 1000
wait_time = 1/1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(num_steps)
frontLegSensorValues = np.zeros(num_steps)

for i in range(num_steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    print(i)
    time.sleep(wait_time)
np.save('data/backLegSensorValues.npy',backLegSensorValues)
np.save('data/frontLegSensorValues.npy',frontLegSensorValues)

p.disconnect()

