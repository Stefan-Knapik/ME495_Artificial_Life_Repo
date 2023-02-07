from math import pi

# Visualisation
progress_bar = 1
printFitness = 0

# Body 
numLinks = 12 # number of links in the body
radius = 1 # radius of circumscribed circle
thickness = 0.1 # thickness of the hoop, radial
width = 1 # width of the hoop, axial

# Optimization 
numberOfGenerations = 200
populationSize = 20
# Reproduction
randomPercentage = 0.1 # proportion of random children
bredPercentage = 0.4 # proportion of bred children

# Simulation settings
num_steps = 2000
sleep_time = 1/240
gravity = -9.8

# Control 
maxForce = 100
motorJointRange = 0.2
numSensorNeurons = numLinks
numMotorNeurons = numLinks - 1