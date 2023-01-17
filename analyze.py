import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

# print(backLegSensorValues)

plt.plot(backLegSensorValues, linewidth=3, label='Back Leg')
plt.plot(frontLegSensorValues, linewidth=1.5, label='Front Leg')
plt.legend()
plt.xlabel('Time Steps')
plt.ylabel('Books Read')

plt.show()


