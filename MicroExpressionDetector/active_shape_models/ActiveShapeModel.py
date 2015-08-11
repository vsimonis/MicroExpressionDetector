from shapes.Shape import Shape
from shapes.Point import Point
from shapes.ActiveShape import ActiveShape
from shapes.Vector import Vector
import numpy as np
import math


class ActiveShapeModel( object ):


    def __init__( self, refIndices ):
        self.allShapes = []
        self.n = 0 #number of points in shape
        self.refIxs = refIndices     
        
    @property    
    def I( self ):
        """ 
        Returns the number of ASM training shapes
        """
        return len( self.allShapes )

    def addShape( self, s ):
        """
        Adds a training shape to the ASM
        Checks that the number of points in ASM of 
        added shape is same as number of points in other ASM shapes
        """
        if len( self.allShapes ) == 0:
            self.allShapes.append( s )
            self.n = s.n
        else:
            assert( s.n == self.n )
            self.allShapes.append( s )

  
    def drawAllShapes( self, pallette, axis):
        i = 0
        for el in self.allShapes:
            el.draw( palette, i, axis)
            i += 1
        axis.plot( self.meanShape.xs, self.meanShape.ys, c = 'k' )

    
    def calcMeanShape( self ):
        xList = [ el.xs for el in self.allShapes ]
        yList = [ el.ys for el in self.allShapes ]
        meanPointsList = map( lambda x,y: Vector( x, y), np.mean(xList, 0), np.mean(yList, 0) )
#        meanPointsList = zip( np.mean(xList, 0), np.mean(yList, 0) )
        return ActiveShape( meanPointsList )

    def normShape( self, shape  ):
        """
        Calculates and applies normalization to passed shape
        """

        ############## Calc transformations ###################
        ## Translate centroid as origin
        cm = Shape.centroid( shape )
        t = [[ -cm.x ], [ -cm.y ]] 
        shape.translate( t )

        leftEyeIx = self.refIxs[0]
        rightEyeIx = self.refIxs[1]
    
        ## Scale
        # distance between two "eyes"
        d = Point.dist( shape.shapePoints[leftEyeIx], shape.shapePoints[rightEyeIx] )
        s = float(1)/float(d)
        
        ## Rotation
        # eyes level
        xDiff = shape.shapePoints[rightEyeIx].x - shape.shapePoints[leftEyeIx].x
        yDiff = shape.shapePoints[rightEyeIx].y - shape.shapePoints[leftEyeIx].y
        p0 = [ xDiff, yDiff ] 
        axisVector = [ 1, 0]
        thetaP = Vector.angleBetween( p0, axisVector )
        thetaRot = thetaP
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
                [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        shape = shape.rotate( rot )
        shape = shape.scale( s )

        return shape


