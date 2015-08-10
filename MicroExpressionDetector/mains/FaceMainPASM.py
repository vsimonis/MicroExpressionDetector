from ParallelASM import PASM, Point, Shape
import os
from matplotlib import pyplot as plt
import seaborn as sn


#########3


def readIn( asm, files ):
    m = 0
    for f in files:
        if m > 499:
             return        
        with open( os.path.join(folder,f), "r" ) as infile:
            ptList = [ ]
            allLines = infile.readlines()
            pointLine = False
            cleanLines = [ x.strip() for x in allLines]
            for line in cleanLines:
                if line is '{':
                    pointLine = True
                
                elif line is '}':
                    pointLine = False
                    pass
                elif pointLine:
                    ptList.append( map( float, line.split(' ') ) )
                else:
                    pass

        asm.addShape( Shape( ptList ) )
        m += 1
        print m
if __name__ == "__main__":

    DIR = "C:\\Users\\Valerie\\Desktop\\MicroExpress\\facePoints"
    SUBDIR = "session_1"
    folder = os.path.join( DIR, SUBDIR )
    files = next(os.walk(folder))[2]
    asm = PASM( [36,31], 100)
    readIn( asm, files)
    asm.iterateAlignment()
    with open( 'outfile-ASM-100iters-500tr.txt', "w") as output:
            output.write( str(asm.meanShape) )
            output.write( "!!!\n" )
            for shape in asm.allShapes:
                output.write(  str(shape) )
                output.write( "@@@\n" )
            output.write( "!!!\n" )

    
