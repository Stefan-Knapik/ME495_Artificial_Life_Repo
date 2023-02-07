from math import pi

numLinks = 4
numSensorNeurons = numLinks
numMotorNeurons = numLinks - 1

radius = 1 # radius of circumscribed circle
thickness = 1 # thickness of the loop, radial
width = 0.5 # width of the loop, axial

progress_bar = True
printFitness = False

numberOfGenerations = 2
populationSize = 1

num_steps = 1000
sleep_time = 1/240

gravity = -9.8
maxForce = 10
motorJointRange = 0.001

# maxForce = 20
# amplitude = pi/6
# frequency = 13
# phaseOffset = pi/12
