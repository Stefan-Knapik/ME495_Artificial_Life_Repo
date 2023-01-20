import constants as c
from math import pi
import numpy as np
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:

    def __init__(self, jointName):

        self.jointName = jointName
        self.Prepare_To_Act()
        
    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset
        
        if self.jointName == "Torso_BackLeg":
            self.frequency = c.frequency * 0.5
        
        self.motorValues = self.amplitude * np.sin(self.frequency * np.linspace(0, 2*pi, c.num_steps) + self.offset)
        
    def Set_Value(self, desiredAngle, robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.maxForce)
        
    def Save_Values(self):
        np.save(f'data/MotorValues_{self.jointName}.npy', self.motorValues)