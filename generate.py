import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

pyrosim.Start_SDF("boxes.sdf")

for i in range(10):
    pyrosim.Send_Cube(name="Box", pos=[x, y, i*height+z] , size=[length, width, height])


pyrosim.End()