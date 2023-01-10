import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

pyrosim.Start_SDF("boxes.sdf")

for y in range(-2,3):
    for x in range(-2,3):
        for i in range(10):
            scale = 0.9**i
            pyrosim.Send_Cube(name="Box", pos=[x, y, i*height+z] , size=[scale*length, scale*width, scale*height])


pyrosim.End()