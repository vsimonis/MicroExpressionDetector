from ActiveShapeModels import ASM, Point, Shape
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import os
def drawScaleSegment( axis, shape ):
    axis.plot( [shape.shapePoints[0].x, shape.shapePoints[1].x],          # plot p0 to p1 segment
              [shape.shapePoints[0].y, shape.shapePoints[1].y],
              color= 'r', ls = '-')
    
def drawLineUP( axis, shape, cm ):
    axis.plot( [ cm.x, shape.shapePoints[0].x], 
             [ cm.y, shape.shapePoints[0].y], color='b')

def drawShape( axis, shape ):
    shape.draw( sns.xkcd_palette( ["light blue"] ), 0, axis)

def drawCentroid( axis, cm ):
    axis.scatter( cm.x, cm.y, c='r')                     

def plotAll( axis, shape ):
    cm = ASM.centroid( shape )
    drawShape( axis, shape)
    drawCentroid( axis, cm )
    drawLineUP( axis, shape, cm )
    drawScaleSegment( axis, shape )

DIR = "C:\\Users\\Valerie\\Desktop\\stars"
OUTPUT = os.path.join( DIR, "output20")
## 20 point shape
#s1 = Shape( [ Point(857, -129), Point(89,-409), Point(-404,254), Point( 96,957), Point(877,712) ])
files = next(os.walk(OUTPUT))[2]
f = files[0]
with open( os.path.join( OUTPUT, f), "r" ) as infile:
        
    allLines = infile.readlines()
    if len(allLines) > 0:
        cleanLines = [ x.strip().split('\t') for x in allLines]
        ptList = [ Point( x[0], x[1]) for x in cleanLines ]
        s1 = Shape( ptList )

f, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)

## Original shape (input)
cmShape = ASM.centroid( s1 )
plotAll( ax1, s1 ) 

############## Calc transformations ###################
## Translate
t = [[ -cmShape.x ], [ -cmShape.y ]] 
for pt in s1.shapePoints:
    pt.translate( t )
s1.update()
plotAll( ax2, s1)


    
## Scale
d1 = s1.shapePoints[0].dist( s1.shapePoints[1] )
s = float(1)/float(d1)
        
## Rotation
p0 = [ s1.shapePoints[0].x, s1.shapePoints[0].y ]
axisVector = [ 0, 1]
thetaP = ASM.angleV( p0, axisVector )
thetaRot = 2*math.pi - thetaP
rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
        [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]






## What order to calculate and apply the transformations?




for pt in s1.shapePoints:
    pt.rotate( rot )
s1.update()

plotAll( ax3, s1 )

for pt in s1.shapePoints:
    pt.scale( s )
s1.update()
plotAll( ax4, s1)


plt.show()

