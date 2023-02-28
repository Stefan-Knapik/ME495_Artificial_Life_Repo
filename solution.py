import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import pandas as pd

identical_worlds_and_bodies = False

class SOLUTION:

    def __init__(self, nextAvailableID, random_seed=0):
        
        self.myID = nextAvailableID
        np.random.seed(random_seed)
        
        self.min_len = 0.2
        self.max_len = 0.5
        self.root_height = 1.2
        
        self.link_lim = np.random.randint(5, 20)
        self.layer_lim = 99 #np.random.randint(10)
        self.children_lim = np.random.randint(1, 4)
        
        self.prob_sensor = 0.5
        self.connect_factor = 0.99 # bring spheres together by this factor
            
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
        
        pyrosim.Start_URDF(f"temp\\body{self.myID}.urdf")
        
        # Preallocate link parameter storage
        link_info = np.zeros((self.link_lim, 13)) # idx of dim1 is link number
        # 0-2 xyz, 3 diameter, 4 sensor, 5 eligibility, 
        # 6-8 parent joint absolute location, 9-11 parent joint direction
        # 12 layer number
        children = np.empty((self.link_lim,), dtype=object)
        joints = np.empty((self.link_lim - 1,2) ,dtype=int)
        
        # tree_info = pd.DataFrame() # idx of dim1 is link number
        # 0 layer, 1 parent, 2 children
        
        # Root link and first joint (absolute coords)
        i = 0
        x = 0
        y = 0
        z = self.root_height
        d = self.max_len
        s = np.random.randint(0,2) # 0 = no sensor, 1 = sensor
        
        # layer = 1
        # parent = None
        # children = []
        
        colorname = 'green' if s == 1 else 'blue'
        pyrosim.Send_Cube(name=f"{i}", pos=[x,y,z], size=d, color=colorname, shape=2)
        link_info[i,0:6] = [x, y, z, d, s, 1]
        # tree_info[i,0:3] = [layer, parent, children]
        
        collision_counter = [0,0]
        
        for i in range(1, self.link_lim):
            link_added = False
            while not link_added:
                # pick a random parent from eligible parents
                eligible_parents = np.squeeze(np.argwhere(link_info[:,5] == 1), axis=1)
                parent = np.random.choice(eligible_parents)
                
                # randomly spawn a joint location
                seed = np.random.normal(size=3)
                norm = np.linalg.norm(seed)
                if norm == 0: seed[0] = 1 
                direction = seed/norm 
                
                # randomly spawn a link
                d = self.min_len + (self.max_len - self.min_len) * np.random.rand()
                
                center = link_info[parent,0:3] + 0.5*self.connect_factor*(link_info[parent,3]+d)*direction
                
                # check for collision with floor or other sphere, and if so, try again
                if center[2] <= 0.5*d:
                    print(f"{collision_counter[0]} floor collision")
                    collision_counter[0] += 1
                    continue
                
                if i > 1:
                    links_to_check = np.delete(link_info[0:i,0:4],parent,0)
                    # print(links_to_check.shape[0])
                    # print(np.repeat(center,links_to_check.shape[0],0))
                    # print(links_to_check)
                    # exit()
                    vecd = center - links_to_check[:,0:3]
                    distance = np.linalg.norm(vecd, axis=1)
                    sum_radii = 0.5 * (links_to_check[:,3] + d)
                    if min(distance-sum_radii) <= -0.1:
                        print(f"{collision_counter[1]} link collision")
                        collision_counter[1] += 1
                        continue
                
                # if no collision, add joint and link
                s = np.random.randint(0,2) # 0 = no sensor, 1 = sensor
                link_info[i,0:6] = [center[0], center[1], center[2], d, s, 1]
                # tree_info[i,:] = [layer, parent, children]  
                
                link_info[i,6:9] = link_info[parent,0:3] + 0.5*link_info[parent,3]*direction
                link_info[i,9:12] = direction
                link_info[i,12] = link_info[parent,12] + 1
                
                current_link_loc = (0.5*self.connect_factor*d*direction).tolist()
                if parent == 0:
                    current_joint_loc = (link_info[i,6:9]).tolist()
                else:
                    current_joint_loc = (link_info[i,6:9] - link_info[parent,6:9]).tolist()
                
                
                # generate a random axis perpendicular to the joint direction
                seed = np.random.normal(size=3)
                norm = np.linalg.norm(seed)
                if norm == 0: seed[0] = 1 
                directionJ = seed/norm 
                joint_axis = directionJ - np.dot(directionJ, direction)*direction
                joint_axis = np.array2string(joint_axis, separator=' ')[2:-1]
                
                # generate a joint axis aligned with its direction
                # joint_axis = np.array2string(link_info[i,9:12], separator=' ')[2:-1] 
                    
                pyrosim.Send_Joint(name = f"{parent}_{i}" , parent= f"{parent}" , child = f"{i}" , type = "revolute", 
                                    position = current_joint_loc, jointAxis = joint_axis)
                
                colorname = 'green' if s == 1 else 'blue'
                pyrosim.Send_Cube(name=f"{i}", pos=current_link_loc, size=d, color=colorname, shape=2)
        
                joints[i-1,0] = parent
                joints[i-1,1] = i
                
                num_children = (joints[:,0] == parent).sum() # counts children of parent
                if num_children >= self.children_lim:
                    link_info[parent,5] = 0
                if link_info[i,12] >= self.layer_lim:
                    link_info[i,5] = 0
                
                link_added = True
            
        pyrosim.End()
        
        self.link_info = link_info
        self.joints = joints
        self.numSensorNeurons = int(np.sum(link_info[:,4]))
        self.numMotorNeurons = self.link_lim - 1
        
        while not os.path.exists(f"temp\\body{self.myID}.urdf"):
            time.sleep(0.001)
        
    def Create_Brain(self):
        
        pyrosim.Start_NeuralNetwork(f"temp\\brain{self.myID}.nndf")
        n_num = 0
        self.weights = 2 * np.random.rand(self.numSensorNeurons,self.numMotorNeurons) - 1
        
        for i in range(self.link_lim):
            if self.link_info[i,4] == 1:
                pyrosim.Send_Sensor_Neuron(name = n_num , linkName = f"{i}"); n_num += 1
                
        for i in range(self.link_lim - 1):
            pyrosim.Send_Motor_Neuron(name = n_num , jointName = f"{self.joints[i,0]}_{self.joints[i,1]}"); n_num += 1
            
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