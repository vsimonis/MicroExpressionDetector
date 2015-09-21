import os
from ActiveShapeModels import ASM, Point, Shape
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import os


def drawEyeSegment( axis, shape ):
    axis.plot( [shape.shapePoints[33].x, shape.shapePoints[28].x],
              [shape.shapePoints[33].y , shape.shapePoints[28].y],
              color= 'g', ls = '-')
    axis.scatter( [shape.shapePoints[33].x, shape.shapePoints[28].x],
              [shape.shapePoints[33].y , shape.shapePoints[28].y],
              color= 'g')

def drawShape( axis, shape ):
    shape.draw( sns.xkcd_palette( ["light blue"] ), 0, axis)

def drawCentroid( axis, cm ):
    axis.scatter( cm.x, cm.y, c='r')                     

def plotAll( axis, shape ):
    cm = ASM.centroid( shape )
    drawShape( axis, shape)
    drawCentroid( axis, cm )
    drawEyeSegment( axis, shape )

#########3
DIR = "C:\\Users\\Valerie\\Desktop\\MicroExpress\\facePoints"
SUBDIR = "session_1"
folder = os.path.join( DIR, SUBDIR )
files = next(os.walk(folder))[2]

for f in files:
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
    ptList
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

    leftEyeIx = 33
    rightEyeIx = 28
    
    ## Scale
    d1 = s1.shapePoints[leftEyeIx].dist( s1.shapePoints[rightEyeIx] )
    s = float(1)/float(d1)
        
    ## Rotation
    leftEyeIx = 33
    rightEyeIx = 28

    xDiff = s1.shapePoints[rightEyeIx].x - s1.shapePoints[leftEyeIx].x
    yDiff = s1.shapePoints[rightEyeIx].y - s1.shapePoints[leftEyeIx].y
    
    p0 = [ xDiff, yDiff ] #s1.shapePoints[0].x, s1.shapePoints[0].y ]
    axisVector = [ 1, 0]
    thetaP = ASM.angleV( p0, axisVector )
    thetaRot = thetaP
    
    #thetaRot = math.atan2( yDiff, xDiff )

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

    