from ParallelASM import PASM, Point, Shape
import os
from matplotlib import pyplot as plt
import seaborn as sn

DIR = "C:\\Users\\Valerie\\Desktop\\stars"
OUTPUT = os.path.join( DIR, "output20")

files = next(os.walk(OUTPUT))[2]

def run():

    asm = PASM([0,1], 1000 )
    allLines = []
    pts = []
    for f in files:
        with open( os.path.join( OUTPUT, f), "r" ) as infile:
        
            allLines = infile.readlines()
            if len(allLines) > 0:
                cleanLines = [ x.strip().split('\t') for x in allLines]
                ptList = [ Point( x[0], x[1]) for x in cleanLines ]
                print len( ptList ) 
                asm.addShape( Shape( ptList ) )



    asm.iterateAlignment()


if __name__ == "__main__":
    run()




