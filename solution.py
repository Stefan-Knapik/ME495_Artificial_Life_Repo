import os
import numpy as np
import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        self.myID = nextAvailableID
        self.weights = 2 * np.random.rand(3,2) - 1
           
    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python simulate.py " + directOrGUI)
        f = open("fitness.txt", "r")
        self.fitness = float(f.read())
        f.close()
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[x-3, y+3, z] , size=[length, width, height])
        pyrosim.End()
        
        while not os.path.exists("world.sdf"):
            time.sleep(0.0001)
        
    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5] , size=[length, width, height])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[length, width, height])
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[length, width, height])
        pyrosim.End()
        
        while not os.path.exists("body.urdf"):
            time.sleep(0.0001)
        
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")
        
        for currentRow in [0, 1, 2]:
            for currentColumn in [0, 1]:
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , 
                                    targetNeuronName = currentColumn + 3 , 
                                    weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        
        while not os.path.exists("brain.nndf"):
            time.sleep(0.0001)
        
    def Mutate(self):
        randomRow = np.random.randint(0,3)
        randomColumn = np.random.randint(0,2)
        self.weights[randomRow,randomColumn] = np.random.random() * 2 - 1
        
    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID
        