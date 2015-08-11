from ActiveShapeModelsBetter import Point, Shape, ASMB
import os
from matplotlib import pyplot as plt
import seaborn as sn

DIR = "C:\\Users\\Valerie\\Desktop\\stars"
OUTPUT = os.path.join( DIR, "output5")

def run():

    files = next(os.walk(OUTPUT))[2]
    asm = ASMB([0,1],100)
    allLines = []
    pts = []
    for f in files:
        with open( os.path.join( OUTPUT, f), "r" ) as infile:
        
            allLines = infile.readlines()
            if len(allLines) > 0:
                cleanLines = [ x.strip().split('\t') for x in allLines]
                ptList = [ Point( x[0], x[1]) for x in cleanLines ]
                asm.addShape( Shape( ptList ) )
    asm.iterateAlignment()


if __name__ == "__main__":
    run()











'''
f, (ax1, ax2) = plt.subplots( 1,2, sharey=True, sharex = True)
cp =sn.color_palette( "BrBG", 10 )
for i in range(asm.I):
    sh = asm.allShapes[i] 
    _ = ax1.scatter( sh.xs, sh.ys, c = cp[i])

asm.alignShapes()
for i in range(asm.I):
    sh = asm.allShapes[i]
    print map( str, sh.shapePoints )
    _ = ax2.scatter( sh.xs, sh.ys, c = cp[i])
plt.show()
'''
