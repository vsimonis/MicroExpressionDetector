import sys
sys.path.append( ".." )

from helpers.FileHelper import FileHelper
from helpers.DrawFace import DrawFace
from image_processing.TemplateMatcher import TemplateMatcher
from shapes.Point import Point
from shapes.Vector import Vector
from shapes.ActiveShape import ActiveShape
from active_shape_models.ShapeAligner import ShapeAligner 
from active_shape_models.PointMovementCalculator import PointMovementCalculator as pmc
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import copy


class ApplyASM(object):

    def __init__( self, asm, nIters, nTrain, out, img, method, maxPx, filterSize, filterPoints ):
        self.img  = img#FileHelper( nIters, nTrain, out).readInImage( )
        self.out = out
        self.asm = asm

        self.method = method
        self.maxPx = maxPx
        self.fSize = filterSize
        
        self.fPts = filterPoints

        self.nVals = asm.n *2
        self.P = self.asm.evecs[ :, 0 : self.nVals ]
        self.b =  np.zeros( self.nVals )#self.asm.evals
        #self.Wb = np.diag( map( math.sqrt, self.asm.evals[ 0 : self.nVals ] ) )
        self.db = np.zeros( self.nVals ) 
        self.d0 = 0
        self.ds = 0
        self.dXc = np.zeros( self.asm.n )
        


    ### DYNAMIC PROPERTIES
    @property 
    def x( self ):
        pcaMat = np.dot( self.P, self.b)   
        pts = np.add( self.asm.meanShape.flatten(), pcaMat ) 
        return pts

    @property 
    def y( self ):
        shape = ActiveShape.createShape( self.x )
        shape = shape.M( self.s, self.theta )
        pts = np.add( shape.flatten(), self.dX )
        pts = np.subtract( pts, self.dXc   )
        return pts



    def genXc( self, pDict ) :        
        xc = np.ones( self.asm.n ) * pDict['t'][0][0]
        yc = np.ones( self.asm.n ) * pDict['t'][1][0]
        return np.ravel( zip( xc, yc ) )




    ### For initial setup of model
    def alignEyes( self, eye1, eye2 ):

        
        x = ActiveShape.createShape( self.x ) 
        f, [[ax1, ax2], [ax3, ax4]] = plt.subplots( 2,2)
        # distance between eyes:
        d1 = Point.dist( eye1, eye2 )
        rc = ActiveShape.centroid( ActiveShape( x.shapePoints[ 31 : 35 ]  )   )
        lc = ActiveShape.centroid( ActiveShape( x.shapePoints[ 27 : 31 ] ) )
           

        if self.asm.n == 68:
            d2 = Point.dist( x.shapePoints[ self.asm.rightEyeIx], x.shapePoints[self.asm.leftEyeIx] )
        else :
            d2 = Point.dist( rc, lc )
        s = float( d1/d2 ) 


        shape = copy.deepcopy( x )

        DrawFace( shape, ax1).drawBold()

        shape = shape.scale( s ) 
        DrawFace( shape, ax2).drawBold()

        rot, thetaRot = self.asm.calcNormRotateImg( shape )
        shape = shape.rotate( rot )
        DrawFace( shape, ax3).drawBold()

        ax1.invert_yaxis()
        ax2.invert_yaxis()
        ax3.invert_yaxis()
       
        rc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 31 : 35 ]  )   )
        lc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 27 : 31 ] ) )
       

        if self.asm.n == 68:
            t = [ [ (eye2.x - shape.shapePoints[self.asm.leftEyeIx ].x )  ], 
                 [ (eye2.y - shape.shapePoints[self.asm.leftEyeIx ].y )]  ]
        else:
            t = [ [ ( eye2.x - rc.x )], [ (  eye2.y - rc.y )] ]
        shape = shape.translate( t )

        ### Check that initial shape is within image frame
        tempS = 0
        nr, nc = np.shape( self.img )
        for pt in shape.shapePoints:
            if pt.y > nr : 
#                print "y big"
                tempS += ( pt.y - nr + 10 ) / nr
            if pt.x > nc :
#                print "x big"
                tempS += ( pt.x - nc + 10) / nc

        if tempS != 0:        
            shape = shape.scale( 1 - tempS )
        
            if self.asm.n == 68:
                t = [ [ (eye2.x - shape.shapePoints[self.asm.leftEyeIx ].x )  ], 
                        [ (eye2.y - shape.shapePoints[self.asm.leftEyeIx ].y )]  ]
            else:
                rc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 31 : 35 ]  )   )
                lc = ActiveShape.centroid( ActiveShape( shape.shapePoints[ 27 : 31 ] ) )

                t = [ [ ( eye2.x - rc.x )], [ (  eye2.y - rc.y )] ]
            shape = shape.translate( t )


            #print "row: %d\tcol:%d" % ( pt.y, pt.x )
