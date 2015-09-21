from ParallelASM import PASM, Shape, Point
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab as plb

import copy
import matplotlib.cm as cm
from FaceDraw import FaceDraw
import math 

class DASM( PASM):
    def __init__( self, pasm ):
        self.pasm = pasm
        self.PCA()

        self.__dict__.update( pasm.__dict__ )
        pasm.normShape( self.meanShape )
        
        self.model = self.meanShape
        self.modelParams = { 'rot' : [[1,0],[0,1]] , 't' : [[0],[0]] }

    @property
    def appModel( self ):
        shape = copy.deepcopy( self.model )
        shape = shape.transform( self.modelParams )
        return shape


    def alignAllShapes(self):
        self.calcWs()
        return super(DASM, self).alignAllShapes()

    def calcWs( self ):
        self.w = np.ones( self.n )
        #self.w = [ 1 for j in s]
        self.W = np.diag(self.w)
        ##print "calcWs: %f" % (time.time() - start)
    
    def pointGradient( self ):
        fx = [ -1, 0,1 ]
        fy = np.transpose(fx)

        
    def PCA( self ):
        self.pasm.calcMeanShape()
        map( lambda x : x.calcDiff( self.pasm.meanShape ), self.pasm.allShapes )
        cov = map( lambda x : x.calcSingleCov(), self.pasm.allShapes )
        S = sum( cov ) 

        self.eVals, vecs = np.linalg.eig( S )
        self.eVecs = np.array( vecs )
        
    def alignEyes( self, eye1, eye2, img ):
        # distance between eyes:
        d = eye1.dist( eye2 )
        self.meanShape.scale( d )
          
        rightEyeIx = 36
        leftEyeIx = 31


        
        ## Rotation
        xDiff = self.meanShape.shapePoints[rightEyeIx].x - self.meanShape.shapePoints[leftEyeIx].x
        yDiff = self.meanShape.shapePoints[rightEyeIx].y - self.meanShape.shapePoints[leftEyeIx].y
    
        p0 = [ xDiff, yDiff ] #self.meanShape.shapePoints[0].x, self.meanShape.shapePoints[0].y ]
        axisVector = [ 1, 0]
        thetaP = PASM.angleV( p0, axisVector )
        thetaRot = thetaP
    
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
                [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        self.meanShape.rotate( rot )

        t = [ [eye2.x - self.meanShape.shapePoints[ rightEyeIx].x ],
        [eye2.y - self.meanShape.shapePoints[rightEyeIx].y ] ]


        self.meanShape.translate( t )

        self.transDict = {} #DANGER!!!!!!!
        self.transDict.update( {'rot' : rot , 't' : t })


          
    @staticmethod      
    def getGradient( pt, img ):
        if pt.x is np.nan or pt.y is np.nan:
            return
        ## Check bounds
        h, w = np.shape( img )
        if pt.y > h or pt.y > h-1 :
            pt.setY( h - 2)
        if pt.x > w or pt.x > w-1 :
            pt.setX( w - 2) 

        delF = [ (img[ pt.y, pt.x + 1] - img[pt.y, pt.x - 1 ] )/2,
                (img[ pt.y + 1 , pt.x] - img[pt.y - 1, pt.x ] )/2 ] 
        #print delF
        mag = math.sqrt( delF[0] ** 2 + delF[1] ** 2 )
        #dir = PASM.angleV( delF, [ 0, 0] )
        unitF = PASM.unitV( delF )
        
        return unitF, mag
    
    def adjust( self, img ):
        self.dX = np.ravel( map( lambda x : DASM.getGradient( x, img ), self.meanShape.shapePoints ) )
        nX = np.add( self.meanShape.allPts, self.dX )
        
        x,y = DASM.deravel( nX )
        ms = Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])
        self.transDict = self.alignOneShape( ms, self.appModel )

        #nX = np.add( dasm.meanShape.allPts, np.dot( dasm.eVals, dasm.db ) )
        #x,y = DASM.deravel( nX )
        #ms = Shape( [ Point (pt[0], pt[1] ) for pt in zip(x,y) ])

        #self.db = np.dot( np.transpose( self.eVecs ), np.ravel( self.dX ) )
    
    @staticmethod
    def deravel( vect ):
        x, y = [], []
        vect = np.ravel( vect ) 
        for i in range( len( vect ) ):
            if i % 2 == 0:
                x.append( vect[i] )
            else: 
                y.append( vect[i] )
        return x, y
           
