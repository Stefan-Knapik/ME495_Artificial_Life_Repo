import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

pyrosim.Start_SDF("boxes.sdf")
pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, width, height])
pyrosim.Send_Cube(name="Box2", pos=[x+length, y, z+height] , size=[length, width, height])

pyrosim.End()