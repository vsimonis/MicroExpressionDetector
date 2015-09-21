from shapes.Shape import Shape
from shapes.Point import Point
from shapes.ActiveShape import ActiveShape
from shapes.Vector import Vector
import numpy as np
import math
import copy

class ActiveShapeModel( object ):


    def __init__( self, refIndices ):
        self.allShapes = []
        self.n = 0 #number of points in shape
        self.leftEyeIx = refIndices[0]
        self.rightEyeIx = refIndices[1] 
        self.modelParams = { 'rot' : [[1,0],[0,1]] , 't' : [[0],[0]] }
        
    @property    
    def I( self ):
        """ 
        Returns the number of ASM training shapes
        """
        return len( self.allShapes )


    @property
    def appModel( self ):
        shape = copy.deepcopy( self.meanShape )
        shape = shape.transform( self.modelParams )
        return shape

    def PCA( self ):
        self.meanShape = self.calcMeanShape()
        cov = map( lambda x : x.calcSingleCov( self.meanShape ), self.allShapes )
        S = sum( cov )

        self.evals, vecs = np.linalg.eig( S )
        self.evecs = np.array( vecs )
        
    
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


    def calcNormTranslate( self, shape):
        ## Translate centroid as origin
        cm = Shape.centroid( shape )
        t = [[ -cm.x ], [ -cm.y ]] 
        return t
            
    def calcNormScale( self, shape ):
        if self.n == 68:
            d = Point.dist( shape.shapePoints[self.leftEyeIx], shape.shapePoints[self.rightEyeIx] )
        else :
            rc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 31 : 35 ]  )   )
            lc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 27 : 31 ] ) )
            d = Point.dist( rc, lc )
        s = float(1)/float(d)
        return s
        
    def calcNormRotateImg( self, shape ):
        xDiff = shape.shapePoints[self.rightEyeIx].x - shape.shapePoints[self.leftEyeIx].x
        yDiff = shape.shapePoints[self.rightEyeIx].y - shape.shapePoints[self.leftEyeIx].y
        p0 = [ xDiff, yDiff ] 
        axisVector = [ -1, 0 ]
        thetaP = Vector.angleBetween( p0, axisVector )
        thetaRot = thetaP
        rot = Vector.calcSRotMat( 1, thetaRot )
        return rot, thetaRot
    
    def calcNormRotate( self, shape ):
        xDiff = shape.shapePoints[self.rightEyeIx].x - shape.shapePoints[self.leftEyeIx].x
        yDiff = shape.shapePoints[self.rightEyeIx].y - shape.shapePoints[self.leftEyeIx].y
        p0 = [ xDiff, yDiff ] 
        axisVector = [ 1, 0 ]
        thetaP = Vector.angleBetween( p0, axisVector )
        thetaRot = thetaP
        rot = Vector.calcSRotMat( 1, thetaRot )
        return rot, thetaRot

    def normShape( self, shape  ):
        """
        Calculates and applies normalization to passed shape
        """

        ############## Calc transformations ###################
        ## Translate centroid as origin
        t = self.calcNormTranslate( shape )
        shape = shape.translate( t )

        ## Scale to distance between eyes as 1
        s = self.calcNormScale( shape )
        
        ## Rotate so eyes are level
        rot, rotTheta = self.calcNormRotateImg( shape )

        shape = shape.rotate( rot )
        shape = shape.scale( s )

        return shape


