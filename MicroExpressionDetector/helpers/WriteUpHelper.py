import sys
sys.path.append( ".." )

import os
from helpers.DrawFace import DrawFace
from shapes.ActiveShape import ActiveShape
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import math


class WriteUp(object):
    def __init__( self, ASM, FileHelper ):
        self.asm = ASM
        self.fh = FileHelper
        self.nPlots = 5
        self.P = ASM.evecs
        self.b = np.ravel( ASM.evals  )
        self.lim =  0.25
        self.xbar = ASM.meanShape.flatten()
        self.xlim = (-3,3)
        self.ylim = (-3,3)
        self.out = os.path.join( FileHelper.output, "PCA")
      

    def PCAresults( self ) : 
        with open( os.path.join( self.out, 'faces-results-%diters-%dtr.txt' % (self.fh.nIters, self.fh.nTrain)),  'w') as outfile:
            for i in range( 20 ):
                outfile.write("%d: %f, %f \n" % ( i, self.b[i] / sum( self.b ), sum( self.b[:i+1] ) / sum(self.b ) ) )

        ## Reproject multiple PCS and vary evals 
        for i in range( 10 ):
            self.showVaryMultiplePCS( i + 1 )
            self.showVary( i )
            self.exampleEvalEvecs( i ) 

        ### Draw all faces
        for sh in self.asm.allShapes :
            DrawFace( sh, plt ).drawContrast()
        plt.gca().invert_yaxis()    
        plt.savefig( os.path.join( self.out, 'faces-all-%diters-%dtr.png' % (self.fh.nIters, self.fh.nTrain) ) )
        plt.close()


    def showVaryMultiplePCS( self, numPCs ):
        f, axes = plt.subplots( 1, self.nPlots )
        bs = []
        for p in range( numPCs ):
            rs = np.linspace( - self.lim * math.sqrt( self.b[p] ), self.lim * math.sqrt( self.b[p] ), self.nPlots )
            bs.append( rs )
        P = self.P[:, 0:numPCs]
        for pl in range(self.nPlots) :
            b = [ bs[p][pl] for p in range(len(bs) ) ]
            X = np.add( self.xbar, np.dot( P, b ) )
            s = ActiveShape.createShape( X )
            DrawFace( s, axes[pl] ).drawBold()
            axes[pl].set_xlim( self.xlim )
            axes[pl].set_ylim( self.ylim )
            axes[pl].invert_yaxis()
        f.savefig( os.path.join( self.out, 'faces-%d-PCs-at-once.png' % numPCs ) )
        plt.close()

    def showVary( self, evIx  ) :
        # Vary one eigenvalue
        f, axes = plt.subplots( 1, self.nPlots, sharex = True, sharey = True )
        
        rs = np.linspace( -self.lim * math.sqrt( self.b[evIx] ), self.lim * math.sqrt( self.b[evIx] ), self.nPlots )
    
        for m in range( len(rs) ):
            s = self.projectOnePC( evIx, rs[m] )
            DrawFace( s, axes[m] ).drawBold()
            axes[m].set_xlim( self.xlim)
            axes[m].set_ylim( self.ylim )
            self.plotEigenvectors( evIx, axes[m])
            DrawFace( self.asm.meanShape, axes[m] ).drawContrast()
        plt.gca().invert_yaxis()    
        f.savefig( os.path.join( self.out, 'faces-PC-%d.png' % evIx ) )

        plt.close()

    def plotEigenvectors( self, evIx, axes  ):
        for ptIx in np.multiply( 2, range(self.asm.n) ):
            axes.plot( [ self.xbar[ptIx], self.xbar[ptIx] + self.lim * math.sqrt(self.b[evIx] )* self.P[ptIx][evIx] ] , 
                     [ self.xbar[ptIx+1], self.xbar[ptIx+1] + self.lim * math.sqrt( self.b[evIx] )* self.P[ptIx + 1][evIx] ],
                     c = '#A0A0A0', 
                     lw = 0.5)
            axes.plot( [ self.xbar[ptIx], self.xbar[ptIx] - self.lim * math.sqrt(self.b[evIx] )* self.P[ptIx][evIx] ] , 
                     [ self.xbar[ptIx+1], self.xbar[ptIx+1] - self.lim * math.sqrt( self.b[evIx] )* self.P[ptIx + 1][evIx] ],
                     c = '#A0A0A0', 
                     lw = 0.5)

   
    def projectOnePC( self, evIx, b )  :
        X = np.add( self.xbar, np.multiply( self.P[:,evIx],  b ) )
        return ActiveShape.createShape( X )

    def reProjectCumulative( self, numVals ) :
        P = self.P[:, 0:numVals]
        b = [ np.transpose(np.mat( self.b[ 0: numVals ] )) ] 

        X = np.add( self.xbar, np.dot( P, b ) )

        return ActiveShape.createShape( X )





    def exampleEvalEvecs( self, evIx ):
        vecs = np.array( self.P )
        newPts = np.add( self.xbar, np.dot(math.sqrt( self.b[evIx] ), vecs[:,evIx] ) )

        newx, newy = ActiveShape.deravel( newPts )

        ## Mean Shape
        DrawFace( self.asm.meanShape, plt ).drawBold()

        ## Eigenvectors
        plt.plot( [self.asm.meanShape.xs, np.add( self.asm.meanShape.xs, newx ) ], 
                [ self.asm.meanShape.ys, np.add( self.asm.meanShape.ys, newy ) ], c ='#A0A0A0', lw = 1 )
        plt.xlim( self.xlim )
        plt.ylim( self.ylim )

        ## New Shape
        plt.gca().invert_yaxis()    
        plt.savefig( os.path.join( self.out, 'faces-eigenvectors-%d.png' % evIx ))
        plt.close()

  




