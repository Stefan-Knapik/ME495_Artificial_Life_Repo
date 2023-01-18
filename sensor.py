import constants as c
import numpy as np

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName
        self.values = np.zeros(c.num_steps)