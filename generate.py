import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 2

pyrosim.Start_SDF("box.sdf")
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[length, width, height])

pyrosim.End()