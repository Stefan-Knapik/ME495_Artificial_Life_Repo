from world import WORLD
from robot import ROBOT
import constants as c
import time
import pybullet as p
import pybullet_data

class SIMULATION:

    def __init__(self):
        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)
        
        self.world = WORLD()
        self.robot = ROBOT()
        
    def Run(self):
        for i in range(c.num_steps):
            p.stepSimulation()
            
            self.robot.Sense(i)
            self.robot.Act(i)
            

            print(i)
            time.sleep(c.wait_time)
            
        for linkName in self.robot.sensors:
            self.robot.sensors[linkName].Save_Values()
            
        for jointName in self.robot.motors:
            self.robot.motors[jointName].Save_Values()
            
    def __del__(self):
        p.disconnect()
                