#            print np.shape(self.img )   

        DrawFace( shape, ax4).drawBold()
        ax4.scatter( eye1.x, eye1.y, c = 'r') 
        ax4.scatter( eye2.x, eye2.y, c = 'g' )
        ax4.imshow( self.img, cmap = 'gray' ) 
        f.show()
        plt.savefig( os.path.join( self.out, "deform-init.png" ) )
        plt.gca().invert_yaxis()
        plt.close()
        srot = np.dot(s, rot )
        transDict = { 't' : t, 's' : s, 'rot' : rot,'srot' : srot, 'theta' : thetaRot }
        

        return shape, transDict

    def findEyes( self ):
        eye_cascade = cv2.CascadeClassifier('C:\\OpenCV\\data\\haarcascades\\haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale( self.img )
        im_toshow = copy.deepcopy( self.img )
        eyeArr = []
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(im_toshow,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            eyeArr.append( ( ex, ey, ew, eh ) )

        # filter by area
        eyeAreas = map( self.areaRect, eyeArr )
        ix = np.argmax( eyeAreas )
        eye1 = eyeArr[ix]
    
        eyeAreas.pop( ix )
        eyeArr.pop(ix )

        ix = np.argmax( eyeAreas )
        eye2 = eyeArr[ix]

        ex1, ey1, ew1, eh1 = eye1
        eye1loc = Point( ex1 + ew1/2,ey1+ eh1/2)

        ex2, ey2, ew2, eh2 = eye2
        eye2loc = Point( ex2 + ew2/2,ey2+ eh2/2)

       # cv2.circle( self.img, ( int(eye1loc.x), int(eye1loc.y) ), 1, (255,0,0) )
       # cv2.circle( self.img, ( int(eye2loc.x), int(eye2loc.y) ), 1, (255,0,0) )
        #showImg( im_toshow ) 
        return eye1loc, eye2loc         
    
    @staticmethod
    def areaRect( tup ):
        return tup[2] * tup[3]

    def initialPosition( self ):
        ##### SETUP 
        eye1, eye2 = self.findEyes( )
        
        ### Align eyes needs to return model in the image coordinate frame !!!!
        model, transdict = self.alignEyes( eye1, eye2 )

        return model, transdict


    def calcdX( self ):
        print "calcDX"
#        print "CurrentShape as points"
#        print self.X

#        print "CurrentShape as ActiveShape"
        Xshape = ActiveShape.createShape( self.X ) 
 #       for p in Xshape.shapePoints:
 #           print p.x, p.y
         
        #for pt in Xshape.shapePoints:
        #    print pt.x, pt.y
        if self.method == "grad":
            PMC = pmc( self.img, self.maxPx )
            return np.ravel( map( lambda p : PMC.calcShift( p, 'tx' ), Xshape.shapePoints ) )
        else:
            TM = TemplateMatcher( self.method , self.fSize, self.fPts )
        return np.ravel( TM.performMatching(self.img, Xshape) )

    def applyASM( self ): ## Main
        SA = ShapeAligner( self.asm, 0, self.out )
                                  
        XShape, _ = self.initialPosition()

        xShape = ActiveShape.createShape( self.x )

        modelParams = SA.calcAlignTransBtwn( XShape, xShape , np.ones( self.asm.n) )
#        print "params after init"
#        print modelParams
        #modelParams = SA.calcAlignTransBtwn(  XShape , xShape , np.ones( self.asm.n ) ) 
        self.s = modelParams[ 's' ]

        self.theta = modelParams[ 'theta']

        self.Xc = self.genXc( modelParams ) 

        self.X =  np.add( xShape.M( self.s, self.theta ).flatten(), self.Xc)
        
#        print "Initial Current shape"
#        print self.X


        i = 0
        
        while np.mean( self.calcdX() ) > 0.000001 and i < 150: 
            print i

            f, (ax1, ax2) = plt.subplots( 1,2 ) #, sharex = True, sharey = True )
            
            xShape = ActiveShape.createShape( self.x )
            self.X =  np.add( xShape.M( self.s, self.theta ).flatten(), self.Xc)

            # Calculate point shifts
            self.dX =  self.calcdX()
#            "dX result"
            #print self.dX
                   
            ## X + dX
            self.XdX =  np.add( self.X , self.dX ) 
            
            ax1.imshow(  self.img )
            DrawFace( self.X, ax1).drawContrast()

            DrawFace( self.XdX, ax1).drawBold()

            DrawFace( self.X, ax2).drawContrast()
            DrawFace( self.XdX, ax2 ).drawBold()
            ax1.set_xlim( 0, np.shape( self.img )[1])
            ax1.set_ylim( np.shape( self.img)[0] ,0 )
            ax2.invert_yaxis()
            f.suptitle("Original Shape (Contrast) and Gradient Suggested Shape (Bold)")
            f.savefig( os.path.join( self.out, "deformation-iter-%d.png" % i ) )

                 
            ## Find X --> X + dX    
            XShape = ActiveShape.createShape( self.X )
            XdXShape = ActiveShape.createShape( self.XdX )
            deltaParams = SA.calcAlignTransBtwn( XdXShape, XShape, np.ones( self.asm.n ) )
        
            ## Get transformation constrained delta parameters
            self.d0 = deltaParams['theta']
            self.ds = deltaParams['s']
            self.dXc = self.genXc( deltaParams ) 
        
            ## Calculate dx                            
            yShape = ActiveShape.createShape( self.y ) 
            f, (ax1,ax2) = plt.subplots( 1,2) 
            yt = yShape.M( 1 / ( self.s *( 1 + self.ds ))  , - ( self.theta + self.d0 ) )
            
            DrawFace( yShape, ax1).drawBold()
            DrawFace( yt, ax2).drawBold()

            f.suptitle( "Transformed contour" )
            ax1.set_title( "Original")
            ax2.set_title( "Delta'd") 
            ax1.invert_yaxis()            
            ax2.invert_yaxis()
            f.savefig( os.path.join( self.out, "y-%d.png" % i )   )
            plt.close()

            
            self.dx = np.subtract( yt.flatten(), self.x ) 

            ## Calculate db 
            self.db = np.dot( np.transpose(self.P) , self.dx )

            
            ## Update
            self.theta += self.d0
            self.s = self.s * ( 1 + self.ds )
            self.Xc = np.add( self.Xc, self.dXc )

            self.b = np.add( self.b,  self.db ) 

            f.clear()
            plt.close()
            
            i += 1
        print "It took you %d iterations" % i

        




