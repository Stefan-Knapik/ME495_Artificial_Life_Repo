from math import pi

numLinks = 6
numSensorNeurons = numLinks
numMotorNeurons = numLinks - 1

radius = 1 # radius of circumscribed circle
thickness = 0.1 # thickness of the loop, radial
width = 1 # width of the loop, axial

progress_bar = True
printFitness = 1

numberOfGenerations = 100
populationSize = 10

num_steps = 200
sleep_time = 1/240

gravity = -9.8
maxForce = 100
motorJointRange = 1

# maxForce = 20
# amplitude = pi/6
# frequency = 13
# phaseOffset = pi/12
