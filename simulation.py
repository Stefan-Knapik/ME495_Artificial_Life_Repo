from world import WORLD
from robot import ROBOT
import constants as c
import time
import pybullet as p
import pybullet_data
from tqdm import tqdm

class SIMULATION:

    def __init__(self, directOrGUI):
        
        if directOrGUI == 'DIRECT': 
            self.physicsClient = p.connect(p.DIRECT)
            self.sleep_time = 0
            self.progress_bar = False
        else: 
            self.physicsClient = p.connect(p.GUI)
            self.sleep_time = c.sleep_time
            self.progress_bar = True
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)
        
        self.world = WORLD()
        self.robot = ROBOT()
        
    def Run(self):
        pbar_sim = tqdm(total = c.num_steps, colour = 'cyan', 
                        desc = 'Simulation Progress', unit = 'steps',
                        disable = not self.progress_bar)
        
        for i in range(c.num_steps):
            p.stepSimulation()
            
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()
            
            time.sleep(self.sleep_time)
            # print(i)
            pbar_sim.update(1)
        pbar_sim.close()
            
        for linkName in self.robot.sensors:
            self.robot.sensors[linkName].Save_Values()
            
        # for jointName in self.robot.motors:
        #     self.robot.motors[jointName].Save_Values()
        
    def GET_FITNESS(self):
        return self.robot.Get_Fitness()
            
    def __del__(self):
        p.disconnect()
                