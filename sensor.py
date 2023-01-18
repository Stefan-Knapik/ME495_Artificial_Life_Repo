import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName
        self.values = np.zeros(c.num_steps)
        
    def Get_Value(self, time_step):
        self.values[time_step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        
        if time_step == c.num_steps - 1:
            print(self.values)
            
    def Save_Values(self):
        np.save(f'data/SensorValues_{self.linkName}.npy', self.values)