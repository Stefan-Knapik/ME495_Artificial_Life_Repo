from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color=None):

        self.depth  = 3
        
        if color == "blue":
            self.string1 = '<material name="Blue">'
            self.string2 = '    <color rgba="0 0 1.0 1.0"/>'
        elif color == "green":
            self.string1 = '<material name="Green">'
            self.string2 = '    <color rgba="0 1.0 0 1.0"/>'
        elif color == "red":
            self.string1 = '<material name="Red">'
            self.string2 = '    <color rgba="1.0 0 0 1.0"/>'
        else:
            self.string1 = '<material name="Cyan">'
            self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
