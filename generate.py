import pyrosim.pyrosim as pyrosim

length = 1
width = 2
height = 3

x = 0
y = 0
z = height/2

pyrosim.Start_SDF("box.sdf")
pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, width, height])

pyrosim.End()