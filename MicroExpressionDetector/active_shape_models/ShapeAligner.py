from shapes.ActiveShape import ActiveShape
from active_shape_models.ActiveShapeModel import ActiveShapeModel

from helpers.FileHelper import FileHelper

from shapes.Vector import Vector
from shapes.Shape import Shape

import numpy as np
import math
import logging
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
        self.out = os.path.join( out, "Align" )
        if not os.path.exists( self.out ):
            os.mkdir( self.out )

        
    def alignTrainingSet( self ):

        ## Setup drawing
        co = random.sample( sns.xkcd_rgb.keys(), self.n )
        pal = sns.xkcd_palette( co )
        

        for i in range( self.nIters ):
            start = time.time()

            # Calculate mean shape
            self.asm.meanShape = self.asm.calcMeanShape()
            
            if i == 0:
                map( lambda t : t.draw( pal, plt ), self.asm.allShapes )
                plt.plot( self.asm.meanShape.xs, self.asm.meanShape.ys, c = 'k', lw = 1 )
                plt.gca().invert_yaxis()
                plt.savefig( os.path.join( self.out, "no-alignment-%d.png" % i ) )

                plt.close()

            # Normalize mean shape
            self.asm.normMeanShape = self.asm.normShape( self.asm.meanShape )

            # Align all shapes to normalized mean shape
            self.asm.allShapes = self.alignAllShapes()
            map( lambda t : t.draw( pal, plt ), self.asm.allShapes )
            plt.plot( self.asm.normMeanShape.xs, self.asm.normMeanShape.ys, c = 'k', lw = 1 )
            plt.gca().invert_yaxis()
            plt.savefig( os.path.join( self.out, "alignment-%d.png" % ( i ) ) )
            plt.close()

            with open( os.path.join( self.out, 'log.txt' ), 'a' )  as of:
                of.write( "AlignIter: %f\n" % ( time.time() - start ) )
                of.write( '%d\n\n' % i )
            print i


        return self.asm

                                                 
    ### Alignment methods
    ## Generators
    def Zgen( self, shape, w ):
        SS = map( lambda a, b : a**2 + b**2, shape.xs, shape.ys )
        return np.dot( SS, w )
        

    def Xgen( self, shape, w ):
        return np.dot( shape.xs, w )

    def Ygen( self, shape, w ):
        return np.dot( shape.ys, w )

    def Wgen( self, w ):
        return sum( w )

    def C1gen( self, shape1, shape2, w):
        SW = map( lambda a, b, c,d : a * b + c * d, 
                 shape1.xs, shape2.xs, shape1.ys, shape2.ys )
        return np.dot( SW, w )

    def C2gen( self, shape1, shape2, w):
        SB = map( lambda a, b, c,d : c * b - a * d, 
                 shape1.xs, shape2.xs, shape1.ys, shape2.ys )
        return np.dot( SB, w )


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
        transDict = self.calcAlignTransBtwn( self.asm.normMeanShape, shape,  w )
        shape = shape.transform( transDict )
        return shape

    def calcAlignTransBtwn( self, shape1, shape2, w):
        start = time.time()
        coeffs = np.array( [
            [ self.Xgen( shape2, w ), - self.Ygen( shape2, w ), self.Wgen( w )          , 0],
            [ self.Ygen( shape2, w ), self.Xgen( shape2, w )  ,   0                     , self.Wgen( w )],
            [ self.Zgen( shape2, w ), 0                       , self.Xgen( shape2, w )  , self.Ygen( shape2, w )],
            [ 0                     , self.Zgen( shape2, w )  , - self.Ygen( shape2, w ), self.Xgen( shape2, w )]
            ])
        eqs = np.array([ self.Xgen( shape1, w ) ,  
                        self.Ygen( shape1, w ), 
                        self.C1gen( shape1, shape2, w ), 
                        self.C2gen( shape1, shape2, w ) ] )

        sol = np.linalg.solve( coeffs, eqs )
        d = sol[0]    # d = ax = s cos 0    --> 0
        e = sol[1]    # e = ay = s sin 0    --> 1
        f = sol[2]    # f = tx              --> 2
        g = sol[3]    # g = ty              --> 3
        
            
        srot = [[ d, - e],
               [ e,   d] ]

        t = [[ f ],[ g ]]

        theta = math.atan( e / d )

        s =  math.sqrt( d**2 + e**2 )

        #print 'CalcAlign: %f' % ( time.time() - start )
        return { 'srot': srot, 't':t , 'theta' : theta, 's' : s }


    def shapeDist( self ):
        allD = map( lambda x : x.shapeDist( self.asm.normMeanShape ), self.asm.allShapes )
        return  np.mean(np.mean( allD, 0 )), np.mean(np.std( allD, 0 )), np.mean(np.mean( allD, 1 )), np.mean(np.std( allD, 1 )     )


    def alignAllShapes( self ):
        start = time.time()
        w, W = self.calcWs() 
        freeze_support()
        allShapes = PPool().map( lambda x : self.alignOneShape( x, w ), self.asm.allShapes )
        mn1, sd1, mn2,sd2 = self.shapeDist() 
        with open( os.path.join( self.out, 'log.txt' ), 'a' )  as of: 
            of.write('point-wise mean:\t%f\n' % mn1 )
            of.write('point-wise std:\t%f\n' % sd1 ) 
            of.write('shape-wise mean:\t%f\n'% mn2 )
            of.write('shape-wise std:\t%f\n' % sd2 )
            of.write( 'alignAllShapes: %f\n' % (time.time() - start  ) ) 
        return allShapes