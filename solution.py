import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c

identical_worlds_and_bodies = True

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        self.myID = nextAvailableID
        self.weights = 2 * np.random.rand(c.numSensorNeurons,c.numMotorNeurons) - 1
        
    def Start_Simulation(self, directOrGUI):
        if identical_worlds_and_bodies == False or self.myID == 0:
            self.Create_World()
            self.Create_Body()
        
        self.Create_Brain()
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID} > nul 2> nul")
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")
           
    def Wait_For_Simulation_To_End(self):
        
        fpath = f"temp\\fitness{self.myID}.txt"
        
        # while not os.path.exists(fpath):
        #     time.sleep(0.001)
        for i in range(1000):
            if os.path.exists(fpath):
                break
            time.sleep(0.001)
        
        assert os.path.isfile(fpath)
        
        f = open(fpath, "r")
        self.fitness = float(f.read())
        f.close()
        # print(f"\n{self.myID}   {self.fitness}  ----------------------")
        os.system(f"del temp\\fitness{self.myID}.txt")
    
    def Create_World(self):
        pyrosim.Start_SDF("temp\\world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[-3, 3, 0.5] , size=[1, 1, 1])
        pyrosim.End()
        
        while not os.path.exists("temp\\world.sdf"):
            time.sleep(0.001)
        
    def Create_Body(self):
        
        pyrosim.Start_URDF("temp\\body.urdf")
        
        radius = 1 # radius of circumscribed circle
        thickness = 0.05 # thickness of the loop, radial
        width = 1 # width of the loop, axial
        
        edge_length = 2*radius*np.tan(np.pi/c.numLinks)
        dimensions = [edge_length, width, thickness]
        angle = np.pi/c.numLinks
        
        pyrosim.Send_Cube(name="0", pos=[0,0,thickness] , size=dimensions)
        pyrosim.Send_Joint(name = "0_1" , parent= "0" , child = "1" , type = "revolute", 
                            position = [-0.5*edge_length, 0.0, thickness], jointAxis = "0 1 0")
        
        for i in range(1,c.numLinks):
            angle = i * np.pi/c.numLinks 
            relative_center = 0.5 * edge_length * np.array([-np.cos(2*angle), 0, np.sin(2*angle)])
            relative_joint = relative_center * 2
            
            print(angle, relative_center, relative_joint)
        
            pyrosim.Send_Cube(name=f"{i}", pos=relative_center.tolist() , size=dimensions, rpy = [0.0, angle, 0.0])
            
            if i < c.numLinks - 1:
                pyrosim.Send_Joint(name = f"{i}_{i+1}" , parent= f"{i}" , child = f"{i+1}" , type = "revolute", 
                                    position = relative_joint, jointAxis = "0 1 0")
                print(f"{i}_{i+1}")
        
        # for i in range(c.numLinks):
            
        #     angle = i * np.pi/c.numLinks 
            
        #     center = np.array([0,0,radius+thickness]) + np.array([radius*np.sin(angle), 0, -radius*np.cos(angle)])
       
        #     pyrosim.Send_Cube(name=f"{i}", pos=center.tolist() , size=dimensions.tolist()) # , rpy = [0.0, angle, 0.0]
            
        #     if i == c.numLinks - 1:
        #         pyrosim.Send_Joint(name = f"{0}_{i}" , parent= f"{0}" , child = f"{i}" , type = "revolute", 
        #                         position = [-0.5*edge_length, 0.0, 0.5*thickness], jointAxis = "0 1 0")
        #     else:
        #         pyrosim.Send_Joint(name = f"{i}_{(i+1)%c.numLinks}" , parent= f"{i}" , child = f"{(i+1)%c.numLinks}" , type = "revolute", 
        #                         position = [-0.5*edge_length, 0.0, 0.5*thickness], jointAxis = "0 1 0", rpy=[0.0, angle, 0.0])

        pyrosim.End()
        
        while not os.path.exists("temp\\body.urdf"):
            time.sleep(0.001)
        
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"temp\\brain{self.myID}.nndf")
        
        for i in range(c.numLinks):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = f"{i}"); 
            pyrosim.Send_Motor_Neuron(name = i + c.numLinks , jointName = f"{i}_{(i+1)%c.numLinks}");
            
        for currentRow in range(0,c.numSensorNeurons):
            for currentColumn in range(0,c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , 
                                    targetNeuronName = currentColumn + c.numSensorNeurons, 
                                    weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
        
        while not os.path.exists(f"temp\\brain{self.myID}.nndf"):
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