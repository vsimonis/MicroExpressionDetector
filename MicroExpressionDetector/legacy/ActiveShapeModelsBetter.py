import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import functools
from pathos.multiprocessing import ProcessingPool as Pool
from Geometry import Point, Shape


class ASMB( object ):
    def __init__( self, refIndices, numIterations ):
        self.allShapes = []
        self.n = 0
        self.refIxs = refIndices
           self.nIters = numIterations
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


    def iterateAlignment( self ):

        # Setup drawing

        #colors = ["purple", "light purple", 
        #        "blue", "cyan", "neon blue"]
                #"red", "rose",
                #"green", "bright green", "mint"]
#        roygbv
        co = ['lightish red', 'yellowish orange', 'canary yellow', 'lime', 'cyan']#,'lavender]
        pal = sns.xkcd_palette( co )
        

        for i in range( self.nIters ):
            f, (ax1,ax2) = plt.subplots(1,2)#, sharex= True, sharey=True)
            ## Calculate mean shape
            self.calcMeanShape( )
            ax1.plot( self.meanShape.xs, self.meanShape.ys, 'k' )            
            
            ## Normalize mean shape
            self.normMeanShape( )

            for sh in self.allShapes:
                sh.draw( pal, ax1)
                


            ## Realign
            self.alignAllShapes( )
            for sh in self.allShapes:
                sh.draw( pal, ax2 )
                ax2.plot( self.meanShape.xs, self.meanShape.ys, 'k' )

            # Draw change
            self.calcMeanShape()


            f.savefig( "C:/Users/Valerie/Desktop/stars/plots5/%d.png" % i )
            f.clear()
            plt.close()
            i += 1
        # Show
#        f.show()

   # def isConverged( self ):
    def alignAllShapes( self ):
        import pathos.multiprocessing as mp
        start = time.time()
        pool = Pool()
        self.allShapes = pool.map( self.alignOneShape, self.allShapes )
#        for sh in self.allShapes:
#          self.alignOneShape( sh )
        print 'alignAllShapes: %f' % (time.time() - start  )
        return 

    
    def alignOneShape( self, shape ):
        start = time.time()
        transDict = self.calcAlignTrans( shape )
        shape.applyTrans( transDict )
        return shape

    @staticmethod
    def centroid( shape1 ):
        return Point( np.mean( shape1.xs ) , np.mean( shape1.ys ) )

    @staticmethod
    def unitV( v ): 
        return v / np.linalg.norm( v )

    @staticmethod
    def angleV( v1, v2 ):
        return math.atan2( v1[0], v1[1] ) - math.atan2( v2[0], v2[1] )

    def normMeanShape( self ):
        ############## Calc transformations ###################
        ## Translate
        cmShape = ASMB.centroid( self.meanShape )
        t = [[ -cmShape.x ], [ -cmShape.y ]] 

        self.meanShape.translate( t )
        self.meanShape.update( )

        leftEyeIx = self.refIxs[0]
        rightEyeIx = self.refIxs[1]
    
        ## Scale
        # distance between two "eyes"
        d = self.meanShape.shapePoints[leftEyeIx].dist( self.meanShape.shapePoints[rightEyeIx] )
        s = float(1)/float(d)
        
        ## Rotation
        xDiff = self.meanShape.shapePoints[rightEyeIx].x - self.meanShape.shapePoints[leftEyeIx].x
        yDiff = self.meanShape.shapePoints[rightEyeIx].y - self.meanShape.shapePoints[leftEyeIx].y
    
        p0 = [ xDiff, yDiff ] #self.meanShape.shapePoints[0].x, self.meanShape.shapePoints[0].y ]
        axisVector = [ 1, 0]
        thetaP = ASMB.angleV( p0, axisVector )
        thetaRot = thetaP
    
        rot = [[ math.cos( thetaRot ), -math.sin( thetaRot ) ],
                [ math.sin( thetaRot ), math.cos( thetaRot ) ] ]

        self.meanShape.rotate( rot )
        self.meanShape.update( )
        
        self.meanShape.scale( s )
        self.meanShape.update( )
        return

    def calcAlignTrans( self, shape ):
       
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
        
        return { 'rot': rot, 't':t}
      
    def drawAll( self, axis, palette ):
        i = 0
        for el in self.allShapes:
            el.draw( palette, i, axis)
            i += 1
        axis.plot( self.meanShape.xs, self.meanShape.ys, c = 'k' )

    





#### SHAPE #####




### POINTS ###       

