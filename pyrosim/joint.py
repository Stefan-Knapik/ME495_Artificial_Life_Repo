from pyrosim.commonFunctions import Save_Whitespace

class JOINT: 

    def __init__(self,name,parent,child,type,position,rpy):

        self.name = name

        self.parent = parent

        self.child  = child

        self.type   = type

        self.position = position
        
        self.rpy = rpy

        self.depth = 1

    def Save(self,f,jointAxis):

        Save_Whitespace(self.depth,f)
        f.write('<joint name="' + self.name + '" type="' + self.type + '">' + '\n')

        Save_Whitespace(self.depth,f)
        f.write('   <parent link="' + self.parent + '"/>' + '\n')

        Save_Whitespace(self.depth,f)
        f.write('   <child  link="' + self.child  + '"/>' + '\n')

        Save_Whitespace(self.depth,f)
        originString = str(self.position[0]) + " " + str(self.position[1]) + " " + str(self.position[2])
        rpyString = str(self.rpy[0]) + " " + str(self.rpy[1]) + " " + str(self.rpy[2])
        f.write('   <origin rpy="' + rpyString + '" xyz="' + originString + '" />\n')

        # SCK modified to allow for joint axis to be specified
        Save_Whitespace(self.depth,f)
        # f.write('   <axis xyz="0 1 0"/>\n')
        f.write(' <axis xyz="' + jointAxis + '"/>\n')

        Save_Whitespace(self.depth,f)
        f.write('   <limit effort="0.0" lower="-3.14159" upper="3.14159" velocity="0.0"/>\n')

        Save_Whitespace(self.depth,f)
        f.write('</joint>' + '\n')

