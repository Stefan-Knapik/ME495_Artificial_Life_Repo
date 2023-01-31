import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c

identical_worlds_and_bodies = True

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        self.myID = nextAvailableID
        self.weights = 2 * np.random.rand(c.numSensorNeurons,c.numSensorNeurons) - 1
        
    def Start_Simulation(self, directOrGUI):
        if identical_worlds_and_bodies == False or self.myID == 0:
            self.Create_World()
            self.Create_Body()
        
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID} > nul 2> nul")
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")
           
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.001)
            
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        # print(f"\n{self.myID}   {self.fitness}  ----------------------")
        os.system(f"del fitness{self.myID}.txt")
    
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-3, 3, 0.5] , size=[1, 1, 1])
        pyrosim.End()
        
        while not os.path.exists("world.sdf"):
            time.sleep(0.001)
        
    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        pyrosim.Send_Cube(name="Torso", pos=[0.0, 0.0, 1.0] , size=[1.0, 1.0, 1.0])
        
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", 
                           position = [0.0, -0.5, 1.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0.0, -0.5, 0.0] , size=[0.2, 1.0, 0.2])
        
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", 
                           position = [0.0, 0.5, 1.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.0, 0.5, 0.0] , size=[0.2, 1.0, 0.2])
        
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", 
                           position = [-0.5, 0.0, 1.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0.0, 0.0] , size=[1.0, 0.2, 0.2])
        
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", 
                           position = [0.5, 0.0, 1.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0.0, 0.0] , size=[1.0, 0.2, 0.2])
        
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", 
                           position = [0.0, -1.0, 0.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0.0, 0.0, -0.5] , size=[0.2, 0.2, 1.0])
        
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", 
                           position = [0.0, 1.0, 0.0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0.0, 0.0, -0.5] , size=[0.2, 0.2, 1.0])
        
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", 
                           position = [-1.0, 0.0, 0.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0.0, 0.0, -0.5] , size=[0.2, 0.2, 1.0])
        
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", 
                           position = [1.0, 0.0, 0.0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0.0, 0.0, -0.5] , size=[0.2, 0.2, 1.0])
        
        pyrosim.End()
        
        while not os.path.exists("body.urdf"):
            time.sleep(0.001)
        
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")
        
        pyrosim.Send_Motor_Neuron(name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 11 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 12 , jointName = "Torso_RightLeg")
        
        pyrosim.Send_Motor_Neuron(name = 13 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 14 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 15 , jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 16 , jointName = "RightLeg_RightLowerLeg")
        
        for currentRow in range(0,c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , 
                                    targetNeuronName = currentColumn + c.numSensorNeurons, 
                                    weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        
        while not os.path.exists(f"brain{self.myID}.nndf"):
            time.sleep(0.001)
        
    def Mutate(self):
        randomRow = np.random.randint(0,c.numSensorNeurons)
        randomColumn = np.random.randint(0,c.numMotorNeurons)
        self.weights[randomRow,randomColumn] = np.random.random() * 2 - 1
        
    def Set_ID(self, ID):
        self.myID = ID
        
    def Show_Simulation(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"start /B python simulate.py GUI {self.myID} > nul")
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")