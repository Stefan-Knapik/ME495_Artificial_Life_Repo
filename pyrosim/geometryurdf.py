from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_URDF: 

    def __init__(self,size,shape=0):

        self.depth   = 3

        self.string1 = '<geometry>'
        
        if shape == 0:
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            self.string2 = '    <box size="' + sizeString + '" />'
        else:
            sizeString = 'length="' + str(size[0]) + '" radius="' + str(0.5 * size[1]) + '"'
            self.string2 = '    <cylinder ' + sizeString + ' />'
            

        self.string3 = '</geometry>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
