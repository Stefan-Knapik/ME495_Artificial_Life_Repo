import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

# print(backLegSensorValues)

plt.plot(backLegSensorValues, linewidth=4, label='Back Leg')
plt.plot(frontLegSensorValues, linewidth=2, label='Front Leg')
plt.legend()
plt.xlabel('Time Steps')
plt.ylabel('Touch Sensor Value')
plt.savefig('data\my_plot.png', dpi=500)

plt.show()


