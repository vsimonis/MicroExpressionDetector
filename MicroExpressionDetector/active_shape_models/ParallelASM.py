import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import functools
from pathos.multiprocessing import ProcessingPool as PPool
from sklearn.metrics.pairwise import pairwise_distances
import random

class PASM( object ):
    """
    Parallel ASM implmentation
    """

    
    def __init__( self, refIndices, numIterations ):
        self.allShapes = []
        self.n = 0
        self.refIxs = refIndices
        self.nIters = numIterations

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
    


    def calcWs( self ):
        """
        Calculates and instantiates:
        self.w <-- vector of weights (length == number of points (n) )
        self.W <-- diagonal matrix representing vector (n x n)

        These weights represent the influence of each point
        (by distance among corresponding points across training shapes)  

        

        """
        start = time.time()
        # Get variance matrix V
        for mm in range( len(self.allShapes) ):
            self.allShapes[mm].calcR()
            
        V = []
        for k in range(self.n):
            row = []
            for l in range(self.n):
                col = []
                for i in range(len( self.allShapes )):
                    col.append( self.allShapes[i].R[k][l])
                row.append( np.var(col) )
            V.append(row)
       

        s = map( sum, V)
        self.w = [ math.pow( j, -1) for j in s]
        #self.w = [ 1 for j in s]
        self.W = np.diag(self.w)
        ##print "calcWs: %f" % (time.time() - start)
        

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
        start = time.time()
        xList = [ el.xs for el in self.allShapes ]
        yList = [ el.ys for el in self.allShapes ]
        meanPointsList = zip( np.mean(xList, 0), np.mean(yList, 0) )
        self.meanShape = Shape( meanPointsList )
        #print "CalcMeanShape %f" % (time.time() - start)


    def iterateAlignment( self ):

        # Setup drawing

        #colors = ["purple", "light purple", 
        #        "blue", "cyan", "neon blue"]
                #"red", "rose",
                #"green", "bright green", "mint"]
#        roygbv
        co = ['lightish red', 'yellowish orange', 'canary yellow', 'lime', 'cyan']#,'lavender]

        co = random.sample( sns.xkcd_rgb.keys(), self.n )
        pal = sns.xkcd_palette( co )
        

        for i in range( self.nIters ):
            print i
            f, (ax1,ax2) = plt.subplots(1,2, sharex= True, sharey=True)
            ## Calculate mean shape
            self.calcMeanShape( )
            ax1.plot( self.meanShape.xs, self.meanShape.ys, c = 'k', lw = 1 )            
            
            ## Normalize mean shape
            self.normShape( self.meanShape )

            map( lambda t : t.draw( pal, ax1 ), self.allShapes )



            ## Realign
            self.alignAllShapes( )
            
            map( lambda t : t.draw( pal, ax2 ), self.allShapes )
            ax2.plot( self.meanShape.xs, self.meanShape.ys, c = 'k', lw = 1 )

            # Draw change
            self.calcMeanShape()


            f.savefig( "C:/Users/Valerie/Desktop/stars/plots%d/%d.png" % (self.n, i ) )
            f.clear()
            plt.close()
            i += 1
        # Show
