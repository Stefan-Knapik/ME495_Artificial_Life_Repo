from math import pi

numLinks = 12
numSensorNeurons = numLinks
numMotorNeurons = numLinks - 1

radius = 1 # radius of circumscribed circle
thickness = 0.1 # thickness of the hoop, radial
width = 1 # width of the hoop, axial

progress_bar = 1
printFitness = 0

numberOfGenerations = 200
populationSize = 20
randomPercentage = 0.1
bredPercentage = 0.4

num_steps = 2000
sleep_time = 1/240

gravity = -9.8
maxForce = 100
motorJointRange = 0.2

# maxForce = 20
# amplitude = pi/6
# frequency = 13
# phaseOffset = pi/12
