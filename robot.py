from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:

    def __init__(self):
        
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain.nndf")
        
    def Prepare_To_Sense(self):
        self.sensors = {}
        
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        
    def Sense(self, time_step):
        for linkName in self.sensors:
            self.sensors[linkName].Get_Value(time_step)
            
    def Prepare_To_Act(self):
        self.motors = {} 
        
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
            
    def Act(self, time_step):
        for jointName in self.motors:
            self.motors[jointName].Set_Value(time_step, self.robotId)
            
    def Think(self):
        self.nn.Print()
        
            

        
        
    
