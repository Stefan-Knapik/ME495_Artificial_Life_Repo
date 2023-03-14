import os
import time
import numpy as np
import pyrosim.pyrosim as pyrosim
import constants as c
import pandas as pd
import copy

identical_worlds = True

class SOLUTION:

    def __init__(self, nextAvailableID):
        
        # Parameters
        self.min_len = 0.2
        self.max_len = 0.8
        self.root_height = 1.2
        
        self.num_links = np.random.randint(5, 20)
        self.num_link_max = 40
        self.num_link_min = 4
        
        self.layer_lim = 99 #np.random.randint(10)
        self.children_lim = np.random.randint(3, 7)
        
        self.sensor_prob = 0.5
        
        self.wiggle_room = 0.2
        self.connect_factor = 0.99 # bring spheres together by this factor
        
        # Initialize ID
        self.myID = nextAvailableID
        self.age = 0
        # Initialize Body
        self.Initialize_Body()
        # Initialize Brain
        self.weights = 2 * np.random.rand(self.numSensorNeurons,self.numMotorNeurons) - 1
            
    def Start_Simulation(self, directOrGUI):
        if identical_worlds == False or self.myID == 0:
            self.Create_World()
        
        self.Create_Body()
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID} > nul 2> nul")
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")
           
    def Wait_For_Simulation_To_End(self):
        
        fpath = f"temp\\fitness{self.myID}.txt"
        
        # while not os.path.exists(fpath):
        #     time.sleep(0.001)
        
        # for i in range(2000):
        #     if os.path.exists(fpath):
        #         break
        #     time.sleep(0.01)
        # assert os.path.isfile(fpath)
        # f = open(fpath, "r")
        
        while True:
            try:
                f = open(fpath, "r")
                break
            except:
                time.sleep(0.01)
                
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
            
    def Initialize_Body(self):
        
        # Preallocate storage
        self.links = np.zeros((self.num_links, 17)) # dim0 is link number
                # 0-2 xyz, 3 diameter, 4 sensor, 
                # 5 eligibility, 6 layer number, 7 parent link number
                # 8-10 parent joint absolute location, 
                # 11-13 parent joint absolute direction,
                # 14-16 parent joint axis
        self.joints = np.empty((self.num_links-1, 2) ,dtype=int) # dim0 is joint number
                # 0 parent link, 1 child link
        
        # Root link (absolute coords)
        self.links[0,0:8] = [0, 0, self.root_height, self.max_len, 1, 1, 1, -1]
        
        # Add links until there are enough
        for i in range(1, self.num_links):
            self.Add_A_Link(i)
            
        # decide which links will have sensors
        self.links[:,4] = np.random.choice([0,1], self.links.shape[0], 
                                           p=[1-self.sensor_prob, self.sensor_prob])
        self.links[0,4] = 1 # guarantee at least one sensor
        
        # calculate number of neurons
        self.numSensorNeurons = int(np.sum(self.links[:,4]))
        self.numMotorNeurons = self.num_links - 1
        
    def Add_A_Link(self, i):
        link_added = False
        collision_counter = [0,0]
        failed_attempts = 0
        while not link_added:
            if sum(collision_counter) > 200:
                self.wiggle_room *= 0.9 # reduce wiggle room
                collision_counter = [0,0] # reset collision counter
                failed_attempts += 1
            if failed_attempts > 10:
                print("Resetting eligibilities, ignoring child/layer limits")
                self.links[:,5] = 1 # reset eligibilities, ignoring rules from constructor
                
            # propose a random parent from eligible parents, 7
            eligible_parents = np.squeeze(np.argwhere(self.links[:,5]), axis=1)
            parent = np.random.choice(eligible_parents)
            
            # propose a joint direction, 11 12 13
            seed = np.random.normal(size=3)
            norm = np.linalg.norm(seed)
            if norm == 0: seed[0] = 1 # avoid divide by zero, even though will never happen
            direction = seed/norm 
            
            # propose a link diameter, 3
            d = self.min_len + (self.max_len - self.min_len) * np.random.rand()
            
            # calculate link location, 0 1 2
            center = self.links[parent,0:3] + 0.5*self.connect_factor*(self.links[parent,3]+d)*direction
            
            # if floor collision, try again
            if center[2] <= 0.5*d:
                collision_counter[0] += 1
                if c.printCollision:
                    print(f"{collision_counter[0]} floor collision")
                continue
            
            # if self collision, try again
            if i > 1:
                links_to_check = np.delete(self.links[0:i,0:4],parent,0)
                vecd = center - links_to_check[:,0:3]
                distance = np.linalg.norm(vecd, axis=1)
                sum_radii = 0.5 * (links_to_check[:,3] + d) + self.wiggle_room
                if min(distance-sum_radii) <= 0:
                    collision_counter[1] += 1
                    if c.printCollision:
                        print(f"{collision_counter[1]} link collision")
                    continue
                
            # generate random joint axis
            seed = np.random.normal(size=3)
            norm = np.linalg.norm(seed)
            if norm == 0: seed[0] = 1 # avoid divide by zero, even though will never happen
            axis = seed/norm 
            
            # constrains axis to plane perpendicular to joint direction
            # axis = axis - np.dot(axis, direction)*direction 
            
            # overwrites joint axis to be same as joint direction
            # axis = direction
            
            # store link and joint information
            self.links[i,0:3] = center # x, y, z
            self.links[i,3] = d # diameter
            self.links[i,5] = 1 # eligibility
            self.links[i,6] = self.links[parent,6] + 1 # layer number
            self.links[i,7] = parent # parent link number
            self.links[i,8:11] = self.links[parent,0:3] + 0.5*self.links[parent,3]*direction # parent joint location
            self.links[i,11:14] = direction # parent joint direction
            self.links[i,14:] = axis
            
            self.joints[i-1,0] = parent
            self.joints[i-1,1] = i
            
            # update eligibility of parent and child
            num_children = (self.joints[:,0] == parent).sum() # counts children of parent
            if num_children >= self.children_lim:
                self.links[parent,5] = 0
            if self.links[i,6] >= self.layer_lim:
                self.links[i,5] = 0
                
            # terminate loop
            link_added = True 
            
    def Recalculate_Body(self, temp_links):
        for i in range(1, self.num_links):
            parent = int(temp_links[i,7]) # parent link number
            direction = temp_links[i,11:14] # parent joint direction
            d = temp_links[i,3] # link diameter
            
            # recalculate link absolute location info
            temp_links[i,0:3] = temp_links[parent,0:3] + 0.5*self.connect_factor*(temp_links[parent,3]+d)*direction # center
            temp_links[i,8:11] = temp_links[parent,0:3] + 0.5*temp_links[parent,3]*direction # parent joint location
        return temp_links
    
    def Check_Collisions(self, temp_links):
        for i in range(0, self.num_links):
            # floor collision
            if temp_links[i,2] <= 0.5*temp_links[i,3]:
                return True # collision
            
            # self collision
            if i > 1:
                parent = int(temp_links[i,7])
                center = temp_links[i,0:3]
                d = temp_links[i,3]
                links_to_check = np.delete(self.links[0:i,0:4],parent,0)
                vecd = center - links_to_check[:,0:3]
                distance = np.linalg.norm(vecd, axis=1)
                sum_radii = 0.5 * (links_to_check[:,3] + d) + self.wiggle_room
                if min(distance-sum_radii) <= 0:
                    return True # collision
                
        return False # no collisions
            
    def Create_Body(self):
        
        pyrosim.Start_URDF(f"temp\\body{self.myID}.urdf")
        
        # create root link
        link_loc = (self.links[0,0:3]).tolist()
        diameter = self.links[0,3]
        colorname = 'green' if self.links[0,4] == 1 else 'blue'
        pyrosim.Send_Cube(name="0", pos=link_loc, size=diameter, color=colorname, shape=2)
        
        # create other links and joints
        for i in range(1, self.num_links):
            
            parent = int(self.links[i,7])
            
            link_loc = (0.5*self.connect_factor*self.links[i,3]*self.links[i,11:14]).tolist()
            diameter = self.links[i,3]
            colorname = 'green' if self.links[i,4] == 1 else 'blue'
            
            joint_axis = np.array2string(self.links[i,14:], separator=' ')[2:-1]
            joint_loc = (self.links[i,8:11] - self.links[parent,8:11]).tolist() 
                # subtracts zero if parent is root anyway, so absolute vs. relative is inconsequential
                
            pyrosim.Send_Joint(name = f"{parent}_{i}", parent= f"{parent}", child = f"{i}", type = "revolute", 
                               position = joint_loc, jointAxis = joint_axis)
            
            pyrosim.Send_Cube(name=f"{i}", pos=link_loc, size=diameter, color=colorname, shape=2)
        
        pyrosim.End()
        
        while not os.path.exists(f"temp\\body{self.myID}.urdf"):
            time.sleep(0.001)
        
    def Create_Brain(self):
        
        pyrosim.Start_NeuralNetwork(f"temp\\brain{self.myID}.nndf")
        n_num = 0
        
        for i in range(self.num_links):
            if self.links[i,4] == 1:
                pyrosim.Send_Sensor_Neuron(name = n_num , linkName = f"{i}"); n_num += 1
                      
        for i in range(self.num_links - 1):
            pyrosim.Send_Motor_Neuron(name = n_num , jointName = f"{self.joints[i,0]}_{self.joints[i,1]}"); n_num += 1
            
        for currentRow in range(0,self.numSensorNeurons):
            for currentColumn in range(0,self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , 
                                    targetNeuronName = currentColumn + self.numSensorNeurons, 
                                    weight = self.weights[currentRow, currentColumn])
        pyrosim.End()
        
        while not os.path.exists(f"temp\\brain{self.myID}.nndf"):
            time.sleep(0.001)
        
    def Mutate(self):
        # mutation_type = np.random.randint(0,9)
        
        #                 N  SS  SM  ARS  CJA  AL  CD  CJD  RL
        probs = np.array([1, 1,  1,  1,   3,   3,  2,  0,   3])
        probs = np.array([1, 1,  1,  1,   4,   3,  1,  0,   2])
        probs = np.array([1, 1,  1,  1,   2,   2,  2,  3,   2])
        
        probs = probs / probs.sum()
        mutation_type = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8], p=probs)
        mutation_type = 7
        
        # EASY TO IMPLEMENT
        # single brain weight (of NN)
        if mutation_type == 0: 
            randomRow = np.random.randint(0,self.numSensorNeurons)
            randomColumn = np.random.randint(0,self.numMotorNeurons)
            self.weights[randomRow,randomColumn] = np.random.random() * 2 - 1
        # swap sensors
        elif mutation_type == 1: 
            A = np.random.randint(0,self.numSensorNeurons)
            B = np.random.randint(0,self.numSensorNeurons)
            temp = self.weights[A,:]
            self.weights[A,:] = self.weights[B,:]
            self.weights[B,:] = temp
        # swap motors
        elif mutation_type == 2: 
            A = np.random.randint(0,self.numMotorNeurons)
            B = np.random.randint(0,self.numMotorNeurons)
            temp = self.weights[:,A]
            self.weights[:,A] = self.weights[:,B]
            self.weights[:,B] = temp
        # add or remove sensor
        elif mutation_type == 3: 
            link = np.random.randint(0,self.num_links)
            brain_idx = int(self.links[0:link,4].sum())
            if self.links[link,4] == 1 and self.links[:,4].sum() > 1: # remove sensor
                self.links[link,4] = 0
                np.delete(self.weights, brain_idx, axis=0)
            else: # add sensor
                self.links[link,4] = 1
                self.weights = np.insert(self.weights, brain_idx, np.random.random((1,self.numMotorNeurons))*2-1, axis=0)
        # change joint axis
        elif mutation_type == 4:
            seed = np.random.normal(size=3)
            norm = np.linalg.norm(seed)
            if norm == 0: seed[0] = 1 # avoid divide by zero, even though will never happen
            axis = seed/norm 
            joint = np.random.randint(1,self.num_links)
            self.links[joint,14:] = axis
            
        # DIFFICULT TO IMPLEMENT WELL
        # add a link
        elif mutation_type == 5 and self.num_links < self.num_link_max:
            self.num_links += 1
            self.links = np.append(self.links, np.zeros((1,17)), axis=0)
            self.joints = np.append(self.joints, np.zeros((1,2),dtype=int), axis=0)
            self.Add_A_Link(self.num_links-1)
            self.links[self.num_links-1,4] = np.random.choice([0,1], p=[1-self.sensor_prob, self.sensor_prob]) # sensor?
            # add motor to brain
            self.weights = np.append(self.weights, np.random.random((self.weights.shape[0],1))*2-1, axis=1)
            self.numMotorNeurons = self.num_links - 1
            # add sensor to brain
            if self.links[self.num_links-1,4] == 1:
                self.weights = np.append(self.weights, np.random.random((1,self.numMotorNeurons))*2-1, axis=0)
            self.numSensorNeurons = int(np.sum(self.links[:,4]))
            
        # QUICK BUT JANKY IMPLEMENTATIONS... TO BE FIXED
        # change diameter
        elif mutation_type == 6:
            for i in range(100): # attempt to find a valid diameter, if not give up
                link = np.random.randint(0,self.num_links)
                temp_links = copy.deepcopy(self.links)
                
                temp_links[link,3] *= np.random.random() * 2 + 0.3
                
                temp_links = self.Recalculate_Body(temp_links)
                collision = self.Check_Collisions(temp_links)
                if not collision:
                    self.links = temp_links
                    break
                
        # change joint direction
        elif mutation_type == 7:
            for i in range(100): # attempt to find a valid direction, if not give up
                joint = np.random.randint(1,self.num_links)
                temp_links = copy.deepcopy(self.links)
                
                seed = np.random.normal(size=3)
                norm = np.linalg.norm(seed)
                if norm == 0: seed[0] = 1 # avoid divide by zero, even though will never happen
                axis = seed/norm 
                temp_links[joint,11:14] = axis
                
                temp_links = self.Recalculate_Body(temp_links)
                collision = self.Check_Collisions(temp_links)
                
                if not collision:
                    self.links = temp_links
                    break
        
        # remove a link (leaf link)
        elif mutation_type == 8 and self.num_links > self.num_link_min:
            leaf_links = np.setdiff1d(self.joints[:,1], self.joints[:,0])
            link = np.random.choice(leaf_links)
            
            if self.links[link,4] == 1:
                brain_idx = int(self.links[0:link,4].sum())
                self.weights = np.delete(self.weights, brain_idx, axis=0)
                self.numSensorNeurons -= 1   
                
            self.num_links -= 1
            self.numMotorNeurons = self.num_links - 1
            
            self.joints = np.where(self.joints > link, self.joints-1, self.joints)
            self.links[:,7] = np.where(self.links[:,7] > link, self.links[:,7]-1, self.links[:,7])
            
            self.links = np.delete(self.links, link, axis=0)
            self.weights = np.delete(self.weights, link-1, axis=1)
            self.joints = np.delete(self.joints, link-1, axis=0)
            
            # self.num_links = self.links.shape[0]
            # self.numSensorNeurons = self.weights.shape[0]
            # self.numMotorNeurons = self.weights.shape[1]
        
        # remove a link (and lineage)

    def Set_ID(self, ID):
        self.myID = ID
        
    def Show_Simulation(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"start /B python simulate.py GUI {self.myID} > nul")
        # os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")