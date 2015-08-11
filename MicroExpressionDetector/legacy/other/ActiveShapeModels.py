import math
import numpy as np
import pandas as pd
from sympy import Matrix, solve_linear_system
from sympy.abc import d, e,f, g
import matplotlib.pyplot as plt
import seaborn as sns
import time

class ASM( object ):
    def __init__( self ):
        self.allShapes = []
        self.n = 0
    
    @property    
    def I( self ):
        return len( self.allShapes )

    def addShape( self, s ):

        if len( self.allShapes ) == 0:
            self.allShapes.append( s )
            self.n = s.n
        else:
            assert( s.n == self.n )
            self.allShapes.append( s )
    
    @property
    def V( self ):
        """
        Variance in distance matrix amongst all shapes
        """
        V = []
        for k in range(self.n):
            row = []
            for l in range(self.n):
                col = []
                for i in range(len( self.allShapes )):
                    col.append( self.allShapes[i].R[k][l])
                row.append( np.var(col) )
            V.append(row)
        return V

    @property 
    def W( self ):
        """ 
        Point weights as diagonal matrix
        """
        
        return np.diag(self.w)

    @property
    def w( self ):
        """
        Point weights as array
        """
        s = map( sum, self.V)
        return [ math.pow( j, -1) for j in s]


    def Zgen( self, shape ):
        return sum( [  self.w[k] * ( shape.xs[k] **2 +
                                    shape.xs[k] **2 )
                     for k in range( self.n ) ] )
    def Xgen( self, shape ):
        return sum( [  self.w[k] * shape.xs[k] 
                     for k in range( self.n ) ] )

    def Ygen( self, shape ):
        return sum( [  self.w[k] * shape.ys[k] 
                     for k in range( self.n ) ] )

    def Wgen( self ):
        return sum( [ self.w[k]  for k in range( self.n ) ] )

    def C1gen( self, shape1, shape2):
        return sum( [ self.w[k] * 
                    ( shape1.xs[k] * shape2.xs[k] +
                    shape1.ys[k] * shape2.ys[k] )
                    for k in range( self.n) ] )
    
    def C2gen( self, shape1, shape2):
        return sum( [ self.w[k] * 
                    ( shape1.ys[k] * shape2.xs[k] +
                    shape1.xs[k] * shape2.ys[k] )
                    for k in range( self.n) ] )


    
      
    def calcMeanShape( self ):
        xList = [ el.xs for el in self.allShapes ]
        yList = [ el.ys for el in self.allShapes ]
        meanPointsList = zip( np.mean(xList, 0), np.mean(yList, 0) )
        self.meanShape = Shape( meanPointsList )
        return

    def iterateAlignment( self ):

        # Setup drawing
        
        f, (ax1,ax2) = plt.subplots(1,2)#, sharex= True, sharey=True)
        colors = ["purple", "light purple", 
                "blue", "cyan", "neon blue",
                "red", "rose",
                "green", "bright green", "mint"]
        pal = sns.xkcd_palette( colors )
        
        iter = 0

        # Draw no change
        self.calcMeanShape()
        self.drawAll( ax1, pal )

        # 1. Align to first shape (instantiation)
        self.alignAllShapes( self.allShapes[0] )

        while( iter < 500 ):
            print iter
            if iter > 0:
                f, (ax1,ax2) = plt.subplots(1,2, sharex= True, sharey=True)
                self.drawAll( ax1, pal ) #previous iter
            ## Calculate mean shape
            self.calcMeanShape( )

            ## Normalize mean shape to first shape
            self.normTrans( self.allShapes[0] )

            ## Realign
            self.alignAllShapes( self.meanShape )
        
            # Draw change
            self.calcMeanShape()
            self.drawAll( ax2, pal )
            plt.legend()
            f.savefig( "C:/Users/Valerie/Desktop/stars/plots5/%d.png" % iter )
            f.clear()
            plt.close()
            iter += 1
        # Show
