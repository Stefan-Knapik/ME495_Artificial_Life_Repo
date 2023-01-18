from world import WORLD
from robot import ROBOT
import constants as c
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np

class SIMULATION:

    def __init__(self):
        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)
        
        self.world = WORLD()
        self.robot = ROBOT()
        
    def Run(self):
        for i in range(c.num_steps):
            p.stepSimulation()
            
            self.robot.Sense()
            
            
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = 'Torso_BackLeg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = targetAnglesBackLeg[i],
            #     maxForce = c.maxForceBackLeg)
            
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = robotId,
            #     jointName = 'Torso_FrontLeg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = targetAnglesFrontLeg[i],
            #     maxForce = c.maxForceFrontLeg)

            print(i)
            time.sleep(c.wait_time)
            
    def __del__(self):
        p.disconnect()
                