import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c

identical_worlds_and_bodies = False

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        self.myID = nextAvailableID
        
        self.min_len = 0.5
        self.max_len = 2
        self.number_of_links = np.random.randint(4, 10)
        self.links_shape = np.zeros(self.number_of_links) # All zeros for all cubes
        
        self.links_sizes = self.min_len + (self.max_len - self.min_len) * np.random.rand(self.number_of_links, 3)
        self.links_sensor = np.random.randint(0,2, size=self.number_of_links)
        
        self.numSensorNeurons = sum(self.links_sensor)
        self.numMotorNeurons = self.number_of_links - 1
        self.weights = 2 * np.random.rand(self.numSensorNeurons,self.numMotorNeurons) - 1
        
    def Start_Simulation(self, directOrGUI):
        if identical_worlds_and_bodies == False or self.myID == 0:
            self.Create_World()
            self.Create_Body()
        
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID} > nul 2> nul")
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")
           
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
        
        # Root link and first joint (absolute coords)
        current_link_size = self.links_sizes[0,:].tolist()
        current_joint_loc = (np.array([-0.5, 0, 0]) * self.links_sizes[0,0] + np.array([0, 0, self.max_len])).tolist()
        colorname = 'green' if self.links_sensor[0] == 1 else 'blue'
        pyrosim.Send_Cube(name="0", pos=[0.0, 0.0, self.max_len] , size=current_link_size, color=colorname)
        pyrosim.Send_Joint(name = "0_1" , parent= "0" , child = "1" , type = "revolute", 
                            position = current_joint_loc, jointAxis = "0 1 0")
        
        for i in range(1, self.number_of_links):
            current_link_size = self.links_sizes[i,:].tolist()
            current_link_loc = (np.array([-0.5, 0, 0]) * self.links_sizes[i,0]).tolist()
            current_joint_loc = (np.array([-1, 0, 0]) * self.links_sizes[i,0]).tolist()
            colorname = 'green' if self.links_sensor[i] == 1 else 'blue'
            
            pyrosim.Send_Cube(name=f"{i}", pos=current_link_loc
                              , size=current_link_size , color=colorname)
            
            if i < self.number_of_links - 1:
                pyrosim.Send_Joint(name = f"{i}_{i+1}" , parent= f"{i}" , child = f"{i+1}" , type = "revolute", 
                                    position = current_joint_loc, jointAxis = "0 1 0")
            
        pyrosim.End()
        
        while not os.path.exists("temp\\body.urdf"):
            time.sleep(0.001)
        
    def Create_Brain(self):
        
        pyrosim.Start_NeuralNetwork(f"temp\\brain{self.myID}.nndf")
        n_num = 0
        
        for i in range(len(self.links_sensor)):
            if self.links_sensor[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = n_num , linkName = f"{i}"); n_num += 1
                
        for i in range(self.number_of_links - 1):
            pyrosim.Send_Motor_Neuron(name = n_num , jointName = f"{i}_{i+1}"); n_num += 1
            
        for currentRow in range(0,self.numSensorNeurons):
            for currentColumn in range(0,self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , 
                                    targetNeuronName = currentColumn + self.numSensorNeurons, 
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