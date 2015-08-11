from shapes.ActiveShape import ActiveShape
from active_shape_models.ActiveShapeModel import ActiveShapeModel

from helpers.FileHelper import FileHelper

from shapes.Vector import Vector
from shapes.Shape import Shape

import numpy as np
import math

import matplotlib.pyplot as plt
import seaborn as sns
import functools

from pathos.multiprocessing import ProcessingPool as PPool
from multiprocessing import freeze_support
import random
import time
import os

class ShapeAligner( object ):
    
    def __init__( self, asm, nIters, out ):
        self.asm = asm
        self.nIters = nIters
        self.n = asm.n
        self.out = out

        
    def alignTrainingSet( self ):

        ## Setup drawing
        co = random.sample( sns.xkcd_rgb.keys(), self.n )
        pal = sns.xkcd_palette( co )
        

        for i in range( self.nIters ):
            
            # Drawing
            f, (ax1,ax2) = plt.subplots(1,2, sharex= True, sharey=True)

            # Calculate mean shape
            self.asm.meanShape = self.asm.calcMeanShape()
            ax1.plot( self.asm.meanShape.xs, self.asm.meanShape.ys, c = 'k', lw = 1 )            

            # Normalize mean shape
            self.asm.normMeanShape = self.asm.normShape( self.asm.meanShape )
            map( lambda t : t.draw( pal, ax1 ), self.asm.allShapes )

            # Align all shapes to normalized mean shape
            self.asm.allShapes = self.alignAllShapes()
            map( lambda t : t.draw( pal, ax2 ), self.asm.allShapes )
            ax2.plot( self.asm.normMeanShape.xs, self.asm.normMeanShape.ys, c = 'k', lw = 1 )
            
            f.savefig( os.path.join( self.out, "%d-%d.png" % ( self.nIters, i ) ) )
            f.clear()
            plt.close()
            print i


        return self.asm


    ### Alignment methods
    ## Generators
    def Zgen( self, shape, w ):
        return sum( [  w[k] * ( shape.xs[k] **2 +
                                    shape.xs[k] **2 )
                     for k in range( self.n ) ] )

    def Xgen( self, shape, w ):
        return sum( [  w[k] * shape.xs[k] 
                     for k in range( self.n ) ] )

    def Ygen( self, shape, w ):
        return sum( [ w[k] * shape.ys[k] 
                     for k in range( self.n ) ] )

    def Wgen( self, w ):
        return sum( [ w[k]  for k in range( self.n ) ] )

    def C1gen( self, shape1, shape2, w):
        return sum( [ w[k] * 
                    ( shape1.xs[k] * shape2.xs[k] +
                    shape1.ys[k] * shape2.ys[k] )
                    for k in range( self.n) ] )
    
    def C2gen( self, shape1, shape2, w):
        return sum( [ w[k] * 
                    ( shape1.ys[k] * shape2.xs[k] +
                    shape1.xs[k] * shape2.ys[k] )
                    for k in range( self.n) ] )


    def calcWs( self ):
        """
        Calculates and returns:
        w <-- vector of weights (length == number of points (n) )
        W <-- diagonal matrix representing vector (n x n)

        These weights represent the influence of each point
        (by distance among corresponding points across training shapes)  
        """

        # Get variance matrix V
        V = []

        for k in range(self.n): 
            row = []
            for l in range(self.n):
                col = []
                for i in range(len( self.asm.allShapes )):
                    col.append( self.asm.allShapes[i].R[k][l])
                row.append( np.var(col) )
            V.append(row)
       
            
        s = map( sum, V)
        w = [ math.pow( j, -1) for j in s]
        W = np.diag(w)
        return w, W

    def alignOneShape( self, shape, w ):
        transDict = self.calcAlignTransBtwn( shape, self.asm.normMeanShape, w )
        shape = shape.transform( transDict )
        return shape

    def calcAlignTransBtwn( self, shape1, shape2, w):
        start = time.time()
        coeffs = np.array( [
            [ self.Xgen( shape1, w ), - self.Ygen( shape1, w ), self.Wgen( w ), 0],
            [ self.Ygen( shape1, w ), self.Xgen( shape1, w ), 0, self.Wgen( w )],
            [ self.Zgen( shape1, w ), 0, self.Xgen( shape1, w ), self.Ygen( shape1, w )],
            [ 0, self.Zgen( shape1, w ), - self.Ygen( shape1, w ), self.Xgen( shape1, w )]
            ])
        eqs = np.array([ self.Xgen( shape2, w ) ,  self.Ygen( shape2, w ), 
                        self.C1gen( shape2, shape1, w ), self.C2gen( shape2, shape1, w ) ] )
        sol = np.linalg.solve( coeffs, eqs )
            # d = ax = s cos 0
            # e = ay = s sin 0
            # f = tx
            # g = ty

        rot = [[ sol[0], - sol[1]],
               [ sol[1], sol[0]] ]

        t = [[ sol[2]],[sol[3]]]

        return { 'rot': rot, 't':t}

    def alignAllShapes( self ):
        start = time.time()
        w, W = self.calcWs() 
        freeze_support()
        allShapes = PPool().map( lambda x : self.alignOneShape( x, w ), self.asm.allShapes )
        print 'alignAllShapes: %f' % (time.time() - start  )
        return allShapes


