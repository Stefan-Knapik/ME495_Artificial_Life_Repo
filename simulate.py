import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy

num_steps = 1000
time_step_size = 1/200

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(num_steps)

for i in range(num_steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")

    print(i)
    time.sleep(time_step_size)

p.disconnect()

print(backLegSensorValues)
