# import pybullet as p
# import pybullet_data
# import time
# import pyrosim.pyrosim as pyrosim
# import numpy as np
# from math import pi
# import random
# import constants as c
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()



# targetAnglesBackLeg = c.amplitudeBackLeg * np.sin(c.frequencyBackLeg * np.linspace(0, 2*pi, num_steps) + c.phaseOffsetBackLeg)
# targetAnglesFrontLeg = c.amplitudeFrontLeg * np.sin(c.frequencyFrontLeg * np.linspace(0, 2*pi, num_steps) + c.phaseOffsetFrontLeg)
# # np.save('data/targetAnglesBackLeg.npy', targetAnglesBackLeg)
# # np.save('data/targetAnglesFrontLeg.npy', targetAnglesFrontLeg)
# # exit()

# for i in range(num_steps):
#     p.stepSimulation()
#     backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex = robotId,
#         jointName = 'Torso_BackLeg',
#         controlMode = p.POSITION_CONTROL,
#         targetPosition = targetAnglesBackLeg[i],
#         maxForce = c.maxForceBackLeg)
    
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex = robotId,
#         jointName = 'Torso_FrontLeg',
#         controlMode = p.POSITION_CONTROL,
#         targetPosition = targetAnglesFrontLeg[i],
#         maxForce = c.maxForceFrontLeg)

#     print(i)
#     time.sleep(wait_time)
    
# np.save('data/backLegSensorValues.npy', backLegSensorValues)
# np.save('data/frontLegSensorValues.npy', frontLegSensorValues)

# p.disconnect()

