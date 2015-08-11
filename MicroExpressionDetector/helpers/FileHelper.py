from shapes.ActiveShape import ActiveShape
import os

class FileHelper( object ):
    """description of class"""

    def __init__( self, nTrain, out ):
        direc = "C:\\Users\\Valerie\\Desktop\\MicroExpress\\facePoints"
        subdir = "session_1"
        self.pointFolder = os.path.join( direc, subdir )
        self.pointFiles = next(os.walk(self.pointFolder))[2]
        self.numTraining = nTrain
        self.output = out

    def writeOutASM( self, asm, nIters, nTrain ):
        with open( os.path.join(self.out, 'outfile-ASM-%diters-%dtr.txt' % (nIters, nTrain) ), "w") as output:
            output.write( str(asm.meanShape) )
            output.write( "!!!\n" )
            for shape in asm.allShapes:
                output.write(  str(shape) )
                output.write( "@@@\n" )
            output.write( "!!!\n" )

    def readInPoints( self, asm ):
        m = 0

        for f in self.pointFiles :
            m += 1
            with open( os.path.join(self.pointFolder,f), "r" ) as infile:
                ptList = [ ]
                allLines = infile.readlines()
                pointLine = False
                cleanLines = [ x.strip() for x in allLines]
                for line in cleanLines:
                    if line is '{':
                        pointLine = True
                    elif line is '}':
                        pointLine = False
                    elif pointLine:
                        ptList.append( map( float, line.split(' ') ) )
                    else:
                        pass
                asm.addShape( ActiveShape( ptList ) )
            if m > self.numTraining:
                return asm



