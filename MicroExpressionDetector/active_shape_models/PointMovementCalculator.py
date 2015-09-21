import sys
sys.path.append( ".." )


import numpy as np
import math
from shapes.Vector import Vector
from shapes.Point import Point
from image_processing.TemplateMatcher import TemplateMatcher


class PointMovementCalculator( object ):
    
    def __init__( self, img, maxPx ):
        self.img = img
        self.maxPx = maxPx
        

    def pointGradient( self ):
        fx = [ -1, 0,1 ]
        fy = np.transpose(fx)


    @staticmethod      
    def getGradient( pt, img ):
        if pt.x is np.nan or pt.y is np.nan:
            return


        ## Check bounds
        h, w = np.shape( img )
        if pt.y > h - 2:
            pt.setY( h - 2)
        if pt.x > w - 2 :


            pt.setX( w - 2) 

        if pt.x < 1 :
            pt.setX( 1) 
        if pt.y < 1 :
            pt.setY( 1) 

        

        delF = [ (img[ pt.y, pt.x + 1] - img[pt.y, pt.x - 1 ] )/2,
                (img[ pt.y + 1 , pt.x] - img[pt.y - 1, pt.x ] )/2 ] 
        #print delF
        mag = math.sqrt( delF[0] ** 2 + delF[1] ** 2 )

        unitF = Vector.unit( delF )                 




        
        return unitF, mag, pt
    
    def calcShift( self, point, method ):
        ## get point p (ix 48)

        # Get initial gradient at point ( unitV already )
        # vector, magnitude, origin
        #print "original: %f, %f" % (point.x, point.y)
        f, m, pt = self.getGradient( point, self.img )  
        #print "returned: %f, %f" % (point.x, point.y)

        h, w = np.shape( self.img )  

        cX = pt.x
        cY = pt.y
        # Goal is to find maximal 
        maxM = 1
        cnt = 0
        while ( True ):
            ## move point according to maximal magnitude response in area
            ## normalized according to current magnitude/maximal magnitude
            dx = f[0] * float(m)/float(maxM)
            dy = f[1]* float(m)/float(maxM)

            ## too far from original point
            if cnt > self.maxPx:
               # print point.x + dx, point.y + dy
                return dx, dy
            cnt+= 1

            ## move point one unit in direction of gradient
            cX = cX + f[0]
            cY = cY + f[1]
            if ( cX > w - 2 or cY > h - 2 or cX < 1 or cY < 1 ) :
               # print point.x + dx, point.y + dy
                return dx, dy

            _, cM, _ = self.getGradient( Point( cX, cY ), self.img )
            if cM > maxM:
                maxM = cM

            ## Outside of image frame

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

    




