import constants as c
from math import pi
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:

    def __init__(self, jointName):

        self.jointName = jointName
        
    def Set_Value(self, desiredAngle, robotId):
        
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.maxForce)
        