#        f.show()


    def alignAllShapes( self ):
        start = time.time()
        self.calcWs() 
        self.allShapes = PPool().map( self.alignOneShape, self.allShapes )
        print 'alignAllShapes: %f' % (time.time() - start  )
        return 

    def alignTwoShapes( self, shape1, shape2 ):
        """
        Aligns returns rotation, translation and scaling
        mapping shape1 to shape2 
        ** trans( shape1 ) --> shape2
        """
        transDict = self.calcAlignTransBtwn( shape1, shape2 )
        shape1.transform( transDict )

        return shape1

    
    def alignOneShape( self, shape ):
        start = time.time()
        transDict = self.calcAlignTrans( shape )
        shape.transform( transDict )
        #print "alignOneShape: %f" % ( time.time() - start )
        return shape

    def calcAlignTransBtwn( self, shape1, shape2):
        start = time.time()
        coeffs = np.array( [
            [ self.Xgen( shape1 ), - self.Ygen( shape1 ), self.Wgen(), 0],
            [ self.Ygen( shape1 ), self.Xgen( shape1 ), 0, self.Wgen()],
            [ self.Zgen( shape1 ), 0, self.Xgen( shape1 ), self.Ygen( shape1 )],
            [ 0, self.Zgen( shape1 ), - self.Ygen( shape1 ), self.Xgen( shape1 )]
            ])
        eqs = np.array([ self.Xgen(shape2) ,  self.Ygen(shape2), self.C1gen(shape2, shape1), self.C2gen(shape2, shape1) ] )
        sol = np.linalg.solve( coeffs, eqs )
            # d = ax = s cos 0
            # e = ay = s sin 0
            # f = tx
            # g = ty

        rot = [[ sol[0], - sol[1]],
               [ sol[1], sol[0]] ]

        t = [[ sol[2]],[sol[3]]]
        #print "calc align: %f" % ( time.time() - start )
        return { 'rot': rot, 't':t}

    def calcAlignTrans( self, shape ):
        return calcAlignTransBtwn( shape, self.meanShape )
        """
        start = time.time()
        coeffs = np.array( [
            [ self.Xgen( shape ), - self.Ygen( shape ), self.Wgen(), 0],
            [ self.Ygen( shape ), self.Xgen( shape ), 0, self.Wgen()],
            [ self.Zgen( shape ), 0, self.Xgen( shape ), self.Ygen( shape )],
            [ 0, self.Zgen( shape ), - self.Ygen( shape ), self.Xgen( shape )]
            ])
        eqs = np.array([ self.Xgen(self.meanShape) ,  self.Ygen(self.meanShape), self.C1gen(self.meanShape, shape), self.C2gen(self.meanShape, shape) ] )
        sol = np.linalg.solve( coeffs, eqs )
            # d = ax = s cos 0
            # e = ay = s sin 0
            # f = tx
            # g = ty

        rot = [[ sol[0], - sol[1]],
               [ sol[1], sol[0]] ]
        t = [[ sol[2]],[sol[3]]]
        #print "calc align: %f" % ( time.time() - start )
        return { 'rot': rot, 't':t}
        """



    
    def normShape( self, shape  ):
        """
        Calculates and applies normalization to passed shape
        """

        ############## Calc transformations ###################
        ## Translate centroid as origin
        cmShape = PASM.centroid( shape )
        t = [[ -cmShape.x ], [ -cmShape.y ]] 
        shape.translate( t )

        leftEyeIx = self.refIxs[0]
        rightEyeIx = self.refIxs[1]
    
        ## Scale
        # distance between two "eyes"
        d = shape.shapePoints[leftEyeIx].dist( shape.shapePoints[rightEyeIx] )
        s = float(1)/float(d)
        
        ## Rotation
        # eyes level
        xDiff = shape.shapePoints[rightEyeIx].x - shape.shapePoints[leftEyeIx].x
        yDiff = shape.shapePoints[rightEyeIx].y - shape.shapePoints[leftEyeIx].y
        p0 = [ xDiff, yDiff ] 
        axisVector = [ 1, 0]
        thetaP = PASM.angleV( p0, axisVector )
        thetaRot = thetaP
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
                [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        shape.rotate( rot )
        shape.scale( s )

        return shape
    
      
    def drawAll( self, axis, palette ):
        i = 0
        for el in self.allShapes:
            el.draw( palette, i, axis)
            i += 1
        axis.plot( self.meanShape.xs, self.meanShape.ys, c = 'k' )

 


    def __str__( self ):
        return "(%d, %d)" % (self.__x, self.__y)


class Shape( object ):
    """
    Shape object

    Data members:
    - shapePoints
    - R
    - allPoints
    - diffAllPoints
    
    """

    def __init__(self, pointList ):
        import numpy as np
        import math
        import matplotlib.pyplot as plt
        import seaborn as sns

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
        
    @property
    def xs( self ):
        """
        returns all x values of all points for a given shape
        """

        return map( lambda pt : pt.x, self.shapePoints )

    @property
    def ys( self ):
        """
        returns all y values of all points for a given shape
        """
        return map( lambda pt : pt.y, self.shapePoints )

    @property
    def n( self ):
        """
        returns the number of points in a given shape
        """
        return len( self.shapePoints )
        
    def calcR( self ):
        """
        Calculates distance matrix between all points for a given shape
        sets global variable 
        """
        sp = self.shapePoints
        ## For every point in shapePoints, calculate distance to other points
        self.R = [ [sp[k].dist( sp[l] ) for k in range( self.n )] for l in range( self.n ) ]
        return self.R

    
    def unravel( self ):
        allPts = []
        for pt in self.shapePoints:
            allPts.append( pt.x)
            allPts.append( pt.y )
        self.allPts = allPts
        return allPts 

    def calcDiff( self, shape ):
        self.unravel()
        shape.unravel()
        self.diffAllPts = np.subtract( self.allPts, shape.allPts)
        return self.diffAllPts
     
    def calcSingleCov( self ):
        self.singleCov = np.dot( np.transpose(np.mat(self.diffAllPts)),  np.mat(self.diffAllPts) )
        return self.singleCov

    # Shape operations
    def transform( self, transformation ):
        self.shapePoints = map( lambda q : q.transform( transformation ), self.shapePoints )

    def rotate( self, rotation ):
        self.shapePoints = map( lambda q : q.rotate( rotation ), self.shapePoints )

    def translate( self, translation ):
        self.shapePoints = map( lambda q : q.translate( translation ) , self.shapePoints )

    def scale( self, scaling ):
        self.shapePoints = map( lambda q : q.scale( scaling ) , self.shapePoints )


    def draw( self, palette, axis ):
        _ = axis.scatter( self.xs, self.ys, c = palette, s= 10 )


    def __str__( self ):
        a = map( str, self.shapePoints )
        return ''.join( a )


   
class Point( object ):

    def __init__( self, x, y):
        import numpy as np
        import math
        self.__x = float(x)
        self.__y = float(y)
        
    ## Properties (avoid need to update) 
    @property
    def p( self ):
        return ( self.__x, self.__y )
    @property
    def v( self ):
        return [[ self.__x ],[ self.__y ]]
    @property
    def x( self ):
        return self.__x
    @property
    def y( self ):
        return self.__y

    def setY( self,y ):
        self.__y = y
        #print 'new y'

    def setX( self,x ):
        self.__x = x
        #punrint 'new x'

    def dist( self, pt):
        return math.sqrt( (self.__x - pt.x)**2 + (self.__y - pt.y)**2 )
    
    def transform( self, transDict ):
        x1, y1 = np.dot( transDict['rot'], self.v ) + transDict['t']
        return Point( x1, y1 )

    def rotate( self, rot ):
        x1, y1 = np.dot( rot , self.v )
        return Point( x1, y1 )

    def scale( self, scale ):
        x1, y1 = np.multiply( scale, self.v )
        return Point( x1, y1 )

    def translate( self, vect ):
        x1, y1 = np.add( self.v, vect )
        return Point( x1, y1 ) 

    def __str__(self):
        return '%f\t%f\n' % ( self.x, self.y )