#        f.show()

   # def isConverged( self ):
    def alignAllShapes( self, shape ):
        start = time.time()
        for el in range( 0, self.I ):
           self.alignOneShape( shape, self.allShapes[ el ] )
        print 'alignAllShapes: %f' % (time.time() - start  )
        return 

    
    def alignOneShape( self, shape1, shape2 ):
        start = time.time()
        transDict = self.calcAlignTrans( shape1, shape2 )
        shape2.applyTrans( transDict )
       
        return

    @staticmethod
    def centroid( shape1 ):
        return Point( np.mean( shape1.xs ) , np.mean( shape1.ys ) )

    @staticmethod
    def unitV( v ): 
        return v / np.linalg.norm( v )

    @staticmethod
    def angleV( v1, v2 ):
        return math.atan2( v1[0], v1[1] ) - math.atan2( v2[0], v2[1] )
        """
        v1_u = ASM.unitV(v1)
        v2_u = ASM.unitV(v2)
        angle = np.arccos(np.dot(v1_u, v2_u))
        if np.isnan(angle):
            if (v1_u == v2_u).all():
                return 0.0
            else:
                return np.pi
        return angle
        """

    def normTrans( self, shape1 ):
#        trans = self.calcNormTrans( shape1 ) 
        trans = self.calcNorm3( )
        #self.meanShape.applyInvTrans( trans )
        

        
        return
        
    def calcNorm3( self ):
        ## Original shape (input)
        cmShape = ASM.centroid( self.meanShape )


        ############## Calc transformations ###################
        ## Translate
        t = [[ -cmShape.x ], [ -cmShape.y ]]
        self.meanShape.apply( t, 'translate' )

    
        ## Scale
        d1 = self.meanShape.shapePoints[0].dist( self.meanShape.shapePoints[1] )
        s = float(1)/float(d1)
        
        ## Rotation
        p0 = [ self.meanShape.shapePoints[0].x, self.meanShape.shapePoints[0].y ]
        axisVector = [ 0, 1]
        thetaP = ASM.angleV( p0, axisVector )
        thetaRot = thetaP
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
               [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        self.meanShape.apply( np.multiply( s, rot ), 'rotate')

    def calcNormTrans2( self ):
        cmShape  = ASM.centroid( self.meanShape )
        
        # Move centroid to origin
        t = [[ -cmShape.x ], [ -cmShape.y ]]
        
        ## Scale
        d1 = self.meanShape.shapePoints[0].dist( self.meanShape.shapePoints[1] )
        s = 1./float(d1)
        
        ## Rotation
        p0 = [ self.meanShape.shapePoints[0].x, self.meanShape.shapePoints[0].y ]
        axisVector = [ 1, 0 ]
        thetaP = ASM.angleV( p0, axisVector )
        thetaRot = math.pi / 2 - thetaP
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
               [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        return { 'rot' : np.multiply( s , rot) , 't': t}


    def calcNormTrans( self, shape1):
       
        start = time.time()
        ## Translation
        cmShape  = ASM.centroid( shape1 )
        cmMeanShape = ASM.centroid( self.meanShape )
        t = [[ cmShape.x - cmMeanShape.x ], [cmShape.y - cmMeanShape.y ]] 
        
        ## Scale
        d1 = shape1.shapePoints[0].dist( shape1.shapePoints[1] )
        d2 = self.meanShape.shapePoints[0].dist( self.meanShape.shapePoints[1] )
        s = d1/d2

        ## Rotation
        #http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
        p0 = [ shape1.shapePoints[0].x, shape1.shapePoints[0].y ]
        m0 = [ self.meanShape.shapePoints[0].x, self.meanShape.shapePoints[0].y ]
        axisVector = [ 1, 0 ]
        
        thetaP = ASM.angleV( p0, axisVector )
        thetaM = ASM.angleV( m0, axisVector )

        thetaRot = thetaP - thetaM

        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
               [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]
 
        return { 'rot' : np.multiply( s, rot) , 't':t }

    def calcAlignTrans( self, shape1, shape2 ):
        """
        start = time.time()
        coeffs = np.array( [
            [ self.Xgen( shape2 ), - self.Ygen( shape2 ), self.Wgen(), 0],
            [ self.Ygen( shape2 ), self.Xgen( shape2 ), 0, self.Wgen()],
            [ self.Zgen( shape2 ), 0, self.Xgen( shape2 ), self.Ygen( shape2 )],
            [ 0, self.Zgen( shape2 ), - self.Ygen( shape2 ), self.Xgen( shape2 )]
            ])
        eqs = np.array([ self.Xgen(shape1) ,  self.Ygen(shape1), self.C1gen(shape1, shape2), self.C2gen(shape1, shape2) ] )
        sol = np.linalg.solve( coeffs, eqs )
            # d = ax = s cos 0
            # e = ay = s sin 0
            # f = tx
            # g = ty

        rot = [[ sol[0], - sol[1]],
               [ sol[1], sol[0]] ]
        t = [[ sol[2]],[sol[3]]]
        
        """
        toSolve = Matrix( [
            [ self.Xgen( shape2 ), - self.Ygen( shape2 ), self.Wgen(), 0, self.Xgen(shape1) ],
            [ self.Ygen( shape2 ), self.Xgen( shape2 ), 0, self.Wgen(), self.Ygen(shape1) ],
            [ self.Zgen( shape2 ), 0, self.Xgen( shape2 ), self.Ygen( shape2 ), self.C1gen(shape1, shape2) ],
            [ 0, self.Zgen( shape2 ), - self.Ygen( shape2 ), self.Xgen( shape2 ), self.C2gen(shape1, shape2)]
            ])
                
        sol = solve_linear_system( toSolve, d, e, f, g)
            # d = ax = s cos 0
            # e = ay = s sin 0
            # f = tx
            # g = ty

        rot = [[ sol[d], - sol[e]],
               [ sol[e], sol[d]] ]
        t = [[ sol[f]],[sol[g]]]
        

        return { 'rot': rot, 't':t}
      
    def drawAll( self, axis, palette ):
        i = 0
        for el in self.allShapes:
            el.draw( palette, i, axis)
            i += 1
        axis.plot( self.meanShape.xs, self.meanShape.ys, c = 'k' )

    





#### SHAPE #####
class Shape( object ):
    def __init__(self, pointList ):
        self.shapePoints = []
        # Add points to shape
        if isinstance( pointList[0], list):
            for [x,y] in pointList:
                self.shapePoints.append( Point(x,y) )
        elif isinstance( pointList[0], tuple):
            for (x,y) in pointList:
                self.shapePoints.append( Point(x,y) )
        else:
            self.shapePoints = pointList
        
        self.xs, self.ys, self.Xi = self.unravel()

    def pointTable( self ):
        return pd.DataFrame( np.transpose([self.xs, self.ys, range(self.n)]), columns = ['x','y','shape'] )
        
    def unravel( self ):
        allPts = []
        x = []
        y = []
        for pt in self.shapePoints:
            allPts.append( pt.x)
            x.append( pt.x)
            allPts.append( pt.y )
            y.append( pt.y )
        return x, y, allPts

    @property
    def n( self ):
        return len( self.shapePoints )
        
    @property
    def R( self ):
        """
        Distance matrix between all points
        """
        sp = self.shapePoints
        ds = [ [sp[k].dist( sp[l] ) for k in range( self.n )] for l in range( self.n ) ]
        return ds
    
    def update( self ):
        self.xs, self.ys, self.Xi = self.unravel()

    def applyInvTrans( self, transf ):
        for pt in self.shapePoints:
            pt.invTrans( transf )
        self.update()
        
    def apply( self, arg, op ):

        for pt in self.shapePoints:
            getattr( pt, op )(arg)

        self.update()

    def applyTrans( self, transf ):
        for pt in self.shapePoints:
            pt.transform( transf )
        self.update()
    
    def draw( self, palette, i, axis ):
        _ = axis.scatter( self.xs, self.ys, c = palette[i], label = i )


    def __str__( self ):
        a = map( str, self.shapePoints )
        return ''.join( a )



### POINTS ###       

class Point( object ):
    def __init__( self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        self.p = (self.x, self.y)
        self.v = [[ self.x],[self.y]]

    def getX( self ):
        return self.__x

    def getY( self ):
        return self.__y
    
    @property
    def x( self ):
        return self.__x
    @property
    def y( self ):
        return self.__y

    def dist( self, pt):
        return math.sqrt( (self.__x - pt.x)**2 + (self.__y - pt.y)**2 )

    def update(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        self.p = (self.x, self.y)
        self.v = [[ self.x],[self.y]]


    def transform( self, transDict ):
        x, y = np.dot( transDict['rot'], self.v ) + transDict['t']
        self.update( x,y )

    def rotate( self, rot ):
        x, y = np.dot( rot , self.v )
        self.update( x, y ) 

    def scale( self, scale ):
        x, y = np.multiply( scale, self.v )
        self.update( x, y )

    def translate( self, vect ):
        x, y = np.add( self.v, vect )
        self.update( x, y ) 



    def __str__( self ):
        return "(%d, %d)" % (self.__x, self.__y)
