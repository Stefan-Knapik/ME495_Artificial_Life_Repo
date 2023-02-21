import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import pandas as pd

identical_worlds_and_bodies = False

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        self.myID = nextAvailableID
        
        self.min_len = 1
        self.max_len = 1
        self.root_height = 5
        
        self.prob_sensor = 0.5
        
        self.link_lim = 3 # max number of links
        self.layer_lim = 3 # max number of layers
        self.children_lim = 3 # max number of children per link
        
        
        # self.number_of_links = np.random.randint(4, 5)
        # self.links_shape = np.random.randint(0,2, size=self.number_of_links) # 0 = box, 1 = cylinder
        # self.joint_direction = np.random.randint(0,2, size=self.number_of_links) # 0 = z, 1 = y
        
        # self.links_sizes = self.min_len + \
        #                     (self.max_len - self.min_len) * np.random.rand(self.number_of_links, 3) + \
        #                     self.min_len * np.outer(np.ones(self.number_of_links), np.array([1,0,0])) # bias longer in x direction
        # self.links_sensor = np.random.randint(0,2, size=self.number_of_links) # 0 = no sensor, 1 = sensor
        
        # self.numSensorNeurons = sum(self.links_sensor)
        # self.numMotorNeurons = self.number_of_links - 1
        # self.weights = 2 * np.random.rand(self.numSensorNeurons,self.numMotorNeurons) - 1
        
        
        
        
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
        
        # Preallocate link parameter storage
        link_info = np.zeros((self.link_lim, 6)) # idx of dim1 is link number
        # 0-2 xyz, 3 diameter, 4 sensor, 5 eligibility, 6-8 parent joint absolute location, 9-11 parent joint direction
        tree_info = pd.DataFrame() # idx of dim1 is link number
        # 0 layer, 1 parent, 2 children
        
        # Root link and first joint (absolute coords)
        i = 0
        x = 0
        y = 0
        z = self.root_height
        d = self.max_len
        s = np.random.randint(0,2) # 0 = no sensor, 1 = sensor
        e = 1
        
        layer = 1
        parent = None
        children = []
        
        colorname = 'green' if s == 1 else 'blue'
        
        pyrosim.Send_Cube(name=f"{i}", pos=[x,y,z], size=d, color=colorname, shape=2)
        link_info[i,:] = [x, y, z, d, s, e]
        # tree_info[i,:] = [layer, parent, children]
        
        for i in range(1, self.link_lim):
            link_added = False
            while not link_added:
                # pick a random parent from eligible parents
                eligible_parents = np.argwhere(link_info[:,5] == 1)
                parent = np.random.choice(eligible_parents)
                
                # randomly spawn a joint location
                seed = np.random.normal(size=3)
                norm = np.linalg.norm(seed)
                if norm == 0: seed[0] = 1 
                direction = seed/norm 
                
                # randomly spawn a link
                d = self.min_len + (self.max_len - self.min_len) * np.random.rand()
                center = link_info[parent,0:2] + 0.5*(link_info[parent,3]+d)*direction
                
                # check for collision with floor or other sphere, and if so, try again
                if center[2] <= 0.5*d:
                    break
                vecd = center - link_info[0:i-1,0:2]
                distance = np.linalg.norm(vecd, axis=1)
                sum_radii = 0.5 * (link_info[0:i-1,3] + d)
                if min(distance-sum_radii) <= 0:
                    break
                
                # if no collision, add joint and link
                link_info[i,:] = [x, y, z, d, s, e]
                tree_info[i,:] = [layer, parent, children]  
                
                if parent == 0:
                    link_info[i,6:8] = link_info[0,0:2] + 0.5*link_info[0,3]*direction
                    link_info[i,9:11] = direction
                    current_link_loc = (link_info[0,0:2] + 0.5*(link_info[0,3] + d)*direction).tolist()
                    current_joint_loc = (link_info[i,6:8]).tolist()
                else:
                    link_info[i,6:8] = link_info[parent,6:8] + 0.5*(link_info[parent,3]*link_info[parent,9:11] + d*direction)
                    link_info[i,9:11] = direction
                    
                    current_link_loc = (link_info[i,0:2] - link_info[parent,6:8]).tolist()
                    current_joint_loc = (link_info[i,6:8] - link_info[parent,6:8]).tolist()
                    
                pyrosim.Send_Joint(name = f"{parent}_{i}" , parent= f"{parent}" , child = f"{i}" , type = "revolute", 
                                    position = current_joint_loc, jointAxis = "0 0 1")
                pyrosim.Send_Ball(name=f"{i}", pos=current_link_loc, size=d, color=colorname, shape=2)
        
                link_added = True
            
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